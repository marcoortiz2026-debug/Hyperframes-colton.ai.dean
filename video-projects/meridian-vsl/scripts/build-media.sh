#!/bin/bash
# Rebuild the gitignored media for meridian-vsl from the two source takes.
#
#   bash scripts/build-media.sh
#
# Source takes (Jordan's Google Drive shares; NOTE the share links were swapped:
# the "3:20 AM" link downloads the 3:45 file and vice versa, so match by filename):
#   inbox/footage/take1-0320.src.mp4  = "Recording - Oct 16, 2026 - 3_20 AM.mp4"
#   inbox/footage/take2-0345.src.mp4  = "Recording - Oct 16, 2026 - 3_45 AM.mp4"
#
# To drop in a re-recorded CTA: put the clip at inbox/footage/cta-v2.mp4 (30 fps CFR),
# point the "cta" entry of scripts/plan-cut.py at it, rerun this script and
# scripts/build-captions.py after transcribing the new assets/cta.mp4.
set -euo pipefail
cd "$(dirname "$0")/.."
for t in take1-0320 take2-0345; do
  [ -s cut/$t.env.json ] || python3 -I scripts/envelope.py inbox/footage/$t.src.mp4 cut/$t.env.json
done
python3 -I scripts/plan-cut.py
python3 -I scripts/render-cut.py
python3 -I scripts/verify-sync.py keep assets/a-roll.mp4 | tail -2
python3 -I scripts/verify-sync.py cta assets/cta.mp4 | tail -2

BODY=$(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/a-roll.mp4)
CTA=$(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/cta.mp4)
TOTAL=$(python3 -c "print(round($BODY + $CTA + 4.6, 2))")

# Voice: body + CTA as one track, one loudness pass (sample-exact concat, no gap)
ffmpeg -v error -y -i assets/a-roll.mp4 -i assets/cta.mp4 -filter_complex \
  "[0:a][1:a]concat=n=2:v=0:a=1,highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11[a]" -map "[a]" \
  -ar 48000 -c:a aac -b:a 192k assets/voice.m4a

# Music: the 122.9 s bed, looped once with a 3 s crossfade, faded out over the end card
ffmpeg -v error -y -i assets/music-bed.mp3 -i assets/music-bed.mp3 -filter_complex \
  "[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri,atrim=0:$TOTAL,afade=t=in:d=1.5,afade=t=out:st=$(python3 -c "print($TOTAL - 4)"):d=4[a]" \
  -map "[a]" -c:a aac -b:a 160k assets/music-bed-mix.m4a
echo "body ${BODY}s + cta ${CTA}s -> composition ${TOTAL}s"
