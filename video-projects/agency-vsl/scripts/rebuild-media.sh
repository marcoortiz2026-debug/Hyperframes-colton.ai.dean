#!/bin/bash
# Rebuild this project's gitignored media from the raw footage and render the
# final, reproducing the approved cut exactly (cut points are in cut/edit-plan.json).
#
#   bash scripts/rebuild-media.sh            # media + final render
#   bash scripts/rebuild-media.sh --no-render
#
# Needs: gdown (pip install gdown), ffmpeg, npx hyperframes. ~20 min on 4 cores.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(cd ../.. && pwd)"
RAW_ID="1ksCHf6OdPSXPRmtjMs3rpiEcCUdjZx7y"   # user's Google Drive share of "vsl hvac.MOV"
F=inbox/footage
mkdir -p "$F" assets renders

if [ ! -s "$F/raw-vsl-hvac.mov" ]; then
  tmp=$(mktemp -d)
  (cd "$tmp" && gdown "$RAW_ID")
  mv "$tmp"/*.MOV "$F/raw-vsl-hvac.mov" && rmdir "$tmp"
fi
echo "5ef77d106874538a4741f0817cb0ff48c8ce3ed88706cb213530b3f6b82873e0  $F/raw-vsl-hvac.mov" | sha256sum -c -

# H.264 CFR working copy (same settings as the original pass)
[ -s "$F/raw-vsl-hvac.mp4" ] || ffmpeg -v error -y -i "$F/raw-vsl-hvac.mov" -map 0:v:0 -map 0:a:0 -vf fps=30 \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$F/raw-vsl-hvac.mp4"

# A-roll from the locked cut plan
[ -s assets/a-roll.mp4 ] || python3 -I -c "
import json, sys
sys.path.insert(0, '$ROOT/scripts')
render = __import__('detect-edits').render
render('$F/raw-vsl-hvac.mp4', json.load(open('cut/edit-plan.json'))['keep'], 'assets/a-roll.mp4')"

# Voice (loudness-normalised) and music bed (faded)
[ -s assets/voice.m4a ] || ffmpeg -v error -y -i assets/a-roll.mp4 -vn -af "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 48000 -c:a aac -b:a 192k assets/voice.m4a
[ -s assets/music-bed-mix.m4a ] || ffmpeg -v error -y -i assets/music-bed.mp3 -af "afade=t=in:d=1,afade=t=out:st=118.9:d=4" \
  -c:a aac -b:a 160k assets/music-bed-mix.m4a

echo "a-roll duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/a-roll.mp4)s (approved cut: 123.6s)"
[ "${1:-}" = "--no-render" ] && exit 0
npx hyperframes render --quality high --fps 30 --output "$PWD/renders/hvac-vsl-final.mp4"
