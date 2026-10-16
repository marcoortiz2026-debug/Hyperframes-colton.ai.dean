#!/usr/bin/env python3
"""Dump a 10ms RMS envelope (dBFS) of a source's audio to a .npy-free JSON for cut-point work."""
import json, math, struct, subprocess, sys
src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
x = struct.unpack("<%dh" % (len(raw) // 2), raw)
hop = 160
db = []
for i in range(0, len(x) - hop, hop):
    r = math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) / 32768
    db.append(round(20 * math.log10(max(r, 1e-6)), 1))
json.dump(db, open(out, "w"))
