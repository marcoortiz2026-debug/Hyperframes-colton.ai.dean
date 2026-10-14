# ai-business-roadmap-vsl — @ai-business-alongside-career

**Source:** local upload (user-supplied reference VSL; no public URL). The creator and brand aren't named anywhere on screen or in the audio, so the handle is descriptive.
**Duration:** 66.13s
**Aspect:** 9:16 (vertical)
**Resolution:** 720x1280, 23.976fps
**Studied:** 2026-10-14
**Engagement (at time of study):** n/a (local file)
**Sample rate:** every frame at 1fps (66 frames, viewed as timestamped 3x3 contact sheets), plus a 10fps strip of the opening caption (0.0–1.5s). Hard cuts came from ffmpeg scene detection (`cuts.txt`). Music from a spectrogram and level analysis plus a tempo/beat estimate.

**Format:** vertical paid-social VSL for a done-for-you B2B service. A walk-and-talk hook, then seated face-cam with a process roadmap. It's vertical, so transfer the *techniques* to 16:9 rather than the layouts.

## Hook (0–2s)
- 0.0–0.3s: handheld walk-and-talk down a bright office corridor. The speaker is mid-stride, talking from frame 1.
- 0.0–1.2s: a **mixed-type caption** builds: small bold-sans lead-in words, then one **giant display word** that fades in left to right with a gradient sweep. Then the key noun phrase appears in **coral bold italic** under it.
- 1.3s: hard cut to a new angle, and the caption block swaps for the next phrase, set in a light **italic serif**.
- 2–5s: the "or you don't pay" guarantee clause; its key verb phrase is in **red**, and the next key phrase uses a big coral italic gradient.
- Structure: the offer and guarantee in the first 5s, then a "give me 15 seconds" micro-commitment, then straight into the process.

## Pacing
- Hard cuts: 16 shots, average 4.1s, median 3.7s (range 0.5–8.6s), about 14 cuts/min.
- Hook (0–8s): an angle change every ~1.3–2.5s during the walk-and-talk.
- Rough time split: ~56% talking head, ~44% B-roll or motion graphics.
- Shape: walk-and-talk hook (0–8s) → roadmap steps cut against seated talking head (8–41s) → "your involvement" B-roll (42–57s) → seated CTA (58–66s).

## Captions
- Style: **continuous phrase captions** (2–3 lines, about 4–8 words), present for the whole video, swapped whole at phrase boundaries (no karaoke highlighting).
- Font feel: very heavy wide geometric sans (Clash/Syne-like), white, lowercase-leaning, subtle drop shadow, tight leading.
- Emphasis: only in the hook, by **type contrast**: giant display word, italic serif, coral or red colour. After the hook the captions are uniform white.
- Position: centre to lower-centre (chest height on the talking head, mid-frame on B-roll).
- Size: medium-large for vertical (~3.5% of frame height per line).
- **3D emoji/icon stickers** pop in below the caption on key nouns (a support-agent avatar, cash stacks, an alarm clock, an application form).

## Scene types
1. 0–8s: **talking-head walk-and-talk**, handheld, several angles. Mixed-type kinetic captions.
2. 8–9s: **roadmap intro.** A navy canvas, a winding black road with dashed lane lines, numbered white milestone circles, and phase cards with copper borders and bullet text.
3. 10–12s: **website B-roll.** The service's own site screenshots tilted in 3D perspective, panning with motion blur and a dark/light mix.
4. 13s: **zoom-blur whip** into the seated close-up.
5. 14–16s: seated talking head, tighter.
6. 17–23s: **roadmap, continued.** The camera tracks along the road from milestone 2 to 4, with the matching phase card in focus. A big header ("your path to success") slides past at the top.
7. 24–28s: talking head + 3D sticker pop-ins (an agent avatar, then cash added in for "only paid on what they close").
8. 29–35s: **roadmap, final.** It tracks to milestones 5–6, with a counter-style number flip on a milestone (64 → 6) as the camera passes.
9. 36–41s: talking head.
10. 42–45s: **stock b-roll** of business people reviewing a document, with a **chromatic-aberration / RGB-split** grade.
11. 46–51s: talking head; the medium/tight framing alternates per sentence.
12. 52–54s: a **flat 2D illustration** (an overwhelmed worker at a desk) on a peach background, for "the system was designed around…".
13. 55–57s: **macro stock** of a hand counting bills, with a 3D alarm-clock sticker ("time vs money").
14. 58–66s: seated CTA, with a form/application 3D icon sticker under the caption until the end.

