#!/usr/bin/env python3
"""Turn the approved line list into frame-exact keep ranges (cut/edit-plan.json).

Each line is (source, start, end, start_mode, end_mode) in source seconds, taken
from the word stamps. Modes:
  "edge"  - the boundary sits in a pause: find the real speech onset/offset on
            the loudness envelope and pad it (ASR stamps stretch across pauses).
  "snap"  - the boundary is inside running speech: cut at the quietest 10 ms
            within +-0.12 s of the stamp.
Pauses longer than MAX_PAUSE inside a line are cut down to KEEP_PAUSE.
Times are then rounded outward to whole frames (30 fps); the renderer works in
frame indices only.
"""
import json

FPS = 30
QUIET = -55.0      # dBFS; both takes are gated, room tone sits near -85
MAX_PAUSE = 0.50
KEEP_PAUSE = 0.30
PRE, POST = 0.08, 0.14

SRC = {"T1": "take1-0320", "T2": "take2-0345"}
ENV = {k: json.load(open(f"cut/{v}.env.json")) for k, v in SRC.items()}

# section, source, start, end, start_mode, end_mode, text
LINES = [
    ("hook", "T2", 0.80, 43.36, "edge", "snap", "Contractors, I'm on your side ... past the seven and eight figure range,"),
    ("intro", "T1", 14.96, 18.33, "edge", "edge", "My name is Jordan, owner and founder of Meridian Trades Group."),
    ("intro", "T1", 22.48, 28.64, "edge", "snap", "We work with construction businesses all across the US to help them find more work opportunities and estimates,"),
    ("intro", "T1", 0.56, 14.60, "edge", "edge", "Look, I'm gonna be up front with you ... get along in the first place."),
    ("leadgen", "T1", 74.19, 82.56, "edge", "edge", "And I understand you've probably heard similar claims ... Everybody claims they're different."),
    ("leadgen", "T1", 85.79, 97.23, "edge", "edge", "Everyone claims they can get you more leads ... funny business over here."),
    ("leadgen", "T1", 102.19, 110.67, "edge", "snap", "Because I know if I give you a name ... give me a dispute,"),
    ("leadgen", "T1", 111.79, 122.03, "snap", "edge", "which neither of us want, right? ... for you guys to incorporate."),
    ("fit", "T1", 35.12, 40.16, "edge", "snap", "I am not going to sit here and guarantee you that we're gonna make you a millionaire overnight,"),
    ("fit", "T2", 151.16, 164.60, "edge", "edge", "but what I am gonna guarantee you is ... make a lot of money together."),
    ("numbers", "T1", 146.40, 150.00, "edge", "snap", "That's why I personally believe that results should speak for themselves."),
    ("numbers", "T2", 199.95, 210.43, "edge", "edge", "Because you shouldn't have to buy into a pitch ... execute from what we tell you."),
    ("notfor", "T2", 217.59, 226.55, "edge", "edge", "Because we're not the right fit for everyone ... I'm sorry, we're not the one."),
    ("notfor", "T1", 180.72, 188.97, "edge", "edge", "We're not gonna close for you ... you will have it in abundance."),
    ("call", "T1", 199.53, 209.37, "edge", "edge", "When you book a call, we're gonna break down ... worked with in the past."),
    ("call", "T1", 227.13, 245.18, "edge", "edge", "I'm a straight guy ... if the numbers don't make sense."),
]
CTA = [("cta", "T1", 289.18, 306.70, "edge", "edge", "So if you're serious about scaling ... scale you guys up. [PLACEHOLDER - to be replaced by re-recorded CTA]")]


def frame_of(t):   # envelope index (10 ms)
    return int(round(t * 100))


def quiet(env, i):
    """Below the gate threshold, ignoring loud blips under 50 ms (clicks,
    lip smacks) that sit inside silence."""
    if env[i] < QUIET:
        return True
    lo = i
    while lo > 0 and env[lo - 1] >= QUIET and i - lo < 5:
        lo -= 1
    hi = i
    while hi < len(env) - 1 and env[hi + 1] >= QUIET and hi - i < 5:
        hi += 1
    return hi - lo + 1 < 5


def quiet_runs(env, a, b, min_len):
    """(start, end) of quiet runs of at least min_len s inside [a, b], in s."""
    out, i = [], None
    for k in range(frame_of(a), frame_of(b) + 1):
        if quiet(env, k):
            i = k if i is None else i
        else:
            if i is not None and (k - i) / 100 >= min_len:
                out.append((i / 100, k / 100))
            i = None
    if i is not None and (frame_of(b) + 1 - i) / 100 >= min_len:
        out.append((i / 100, (frame_of(b) + 1) / 100))
    return out


def onset(env, t):
    """Speech onset for a line whose first word is stamped at t: the end of
    the quiet run (>= 80 ms) nearest t, within +-0.5 s. ASR start stamps run
    early or late by a few hundred ms."""
    runs = [r for r in quiet_runs(env, t - 0.8, t + 0.5, 0.08) if abs(r[1] - t) <= 0.5]
    if not runs:
        return snap(env, t)
    return min(runs, key=lambda r: abs(r[1] - t))[1] - PRE


def offset(env, t):
    """Speech offset after the last word (stamped at t): start of the first
    quiet run of 150 ms or more."""
    j = frame_of(t)
    while j < len(env) - 15 and not all(quiet(env, k) for k in range(j, j + 15)):
        j += 1
    return j / 100 + POST


def snap(env, t, w=0.12):
    lo, hi = frame_of(t - w), frame_of(t + w)
    return min(range(lo, hi + 1), key=lambda i: env[i]) / 100


def pauses(env, a, b):
    return [r for r in quiet_runs(env, a, b, MAX_PAUSE) if a < r[0] and r[1] < b]


def build(lines):
    keep = []
    for sec, src, a, b, ma, mb, text in lines:
        env = ENV[src]
        s = onset(env, a) if ma == "edge" else snap(env, a)
        # for edge ends, b is the start of the last word
        e = offset(env, b) if mb == "edge" else snap(env, b)
        parts, cur = [], s
        for pa, pb in pauses(env, s + 0.05, e - 0.05):
            half = KEEP_PAUSE / 2
            parts.append((cur, pa + half))
            cur = pb - half
        parts.append((cur, e))
        for k, (x, y) in enumerate(parts):
            fa, fb = int(x * FPS), -int(-y * FPS)    # floor / ceil to frames
            keep.append({"section": sec, "src": SRC[src], "f0": fa, "f1": fb,
                         "text": text if k == 0 else "(pause tightened)"})
    return keep


plan = {"fps": FPS, "sources": {v: f"inbox/footage/{v}.src.mp4" for v in SRC.values()},
        "keep": build(LINES), "cta": build(CTA)}
json.dump(plan, open("cut/edit-plan.json", "w"), indent=1)
tot = sum(k["f1"] - k["f0"] for k in plan["keep"])
cta = sum(k["f1"] - k["f0"] for k in plan["cta"])
for k in plan["keep"] + plan["cta"]:
    print(f'{k["section"]:8} {k["src"]} {k["f0"]/FPS:7.2f}-{k["f1"]/FPS:7.2f} ({(k["f1"]-k["f0"])/FPS:5.2f}s) {k["text"][:60]}')
print(f"body {tot/FPS:.2f}s + cta {cta/FPS:.2f}s = {(tot+cta)/FPS:.2f}s, {len(plan['keep'])+len(plan['cta'])} pieces")
