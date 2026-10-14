# @agency-vsl-blend — Style Fingerprint

A blend of three agency reference videos, mapped onto this workspace's VSL format: 16:9, raw face-cam footage that we cut, an HVAC agency offer, and the dark + blue brand. Last distilled: 2026-10-14.

| Ref | Analysis | Weight | Why |
| --- | --- | --- | --- |
| A | [`kll-digital/…/window-company-calendar-vsl`](../kll-digital/videos/window-company-calendar-vsl/analysis.md) | **Primary** | Same buyer (home-services owners), same promise (booked appointments), desk face-cam, proof-heavy. Its structure is the template. |
| B | [`ai-business-alongside-career/…/ai-business-roadmap-vsl`](../ai-business-alongside-career/videos/ai-business-roadmap-vsl/analysis.md) | Secondary | Process explanation (roadmap), hook caption treatment, sticker accents. It's vertical, so adapt the layouts. |
| C | [`blue-collar-marketing/…/contractor-brand-film`](../blue-collar-marketing/videos/contractor-brand-film/analysis.md) | Accent | Trades credibility: UI mockups for services, stat callouts, keyword slams over B-roll, end card. A 60s sizzle, so its density applies to short passages only. |

**Precedence reminder:** `CREATOR.md` > `PREFERENCES.md` > this file > `MOTION_PHILOSOPHY.md`. Where a reference conflicts with the user's stated taste, the conflict is called out below and the user's taste wins.

## Consistent across all three (the core of the style)
- **Visuals sync to the speech, not the music.** Measured on B and C: cut-to-beat alignment is no better than chance. Graphics land on the spoken word: counters finish on the number, checklist items appear per word, keyword slams match the phrase.
- **Every proof or process claim gets a visual.** Numbers become stat cards or callouts, processes become a roadmap or checklist, and services become UI mockups. Nothing is decorative (this matches PREFERENCES: "every animation must reinforce what's being said").
- **Hard cuts are the default edit.** Stylised transitions (zoom-blur, swirl, light leak, whip) mark **section changes** only. *Overrides MOTION_PHILOSOPHY's "never hard cuts" for this VSL style.*
- **A continuous music bed under the voice, never silent.** Mix levels differ (A: low corporate bed; B: upbeat 120-ish BPM bed; C: loud cinematic). SFX are sparse and sit on transitions and reveals.
- **The CTA section is visually calm.** The talking head carries the ask, with one persistent CTA element (A: a "BOOK NOW" pill; B: a form-icon sticker; C: a logo end card with contact details).
- **Two-tone semantic colour.** One colour for positive/target/benefit, one for pain/problem (A: gold/red; B: coral/red; C: white/blue).

## Where they differ (choose per section)
| Dimension | A (primary) | B | C | **Use for our VSL** |
| --- | --- | --- | --- | --- |
| Cut rate | ~6 hard cuts/min + slow push-ins | ~14/min | ~34/min | **8–14/min overall.** A-style calm in the offer and CTA; B-style in the hook and process; C-style bursts only in short B-roll montages. |
| Captions | Hook-only keyword phrases | Continuous phrase captions | Keyword slams only | **Continuous captions** (PREFERENCES: "animated captions throughout, key words highlighted in brand accent"), plus A/C-style **keyword slams** for the biggest claims. |
| Talking-head share | ~66% | ~56% | ~28% | **~60–70%**: the talking head is the anchor (CREATOR.md: face-cam is the anchor). |
| Zooms | Slow push-in (~12% over 2s) | Medium↔tight crop per sentence | Slow dolly on hosts | **Both:** a crop alternation at sentence cuts (which also hides the jump cuts from our rough cut) plus slow push-ins on key lines. |
| B-roll | Stock triptych story | Stock + illustration + macro | FPV/drone job sites | Real or stock **HVAC B-roll** (technicians, rooftop units, a homeowner on the phone, a booked calendar); triptych for the "picture your customer" moment. |
| Graphics canvas | Black + red glow, glass cards | Navy roadmap | Tech-blue UI canvas | **One canvas in brand tokens:** `--brand-bg #0a0a0f` + an accent glow `--brand-accent-glow`, glass cards on `--brand-surface`. |

