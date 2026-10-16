#!/usr/bin/env python3
"""Render cut/edit-plan.json to assets/a-roll.mp4 (body) and assets/cta.mp4 with
picture and sound locked frame-exactly, across both source takes.

Picture: every piece is its own input, opened with an input seek to HALF a
frame before its first frame (sources are true CFR 30 fps with pts = n/30, so
the first decoded frame is exactly frame f0), trimmed to exactly f1-f0 frames
and joined with the concat filter in ONE encode. No per-piece encodes, no fps
filter, nothing that can add or drop a frame.
Sound: each piece is cut from the source by sample count (44.1 kHz = 1470
samples per frame, so piece k is exactly (f1-f0)*1470 samples), 8 ms fades
against clicks, joined as PCM. Afterwards verify with scripts/verify-sync.py.

    python3 scripts/render-cut.py [keep|cta]
"""
import json, os, subprocess, sys, tempfile

plan = json.load(open("cut/edit-plan.json"))
FPS, SR = plan["fps"], 44100
SPF = SR // FPS


def render(pieces, out):
    tmp = tempfile.mkdtemp(prefix="mer-cut-", dir=os.environ.get("TMPDIR", "/tmp"))
    listing = os.path.join(tmp, "list.txt")
    with open(listing, "w") as lf:
        for i, p in enumerate(pieces):
            src = plan["sources"][p["src"]]
            sa, sb = p["f0"] * SPF, p["f1"] * SPF
            dur = (sb - sa) / SR
            wav = os.path.join(tmp, f"{i:03d}.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-af",
                            f"atrim=start_sample={sa}:end_sample={sb},asetpts=N/SR/TB,"
                            f"afade=t=in:d=0.008,afade=t=out:st={dur - 0.008:.4f}:d=0.008",
                            "-ar", str(SR), "-c:a", "pcm_s16le", wav], check=True)
            lf.write(f"file '{wav}'\n")
    audio = os.path.join(tmp, "audio.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
                    "-c:a", "pcm_s16le", audio], check=True)
    args, fl = ["ffmpeg", "-v", "error", "-y"], []
    for i, p in enumerate(pieces):
        args += ["-ss", f"{(p['f0'] - 0.5) / FPS:.6f}", "-i", plan["sources"][p["src"]]] if p["f0"] else \
                ["-i", plan["sources"][p["src"]]]
        fl.append(f"[{i}:v]trim=end_frame={p['f1'] - p['f0']},setpts=PTS-STARTPTS[v{i}]")
    n = len(pieces)
    fl.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,setpts=N/{FPS}/TB[v]")
    args += ["-i", audio, "-filter_complex", ";".join(fl), "-map", "[v]", "-map", f"{n}:a",
             "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-g", str(FPS), "-pix_fmt", "yuv420p",
             "-fps_mode", "passthrough", "-video_track_timescale", "15360", "-c:a", "aac", "-b:a", "256k",
             "-movflags", "+faststart", out]
    subprocess.run(args, check=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    total = sum(p["f1"] - p["f0"] for p in pieces)
    got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"{out}: planned {total} frames ({total / FPS:.3f}s), got {got}")


which = sys.argv[1:] or ["keep", "cta"]
if "keep" in which:
    render(plan["keep"], "assets/a-roll.mp4")
if "cta" in which:
    render(plan["cta"], "assets/cta.mp4")
