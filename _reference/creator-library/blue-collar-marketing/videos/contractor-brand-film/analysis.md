# contractor-brand-film — @blue-collar-marketing

**Source:** local upload (user-supplied reference; no public URL)
**Duration:** 59.61s
**Aspect:** 16:9
**Resolution:** 1280x720, 23.976fps
**Studied:** 2026-10-14
**Engagement (at time of study):** n/a (local file)
**Sample rate:** every frame at 1fps (60 frames, viewed as timestamped 3x3 contact sheets), plus a 10fps strip of the 3D tracked-text moment (20.8–22.0s). Hard cuts came from ffmpeg scene detection (`cuts.txt`). Music from a spectrogram and level analysis plus a tempo/beat estimate.

**Format:** a **brand film / agency sizzle ad** for an agency serving trades, not a classic talking-head VSL. Two hosts on a job site deliver short lines; drone, FPV and on-site B-roll carry most of the runtime. It matches our 16:9 canvas and the trades niche, but its density is meant for 60 seconds, not a multi-minute VSL.

## Hook (0–2s)
- 0.0s: two hosts walk toward camera on a residential job site, with a worker in the background.
- 0.3–1.5s: the **agency's circular logo badge scales up behind the hosts** (masked behind them), and the frame tints to brand blue as "THIS IS <BRAND>" stacks in white + blue.
- 1.8–3.5s: a **zoom-blur transition** into FPV machinery footage, with the brand name in big blue ALL-CAPS.
- Structure: brand identity first, then credibility (founded year), then scope (where they work).

## Pacing
- Hard cuts: 35 shots, average 1.7s, median 1.2s (range 0.4–6.2s), about 34 cuts/min. Very fast.
- Rough time split: ~28% hosts on camera, ~72% B-roll + motion graphics.
- Shape: brand intro (0–8s) → reach stats (9–18s) → benefits as 1–3 word slams over B-roll (21–37s) → services with UI mockups (41–46s) → closing line (47–49s) → hosts ask (50–55s) → logo end card (56–60s).
- One **deliberate black frame** at 29s, a breath before "from the ground up" (it lines up with a breakdown in the music).

## Captions
- Style: **no subtitles.** Only kinetic keyword slams of 1–4 words.
- Font feel: heavy condensed/wide sans, ALL CAPS. **White + brand blue** two-tone stacks (top line white, key word blue, or the reverse).
- Treatments:
  - **3D-tracked into the footage**: "GROW", "COMPETE" and "WIN MORE BUSINESS" are anchored in the FPV/drone shot and scale up as the camera flies toward them.
  - **Text behind the subject**: "HIRE SKILLED TALENT" in blue sits behind the worker (a depth mask).
  - **Outline → fill**: an outlined word with a blue year inside ("since <year>").
  - **Big stat + flag icon**: "45 STATES" with a US flag and "9 PROVINCES" with a Canadian flag, over drone footage.
  - **Motion-blur slam-in** for "GROUND UP" over the hosts.
- Position: centre or tracked to the scene. Size: huge (20–35% of frame height for single words).

## Scene types
1. 0–1s: hosts walk-and-talk; a logo badge scales in behind them.
2. 2–5s: FPV b-roll of machinery, with a brand-name slam and zoom-blur transitions.
3. 6–7s: hosts, with "SINCE <year>" outline-to-fill.
4. 8–9s: overhead drone b-roll of road and site crews; "BLUE COLLAR BUSINESSES" two-tone.
5. 10–12s: **3D globe** (night-side Earth with city lights) pushing in on North America, with a "across North America" stack.
6. 13–15s: hosts.
7. 16–17s: drone b-roll with **stat callouts** (number + flag + region).
8. 18–28s: an FPV + ground b-roll montage, with 3D-tracked benefit words.
9. 29s: black frame (beat).
10. 30–32s: equipment b-roll → hosts with the "GROUND UP" slam.
11. 33–37s: drone and ground b-roll; "GET MORE LEADS" overhead, "HIRE SKILLED TALENT" behind the subject, "STAND OUT AS AN INDUSTRY LEADER" 3D-tracked.
12. 38–40s: hosts.
13. 41–46s: **service mockups on a blue tech canvas** (a website screenshot sliding past, then a Google search results page with the sponsored ad glowing, a cursor and a highlight box) with a two-line label ("high performing / WEBSITES", "driving leads with / GOOGLE ADS").
14. 47–49s: drone b-roll of a finished lakeside project, with "designed to help you / DOMINATE / your trade".
15. 50–55s: hosts deliver the ask.
16. 56–60s: **white end card**: a "#1 <brand> marketing agency" lockup, then the logo badge + phone + URL, with a music swell and fade.