## Signature moves to use (ranked by Hyperframes copy-ability)
1. **Glass stat card with a counter that lands on the spoken number** (A). One reusable sub-composition: name chip, subtitle, counter, optional area chart, optional "jobs booked" pill. GSAP counter with `snap: {innerText: 1}`, `ease: "power2.out"`, ending on the word timestamp from the A-roll transcript. Card enters with a slight 3D tilt and a slow float. Use it for every case study and result.
2. **Before/after card pair** (A): "Without us" animates, then "With us" slides in beside it and overtakes. Use for missed calls vs booked jobs, or revenue before vs after.
3. **Keyword captions in two semantic colours with an icon tile** (A): benefit in `--brand-accent #3b82f6` with a glow, pain in `--brand-warn #ef4444` with a glow; the phrase builds word by word and clears between phrases.
4. **Process roadmap with a camera track** (B): one horizontal 16:9 road/timeline sub-composition with numbered nodes. Tween the container to each node when the speaker reaches that step, and revisit it between talking-head cuts. Use for "how we fill your schedule: steps 1–4".
5. **UI mockup on a dark brand canvas** (C): an ads, booking dashboard or CRM screenshot card sliding in with motion blur, a highlight box and cursor on the key element, and a two-line label (small lead-in + huge keyword).
6. **Stat + icon callouts** (C): a huge number, a small unit word and an icon, for reach or volume claims.
7. **Slow push-in on emphasis lines + crop alternation between sentences** (A+B). The wrapper scales 1.0→1.12 over ~2s; the crop alternates 1.0/1.15 at cut points.
8. **Icon checklist side panel** (A): the speaker shifts left and a list builds on the right, one item per spoken word. Use for "what you get on the call" or "what's included".
9. **Notification-pill marquee** (A) for "we work with N HVAC companies" social proof.
10. **Persistent CTA pill** with a down-arrow chip for the final 6–10s (A), optionally a brand end card (C).
11. **Stylised transitions only at section boundaries:** `cinematic-zoom` / `whip-pan` / `light-leak` / `swirl-vortex` registry blocks. Hard cuts otherwise.
12. **3D icon stickers on key nouns** (B), about 1 every 10–15s at most, so it doesn't get cartoonish for a B2B buyer.

## Section map for a typical HVAC agency VSL (default; adjust to the script)
| Section | Visual treatment |
| --- | --- |
| Hook (0–10s) | Settle-in zoom on frame 1. Qualifier phrase in accent, pain phrase in warn red, both with icon tiles. Captions on. One crop change every ~2–3s. |
| Problem / insight | B-roll story (triptych or 2–3 stock shots) with small centred phrases; return to the talking head with a push-in. |
| Credibility | Brand lower-third (our own design, in brand tokens) on first self-introduction; notification marquee for the client count. |
| Process / mechanism | Roadmap camera-track graphic, revisited per step; UI mockups for the tools named (ads, booking, follow-up). |
| Proof / case studies | **Densest section.** Stat cards → chart cards → before/after pair, one card per number spoken. A section transition into and out of it. |
| Offer | Mostly talking head; icon checklist panel for deliverables. |
| Disqualifiers / urgency | Plain talking head, slow push-in; captions only. |
| CTA | Persistent CTA pill (+ optional end card). Calm, no new graphics. |

## Audio recipe
- Music: a continuous bed, ducked to sit roughly 12–16 dB under the voice. Corporate/modern for the body; it may lift in the proof section and should resolve at the end card. Never fully silent.
- SFX (from `assets/sfx/`, per PREFERENCES: "subtle, never carrying the video"): whoosh on section transitions, soft click/pop on card entries and checklist items, a light tick on counter landings, a low impact on frame 1. No SFX on ordinary hard cuts.

## Don't copy
- Any reference's script, offer, guarantee wording, client names or figures. **Learn the structure only.**
- Their palettes (red/gold, copper/navy, their brand blue): always re-skin in `assets/brand-tokens.css`.
- Their logos, lower-third designs, "#1 agency" claims, phone/URL end cards.
- C's 34-cuts/min density across a whole VSL; B's vertical layouts as-is.
- B's unproofread ASR captions: **always proofread captions against the user's script.**

## Videos studied
- [window-company-calendar-vsl](../kll-digital/videos/window-company-calendar-vsl/analysis.md): desk VSL; glass stat-card proof system (primary template)
- [ai-business-roadmap-vsl](../ai-business-alongside-career/videos/ai-business-roadmap-vsl/analysis.md): vertical VSL; roadmap camera-track + mixed-type hook captions
- [contractor-brand-film](../blue-collar-marketing/videos/contractor-brand-film/analysis.md): trades-agency brand film; 3D-tracked slams, UI mockups, end card
