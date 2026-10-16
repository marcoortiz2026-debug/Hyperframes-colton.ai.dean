#!/usr/bin/env python3
"""Lip-sync check of a finished render against the original-take cut.

Picture: for every camera shot of the render (between cuts / reframes, skipping
full-screen graphics), the face is located in the render and in the cut
(a-roll + CTA, which verify-sync.py already proved identical to the source
takes). Mouth-region motion (frame-to-frame luma change) is compared between
render and cut over lags of +-6 frames; the best lag must be 0.
Sound: the render's mix is cross-correlated with the cut's original audio in
10 s windows; the lag must be 0 ms. Picture lag 0 + sound lag 0 = lip sync
exactly as recorded.

    python3 scripts/verify-render-sync.py renders/meridian-draft.mp4
"""
import json, re, subprocess, sys
import cv2, numpy as np

render = sys.argv[1]
W, H, FPS = 960, 540, 30


def gray(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W)


def pcm(path, sr=8000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


ref = np.concatenate([gray("assets/a-roll.mp4"), gray("assets/cta.mp4")])
out = gray(render)
html = open("index.html").read()
joins = json.loads(re.search(r"var JOINS = (\[[^\]]*\])", html).group(1))
layout = json.loads(re.search(r"var LAYOUT = (\[.*?\]\]);", html, re.S).group(1).replace('"', '"'))
cam_end = len(ref) / FPS
cuts = sorted(set([0.0] + joins + [t for t, _ in layout]))
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def lay(t):
    l = "cam"
    for a, b in layout:
        if t >= a - 1e-3:
            l = b
    return l


def face_box(frames, idx):
    boxes = []
    for k in idx:
        f = casc.detectMultiScale(frames[k], 1.1, 6, minSize=(70, 70))
        if len(f):
            boxes.append(max(f, key=lambda r: r[2] * r[3]))
    return np.median(boxes, axis=0).astype(int) if boxes else None


def mouth_motion(frames, box, a, b):
    x, y, w, h = box
    mx0, mx1 = x + int(0.2 * w), x + int(0.8 * w)
    my0, my1 = y + int(0.62 * h), min(H, y + int(1.0 * h))
    crop = frames[a:b, my0:my1, mx0:mx1].astype(np.float32)
    m = np.abs(np.diff(crop, axis=0)).mean(axis=(1, 2))
    return (m - m.mean()) / (m.std() + 1e-6)


rows, worst = [], 0
for i, t0 in enumerate(cuts):
    t1 = cuts[i + 1] if i + 1 < len(cuts) else cam_end
    t1 = min(t1, cam_end)
    if lay(t0) == "full" or t1 - t0 < 1.0:
        continue
    a, b = int(round(t0 * FPS)) + 1, int(round(t1 * FPS)) - 1
    samp = np.linspace(a, b - 1, 6).astype(int)
    bo, br = face_box(out, samp), face_box(ref, samp)
    if bo is None or br is None:
        rows.append((t0, t1, None, "face not found"))
        continue
    so, sr_ = mouth_motion(out, bo, a, b), mouth_motion(ref, br, a, b)
    n = len(so)
    sc = {L: float(np.dot(so[max(0, L):n + min(0, L)], sr_[max(0, -L):n - max(0, L)]) / (n - abs(L))) for L in range(-6, 7)}
    best = max(sc, key=sc.get)
    worst = max(worst, abs(best))
    rows.append((t0, t1, best, f"corr {sc[best]:.2f} (lag0 {sc[0]:.2f})"))
for r in rows:
    print(f"shot {r[0]:7.2f}-{r[1]:7.2f}s  picture lag {r[2]} frames  {r[3]}")
print(f"PICTURE: {sum(1 for r in rows if r[2] is not None)} shots checked, worst lag {worst} frames")

# sound
SR = 8000
ro = pcm(render)
rr = np.concatenate([pcm("assets/a-roll.mp4"), pcm("assets/cta.mp4")])
lags = []
for s in range(0, int(cam_end) - 10, 10):
    seg = rr[s * SR:(s + 10) * SR]
    win = ro[s * SR - 400 if s else 0:(s + 10) * SR + 400]
    off = 400 if s else 0
    c = np.correlate(win, seg, mode="valid")
    lags.append((np.argmax(c) - off) / SR * 1000)
print("SOUND: 10 s windows, lag ms:", " ".join(f"{l:+.1f}" for l in lags))
print(f"SOUND: worst lag {max(abs(l) for l in lags):.1f} ms")