## Transitions
- Flavors observed: hard cut (dominant), zoom-blur whip (13s), motion-blur pans inside graphics, and the camera move along the roadmap as an in-graphic transition between steps.
- Rotation: hard cuts on talking-head angle changes. Graphics enter on a hard cut and move *internally*.
- Signature: **the roadmap camera track.** One continuous graphic revisited three times, each visit advancing along the road to the next step being described.

## Face treatment
- Mode: fullscreen talking head. A walk-and-talk for the hook, then seated for the body.
- Grading: bright, airy, neutral-warm. A light wood shelving background with decor objects.
- Camera motion: handheld in the hook, locked-off when seated, with **medium↔tight crop alternation between sentences** (digital reframe on cut).
- Framing: centred, face in the upper third, so the caption sits on the chest.

## Audio reactivity
- Text pulses on beat: no.
- Background reactivity: no.
- Measured: about 122 BPM, but cuts are **not** beat-aligned (39% of cuts within 80ms of a beat vs 33% chance). Cuts follow the speech phrasing.

## Audio (music + SFX)
- Music: a **rhythmic, upbeat bed** (regular kick-drum pulses visible in the spectrogram, ~122 BPM). It's never silent (the quietest 0.5s window is −23 dBFS), so the bed is mixed relatively hot under the voice.
- SFX: a tonal riser/whoosh into the first roadmap reveal (~6.6–8s). Pop-style hits likely accompany the sticker entries (small transients); subtle.

## Palette
- `#13233f`: roadmap navy (graphics canvas; dominant in graphics)
- `#c98a6a`: copper/peach phase-card borders
- `#f08a7a`: coral emphasis captions
- `#d9334a`: red emphasis (the negated verb)
- `#ffffff`: caption white; set tones are light wood `#d9c3a5`

## Signature move
A **single "path to success" roadmap graphic revisited several times.** The camera advances along a winding road to the next numbered milestone each time the speaker reaches the next step, so a 6-step process reads as one journey.

## What to steal (actionable for Hyperframes builds)
- **Process roadmap with a camera track** for "here's exactly how it works": one wide sub-composition (road SVG path + numbered nodes + phase cards), with a GSAP tween of the container's `x/y/scale` to each milestone, timed to the spoken step and revisited between talking-head cuts. Ideal for an HVAC "how we fill your schedule" 3–5 step process. Use brand navy/blue instead of copper.
- **Hook-only type contrast**: one giant display word per phrase plus an italic serif or accent-colour phrase, then plain captions for the body. Keeps the hook loud and the body readable.
- **3D icon stickers on key nouns** (pop-in with `back.out(2)`, scale 0→1, ~0.25s), sparingly, ~1 every 10s.
- **Website/UI B-roll in 3D perspective** (tilted screenshot, slow pan + motion blur), for "we build you a site / ads / dashboard" claims.
- **Medium↔tight reframe between sentences** on seated talking head (alternate scale 1.0 / 1.18 on the video wrapper at sentence cuts).
- **Walk-and-talk cold open** if the user ever films one: angle change every ~1.5–2s.

## What's creator-specific (don't copy literally)
- Their offer (an AI business alongside a corporate career), guarantee wording and phase text.
- The copper + navy roadmap palette. Re-skin in our brand tokens.
- The vertical layout: in 16:9 the captions go to the lower third, and the roadmap can run horizontally.

## Transcript
See `transcript.json` in this folder (Whisper small.en). Mistranscriptions: "closers" became "clothes are" / "closure" at about 44–46s (the on-screen caption has the same error, so the editor used ASR captions unchecked). **Lesson: always proofread captions against the script.**
