#!/usr/bin/env python3
"""Face centre/size per A-roll piece (median of 5 samples), for camera framing.
Writes assets/faces.js: window.FACES = [{t, cx, cy, h}] in 1920x1080 source px."""
import json, subprocess, sys
import cv2, numpy as np
video, plan_key, offset = sys.argv[1], sys.argv[2], float(sys.argv[3])
plan = json.load(open("cut/edit-plan.json"))
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(video)
out, t = [], 0
for p in plan[plan_key]:
    n = p["f1"] - p["f0"]
    found = []
    for k in np.linspace(t * 30 + 2, t * 30 + n - 3, 5).astype(int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(k))
        ok, im = cap.read()
        if not ok:
            continue
        g = cv2.cvtColor(cv2.resize(im, (960, 540)), cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, 1.1, 6, minSize=(80, 80))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2] * r[3])
            found.append((2 * (x + w / 2), 2 * (y + h / 2), 2 * h))
    cx, cy, h = np.median(found, axis=0) if found else (960, 400, 300)
    out.append({"t": round(offset + t, 3), "cx": int(cx), "cy": int(cy), "h": int(h), "n": len(found)})
    t += n / 30
print(json.dumps(out))
