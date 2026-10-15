#!/usr/bin/env python3
"""Find dead air, filler words, flubs and retakes in raw talking-head footage.

Combines two signals, because neither is enough alone:
  * ffmpeg silencedetect  -> exact pause boundaries (ASR word timestamps stretch
    across silences, so gaps between words can't be trusted for cut points)
  * a word-level transcript from `npx hyperframes transcribe` (use
    `--engine parakeet`; its word start times are far more accurate than
    whisper's) -> what was said, so we can spot fillers, retake cues and
    repeated takes. Rule: the LAST take of a repeated line wins.

Usage (from inside a project folder):
  npx hyperframes transcribe assets/raw.mp4 --engine parakeet --json
  python3 ../../scripts/detect-edits.py assets/raw.mp4 transcript.json \
      --out edit-plan.json [--script script.txt] [--render renders/rough-cut.mp4]

Writes edit-plan.json: {"keep": [[start, end], ...], "cuts": [{start, end, reason, text}],
"review": [{start, said, script}]} — review lists off-script lines that were NOT cut.
The plan is a proposal — review it against the script before building on it.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys

FILLERS = {"um", "uh", "uhm", "umm", "er", "erm", "ah", "hmm", "mm"}
RETAKE_CUES = [
    r"\blet me (start|say|do|try) (that|this|it)? ?(again|over)\b",
    r"\b(start|starting) (that|this) (again|over)\b",
    r"\bone more time\b",
    r"\bscratch that\b",
    r"\btake (two|2|three|3)\b",
    r"^(wait|sorry|no)\b",
]
RETAKE_WINDOW = 45.0  # seconds after a segment in which a re-take of it is looked for


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def spell(n):
    """30 -> 'thirty', 147 -> 'one hundred forty seven' (so '30' matches a script's 'thirty')."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + spell(n % 100))
    if n < 1_000_000:
        return spell(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + spell(n % 1000))
    return str(n)


def norm(word):
    return re.sub(r"[^a-z0-9']", "", word.lower())


def script_tokens_of(text):
    """Tokens for diffing: numbers spelled out, '$5,000' -> 'five thousand'."""
    out = []
    for raw in text.split():
        t = norm(raw.replace(",", ""))
        out.extend(spell(int(t)).split() if t.isdigit() else [t] if t else [])
    return out


def detect_silences(media, noise_db, min_silence):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", media, "-af",
         f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    duration = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", media],
        capture_output=True, text=True,
    ).stdout.strip())
    if len(ends) < len(starts):  # trailing silence runs to end of file
        ends.append(duration)
    return list(zip(starts, ends)), duration


def speech_segments(silences, duration):
    segs, t = [], 0.0
    for s, e in silences:
        if s - t > 0.05:
            segs.append({"start": t, "end": s, "words": []})
        t = e
    if duration - t > 0.05:
        segs.append({"start": t, "end": duration, "words": []})
    return segs


def assign_words(segs, words):
    # A word belongs to the segment containing its start; a start that falls in
    # a silence (ASR timing drifts a little either way) goes to the nearer side.
    for w in words:
        t = w["start"]
        nxt = next((i for i, s in enumerate(segs) if t < s["end"]), len(segs) - 1)
        if nxt > 0 and t < segs[nxt]["start"]:
            if t - segs[nxt - 1]["end"] < segs[nxt]["start"] - t:
                nxt -= 1
        segs[nxt]["words"].append(w)
    for s in segs:
        s["text"] = " ".join(w["text"] for w in s["words"])
        s["tokens"] = [norm(w["text"]) for w in s["words"] if norm(w["text"])]


