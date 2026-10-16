#!/usr/bin/env python3
"""Darken the room behind the speaker, frame by frame, keeping every frame.

Person segmentation (MediaPipe selfie_multiclass) gives a per-pixel
background probability; the mask is feathered and temporally smoothed so
edges (hair, shoulders) do not shimmer, and the background is multiplied
down to BG_GAIN. Output has exactly the input's frames (pipe in, pipe out,
same fps, -fps_mode passthrough) and the input's audio stream copied, so
picture-to-sound timing is untouched; re-run verify-sync afterwards anyway.

    python3 scripts/darken-bg.py IN.mp4 OUT.mp4 [--preview T1,T2,...]
"""
import subprocess, sys
import cv2, numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

MODEL = "../../.cache/models/selfie_multiclass.tflite"
BG_GAIN = 0.22        # wall drops to ~22% brightness, close to the near-black HVAC room
FEATHER = 9           # px blur of the mask at 1080p
SMOOTH = 0.6          # temporal EMA on the mask
W, H = 1920, 1080

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODEL), output_confidence_masks=True))


def person_mask(rgb):
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    bg = r.confidence_masks[0].numpy_view()
    m = 1.0 - cv2.resize(bg, (W, H), interpolation=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(np.clip((m - 0.15) / 0.7, 0, 1), (0, 0), FEATHER)
    return m


def apply(rgb, m):
    g = (BG_GAIN + (1 - BG_GAIN) * m)[..., None]
    return np.clip(rgb.astype(np.float32) * g + 0.5, 0, 255).astype(np.uint8)


src, out = sys.argv[1], sys.argv[2]
if len(sys.argv) > 3 and sys.argv[3] == "--preview":
    for t in sys.argv[4].split(","):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", src, "-frames:v", "1", "-f", "rawvideo",
                              "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        rgb = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
        res = apply(rgb, person_mask(rgb))
        cv2.imwrite(f"{out}-{t}.jpg", cv2.cvtColor(np.hstack([rgb, res])[::2, ::2], cv2.COLOR_RGB2BGR))
    sys.exit()

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
                        "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                        "-g", "30", "-pix_fmt", "yuv420p", "-fps_mode", "passthrough", "-c:a", "copy",
                        "-movflags", "+faststart", out], stdin=subprocess.PIPE)
prev, n = None, 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    rgb = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    m = person_mask(rgb)
    # temporal smoothing, but never across a cut (big mask change = new shot)
    if prev is not None and np.abs(m - prev).mean() < 0.08:
        m = SMOOTH * prev + (1 - SMOOTH) * m
    prev = m
    enc.stdin.write(apply(rgb, m).tobytes())
    n += 1
enc.stdin.close(); enc.wait()
print(f"{out}: {n} frames")