## Transitions
- Flavors observed: zoom-blur / radial-blur punches (most common), hard cuts, motion-blur whip on text, a black-frame dip, and a fade to white for the end card.
- Rotation: zoom-blur on scene changes into B-roll, hard cuts within a montage.
- Signature: **FPV fly-through with 3D-tracked words.** The camera move *is* the transition.

## Face treatment
- Mode: fullscreen wide two-shot, hosts standing full-body on location. No close-ups.
- Grading: bright, natural daylight, slightly desaturated greens, crisp.
- Camera motion: slow dolly-in on host shots; aggressive FPV and drone on B-roll.
- Framing: centred two-shot, with the job-site action in the background as "proof" in the frame.

## Audio reactivity
- Text pulses on beat: no.
- Background reactivity: no.
- Measured: about 71 BPM (half-time feel), and cuts are **not** beat-aligned (16% of cuts within 80ms of a beat vs 19% chance). The music *structure* matters more: its breakdown sits under the 29s black frame, and a swell carries the end card.

## Audio (music + SFX)
- Music: a **loud, cinematic/hype bed** with heavy bass sections. It's the most prominent music of the three references, and it drops out briefly (27–30s) for the breakdown, then re-enters.
- SFX: whoosh/impact on zoom-blur transitions (broadband transients at the hook and section starts); a bass swell under the end card, then a fade.

## Palette
- `#2f80d8`: brand blue (key words, logo, tint wash; dominant accent)
- `#ffffff`: text + end card
- `#0a1a33`: dark tech-blue canvas for the UI mockups
- warm natural footage tones (yellow machinery `#e0a419`, dirt browns)

## Signature move
**Benefit words physically placed inside the job-site footage** (3D-tracked into the FPV/drone shots, or masked behind workers), so the claims feel like part of the trade's world rather than an overlay.

## What to steal (actionable for Hyperframes builds)
- **UI mockup cards on a dark brand canvas** for services ("websites" / "Google Ads" / "booked calls"): a screenshot card sliding in with motion blur, a highlight box on the important element, a cursor, and a two-line label (small lead-in + huge keyword). Direct fit for showing an HVAC client's ad or booking dashboard.
- **Stat + icon callouts** (huge number, small unit word, icon/flag) for reach or results numbers ("120 HVAC companies", "38 states").
- **Two-tone keyword slams** (white + brand blue, 1–4 words) over B-roll for benefit lists. Use for B-roll passages, not the talking head.
- **Text behind the subject** as an occasional premium move, if we have a person-segmentation matte (`npx hyperframes remove-background` can generate one).
- **Black-frame breath** before a key statement, aligned to a music dip.
- **Logo end card** with phone + URL, held 3–4s with a music swell.
- **Zoom-blur transitions** into B-roll sections (`cinematic-zoom` registry block, or a CSS radial blur).

## What's creator-specific (don't copy literally)
- Their brand name, logo badge, slogan and phone/URL. Their "#1 agency" claim.
- The 34-cuts-per-minute density. It works for a 60s sizzle, but in a multi-minute VSL it would bury the speaker. Use the density only in short montage passages.
- FPV and drone footage needs real HVAC B-roll (job sites, rooftop units, vans). Without it, use licensed stock or skip the move.

## Transcript
See `transcript.json` in this folder (Whisper small.en). The hosts' lines are sparse; much of the runtime is music under B-roll.