def retaken(i, segs):
    """True if most of segment i is said again, in order, shortly after it.

    Retakes rarely restart with identical words ("a reason why..." then
    "There's a reason why..."), and a later take is often split across several
    pause-separated segments, so compare against the following speech joined
    together and require a long shared run, not a shared opening.
    """
    a = segs[i]["tokens"]
    if len(a) < 3:
        return False
    later = []
    for s in segs[i + 1:]:
        if s["start"] > segs[i]["end"] + RETAKE_WINDOW or len(later) > 2 * len(a) + 10:
            break
        later.extend(s["tokens"])
    m = difflib.SequenceMatcher(None, a, later, autojunk=False).find_longest_match(0, len(a), 0, len(later))
    return m.size >= max(3, -(-len(a) // 2))


def trim_boundary_repeats(kept):
    """'...with the results, / with the results that...': drop the repeated
    run (2-6 words) once. It comes off the START of the later segment, whose
    edge is a measured silence, so only one cut point relies on ASR timing
    (trimming the earlier segment's tail relies on it entirely, and ASR stamps
    drift ~0.2s). If the earlier segment is nothing but the repeat, drop it."""
    for s, nxt in zip(kept, kept[1:]):
        ws = [w for w in s["words"] if norm(w["text"])]
        head = [w for w in nxt["words"] if norm(w["text"])]
        for n in range(min(6, len(ws), len(head)), 1, -1):
            if [norm(w["text"]) for w in ws[-n:]] == [norm(w["text"]) for w in head[:n]]:
                for w in (ws if n == len(ws) else head[:n]):
                    w["cut"] = "repeated across pause"
                break


def load_quiet_finder(media, window=0.12):
    """Return snap(t): the quietest 20ms point within +-window of t. Used for
    cut points inside speech, where ASR word stamps are off by up to ~0.2s."""
    import math
    import struct
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", media, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = struct.unpack("<%dh" % (len(raw) // 2), raw)
    hop = 320  # 20ms
    rms = [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) for i in range(0, len(x) - hop, hop)]

    def snap(t):
        lo, hi = max(0, int((t - window) * 50)), min(len(rms) - 1, int((t + window) * 50))
        if hi <= lo:
            return t
        best = min(range(lo, hi + 1), key=lambda i: rms[i])
        return best / 50 + 0.01
    return snap


def mark_off_script(kept, script_tokens):
    """Diff kept words against the script. Only fillers ASR heard as a word
    ("uh" -> "a") and doubled words ("the the") are auto-cut. Every other
    difference becomes a review note, never a cut: speakers paraphrase and
    reorder ("Instagram and Facebook"), and cutting a single word there
    breaks the sentence."""
    words, toks = [], []
    for w in (w for s in kept for w in s["words"] if not w.get("cut")):
        for t in script_tokens_of(w["text"]):
            words.append(w)
            toks.append(t)
    review = []
    sm = difflib.SequenceMatcher(None, toks, script_tokens, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        said = " ".join(toks[i1:i2])
        chunk = toks[i1:i2]
        stutter = len(chunk) == 1 and (
            (i1 > 0 and toks[i1 - 1] == chunk[0]) or (i2 < len(toks) and toks[i2] == chunk[0]))
        if tag == "delete" and (stutter or all(t in FILLERS or t == "a" for t in chunk)):
            for w in words[i1:i2]:
                w["cut"] = "off-script stumble"
        elif tag in ("delete", "replace"):
            review.append({"start": words[i1]["start"], "said": said,
                           "script": " ".join(script_tokens[j1:j2])})
        elif tag == "insert":
            at = words[i1]["start"] if i1 < len(words) else words[-1]["end"]
            review.append({"start": at, "said": "", "script": " ".join(script_tokens[j1:j2])})
    return review


def plan(segs, max_pause, pad, script_tokens=None, snap=lambda t: t):
    cuts = []
    for i, s in enumerate(segs):
        toks = s["tokens"]
        if not toks:
            s["drop"] = "no speech (noise/breath)"
        elif any(re.search(p, " ".join(toks)) for p in RETAKE_CUES):
            s["drop"] = "retake cue"
        elif retaken(i, segs):
            s["drop"] = "flubbed take (re-said later)"
        elif all(t in FILLERS for t in toks):
            s["drop"] = "filler only"
    # A take abandoned mid-line ("...leads to") is often followed by a cue
    # segment, then the clean retake: catch it via the line it restarts.
    for i, s in enumerate(segs):
        if "drop" not in s and i + 1 < len(segs) and segs[i + 1].get("drop") == "retake cue":
            if retaken(i, segs):
                s["drop"] = "flubbed take (re-said later)"

    kept = [s for s in segs if "drop" not in s]
    for s in segs:
        if "drop" in s:
            cuts.append({"start": round(s["start"], 3), "end": round(s["end"], 3),
                         "reason": s["drop"], "text": s["text"]})

    trim_boundary_repeats(kept)
    review = mark_off_script(kept, script_tokens) if script_tokens else []

    # Fillers / stumbles inside kept segments: cut from the end of the previous
    # kept word to the start of the next one. Ranges carry whether each edge sits
    # on a silence (gets padding) or on a word cut (no padding, or it would pull
    # the filler back in).
    keep = []
    for s in kept:
        ranges, cur, cur_pad = [], s["start"], True
        ws = s["words"]
        in_cut = False
        for j, w in enumerate(ws):
            reason = w.get("cut") or ("filler" if norm(w["text"]) in FILLERS else None)
            if not reason:
                in_cut = False
                continue
            nxt = ws[j + 1]["start"] if j + 1 < len(ws) else s["end"]
            if j + 1 < len(ws):
                nxt = snap(nxt)
            if in_cut:
                # consecutive cut words form one cut: extend it, no sliver between
                nxt = max(nxt, cur)
                cuts[-1]["end"] = round(nxt, 3)
                cuts[-1]["text"] += " " + w["text"]
            else:
                # "in uh in": drop the stutter word before the filler too
                first = j - 1 if j > 0 and j + 1 < len(ws) and norm(ws[j - 1]["text"]) == norm(ws[j + 1]["text"]) else j
                cut_from = snap(ws[first - 1]["end"]) if first > 0 else s["start"]
                nxt = max(nxt, cut_from)  # ASR can stamp the next word before the cut point
                ranges.append([cur, cut_from, cur_pad, False])
                cuts.append({"start": round(cut_from, 3), "end": round(nxt, 3), "reason": reason,
                             "text": " ".join(x["text"] for x in ws[first:j + 1])})
            cur, cur_pad, in_cut = nxt, j + 1 >= len(ws), True
        ranges.append([cur, s["end"], cur_pad, True])
        keep.extend(r for r in ranges if r[1] - r[0] > 0.05)

    # Pad silence edges so cuts don't clip consonants; join ranges separated by
    # a pause shorter than max_pause (that pause is natural rhythm).
    padded, prev_end = [], None
    for a, b, pad_a, pad_b in keep:
        b_out = b + pad if pad_b else b
        if padded and a - prev_end <= max_pause:
            padded[-1][1] = b_out
        else:
            padded.append([max(0.0, a - pad) if pad_a else a, b_out])
        prev_end = b
    return [[round(a, 3), round(b, 3)] for a, b in padded], cuts, review


def render(media, keep, out, fps=30, sr=48000):
    """Write the rough cut with picture and sound locked frame-exactly.

    Picture: ONE pass over a constant-frame-rate source, keeping frames by
    index (select) and renumbering them (setpts=N), so output frame k is
    exactly the planned source frame. Do not encode ranges separately and
    concatenate them: per-range `-ss/-t/fps` encodes come out a frame or so
    long, the concat accumulates the surplus, and the picture drifted 11
    frames (367 ms) behind the sound by the end of a 2-minute cut.
    Sound: each range is cut by sample count (with 10 ms fades against
    clicks) and joined as PCM, which is sample-exact.
    The source must be constant frame rate (re-encode phone footage with
    -vf fps=30 first).
    """
    import os
    import tempfile
    frames = [(round(a * fps), round(b * fps)) for a, b in keep]
    sel = "+".join(f"between(n,{fa},{fb - 1})" for fa, fb in frames)
    tmp = tempfile.mkdtemp(prefix="rough-cut-")
    listing = os.path.join(tmp, "list.txt")
    with open(listing, "w") as lf:
        for i, (fa, fb) in enumerate(frames):
            sa, sb = fa * sr // fps, fb * sr // fps
            dur = (sb - sa) / sr
            piece = os.path.join(tmp, f"{i:04d}.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-vn", "-af",
                            f"aresample={sr},atrim=start_sample={sa}:end_sample={sb},asetpts=N/SR/TB,"
                            f"afade=t=in:d=0.01,afade=t=out:st={max(0, dur - 0.01):.4f}:d=0.01",
                            "-c:a", "pcm_s16le", piece], check=True)
            lf.write(f"file '{piece}'\n")
    audio = os.path.join(tmp, "audio.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
                    "-c:a", "pcm_s16le", audio], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", media, "-i", audio, "-filter_complex",
                    f"[0:v]select='{sel}',setpts=N/{fps}/TB[v]", "-map", "[v]", "-map", "1:a",
                    "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-g", str(fps), "-pix_fmt", "yuv420p",
                    "-r", str(fps), "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media")
    ap.add_argument("transcript")
    ap.add_argument("--out", default="edit-plan.json")
    ap.add_argument("--noise-db", type=float, default=-35)
    ap.add_argument("--min-silence", type=float, default=0.35, help="shortest gap that splits takes (s)")
    ap.add_argument("--max-pause", type=float, default=0.45, help="longest pause left in the cut (s)")
    ap.add_argument("--pad", type=float, default=0.12, help="handle kept around speech (s)")
    ap.add_argument("--script", help="VSL script (plain text): catches stumbles ASR can't tell from real words")
    ap.add_argument("--drop", action="append", default=[], metavar="START-END",
                    help="also remove this time range (s), e.g. --drop 264.2-265.4; repeatable")
    ap.add_argument("--render", help="also write a rough-cut MP4 here")
    args = ap.parse_args()

    with open(args.transcript) as f:
        words = json.load(f)
    silences, duration = detect_silences(args.media, args.noise_db, args.min_silence)
    segs = speech_segments(silences, duration)
    if not segs:
        sys.exit("no speech found — check --noise-db")
    assign_words(segs, words)
    script_tokens = None
    if args.script:
        with open(args.script) as f:
            script_tokens = script_tokens_of(f.read())
    keep, cuts, review = plan(segs, args.max_pause, args.pad, script_tokens,
                              snap=load_quiet_finder(args.media))
    for s, e in silences:
        if e - s > args.max_pause and not any(a <= s and e <= b for a, b in keep):
            cuts.append({"start": round(s, 3), "end": round(e, 3), "reason": "dead air", "text": ""})

    for d in args.drop:
        a, b = (float(x) for x in d.split("-"))
        keep = [r for k in keep for r in ([k[0], min(k[1], a)], [max(k[0], b), k[1]]) if r[1] - r[0] > 0.05]
        cuts.append({"start": a, "end": b, "reason": "manual drop", "text": ""})
    kept_len = sum(b - a for a, b in keep)
    result = {"source": args.media, "duration": round(duration, 3),
              "kept_duration": round(kept_len, 3), "keep": keep,
              "cuts": sorted(cuts, key=lambda c: c["start"]),
              "review": review}
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)

    print(f"{duration:.2f}s -> {kept_len:.2f}s ({len(keep)} kept ranges)")
    for c in result["cuts"]:
        print(f"  cut {c['start']:7.2f}-{c['end']:7.2f}  {c['reason']:<30} {c['text']}")
    for r in review:
        print(f"  review {r['start']:6.2f}  said: {r['said']!r:<30} script: {r['script']!r}")
    if args.render:
        render(args.media, keep, args.render)
        print(f"rough cut -> {args.render}")


if __name__ == "__main__":
    main()
