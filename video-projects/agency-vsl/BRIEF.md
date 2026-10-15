# agency-vsl: HVAC pre-call VSL

## Audience and context
- **Who:** HVAC contractors who were cold-called and **already booked** onto a sales call.
- **When/where:** they watch after booking, **on their phone** (16:9 video, so it plays small in portrait or fills the screen in landscape).
- **Job of the video:** show-up and pre-sell. It builds belief (results, risk reversal, how it works) so they attend the call ready to buy. **It is not a cold ad.** There's no "book now" button: the appointment already exists.
- **CTA:** "make sure you don't miss our call". End on a calm reminder, not a booking prompt.

## Constraints
- **No name, business name, logo, or name lower-third anywhere** (user decision, 2026-10-15; also in `PREFERENCES.md`).
- **Phone-first legibility:** caption and graphic text must be large. Plan for a ~6-inch screen: on-screen numbers ≥ 90px tall at 1080p, captions ≥ 64px, and no fine print.
- Style: `@agency-vsl-blend` (`_reference/creator-library/agency-vsl-blend/style-distilled.md`), re-skinned in brand tokens.

## Source
- `inbox/footage/raw-vsl-hvac.mov`: iPhone 17, 1920x1080, HEVC, 4:28 (gitignored). Working copy: `raw-vsl-hvac.mp4` (H.264, CFR 30).
- `inbox/script/script.txt`: the script, the reference for take selection and caption proofreading.

## Rough cut (locked 2026-10-15): `inbox/footage/a-roll.mp4`, 2:03.6
Produced by:
```bash
cd video-projects/agency-vsl/inbox/footage
python3 ../../../../scripts/detect-edits.py raw-vsl-hvac.mp4 transcript.json \
    --script ../script/script.txt --drop 263.9-267.8 --out edit-plan.json --render a-roll.mp4
```
- Removed: walk-in and walk-out, the 7 flubbed takes (last take kept), the repeated "There's a reason" and "with the results", ~50 pauses tightened to ~0.25s, and the trailing "Let's see what happens".
- Kept as delivered: the speaker's paraphrasing of the script ("Angie, your home advisor, do I even have to mention it?", "without you getting results", "installs and replacements"). His delivery is the source of truth; **captions follow what he says, not the script text.**
- Verified: re-transcribed with both Parakeet and Whisper. No repeated phrases, no pause > 0.45s, 88% of script words present in order (the rest is paraphrase).

## Known footage notes
- The eyeline drifts right (reading) on many lines. Cover the worst stretches with full-screen graphics or B-roll, and use crop changes at cuts.
- Slightly underexposed: lift exposure and shadows in the grade.
- Jump cuts on a locked-off wide shot: alternate wide and tighter crops at cut points (the reference style does this too).
