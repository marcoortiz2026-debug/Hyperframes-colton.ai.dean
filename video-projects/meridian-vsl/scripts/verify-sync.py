#!/usr/bin/env python3
"""Check a frame-exact cut against its source takes.

Picture: every output frame is compared (64x36 luma) with the source frame
the plan says it is, and with that frame's +-3 neighbours; any frame whose
best match is not offset 0 is reported. Sound: each piece's audio is
cross-correlated with the source around its planned position; the lag must
be 0 ms. Together that proves picture and sound sit exactly where they did in
the original recording, so lip sync is unchanged by the cut.

    python3 scripts/verify-sync.py keep assets/a-roll.mp4
"""
import json, subprocess, sys
import numpy as np

which, out = sys.argv[1], sys.argv[2]
plan = json.load(open("cut/edit-plan.json"))
FPS, W, H = plan["fps"], 64, 36
pieces = plan[which]


def frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H}:flags=area,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def audio(path, sr=8000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


src_f = {s: frames(p) for s, p in plan["sources"].items() if any(x["src"] == s for x in pieces)}
src_a = {s: audio(plan["sources"][s]) for s in src_f}
of, oa = frames(out), audio(out)
bad, k, worst_lag = [], 0, 0
SR = 8000
for i, p in enumerate(pieces):
    S = src_f[p["src"]]
    for f in range(p["f0"], p["f1"]):
        o = of[k]
        d = {off: np.abs(S[f + off] - o).mean() for off in range(-3, 4) if 0 <= f + off < len(S)}
        best = min(d, key=d.get)
        # identical neighbours (frozen picture) tie; only flag a strictly better neighbour
        if best != 0 and d[best] + 0.3 < d[0]:
            bad.append((k, i, f, best, round(d[0], 2), round(d[best], 2)))
        k += 1
    # audio lag: output piece vs source, +-120 ms search
    a0 = round(sum(x["f1"] - x["f0"] for x in pieces[:i]) / FPS * SR)
    n = round((p["f1"] - p["f0"]) / FPS * SR)
    seg = oa[a0 + 80:a0 + n - 80]
    s0 = round(p["f0"] / FPS * SR) + 80
    ref = src_a[p["src"]]
    lags = range(-960, 961)
    sc = [float(np.dot(seg, ref[s0 + L:s0 + L + len(seg)])) if s0 + L >= 0 else -1e9 for L in lags]
    lag = lags[int(np.argmax(sc))] / SR * 1000
    worst_lag = max(worst_lag, abs(lag))
    print(f"piece {i:2d} {p['src']} frames {p['f0']}-{p['f1']}: audio lag {lag:+.1f} ms")
print(f"output frames {len(of)}, planned {k}; picture mismatches: {len(bad)}; worst audio lag {worst_lag:.1f} ms")
for b in bad[:20]:
    print("  out frame %d (piece %d, src %d): best neighbour %+d (diff %.2f vs %.2f)" % b)
