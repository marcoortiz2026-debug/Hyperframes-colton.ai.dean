# DESIGN: Meridian Trades Group contractor VSL

## Style Prompt
A premium, no-nonsense direct-response VSL for construction contractors. Jordan on camera is the anchor; the graphics are the "receipts": a near-black canvas, one electric-blue accent for what works, one red for the agencies and lead-gen sites that burned the viewer's money. Glass cards with a thin bright edge, heavy confident type, big numbers. Motion is snappy and purposeful, things land on the spoken word with a short blur and settle. The tone is provocative and funny in the hook, then calm and credible. Graphics make the argument visible; they never decorate.

## Colors
| Token | Hex | Role |
|---|---|---|
| `--bg` | `#0a0a0f` | Graphics canvas, panels |
| `--surface` | `#141a26` | Glass cards (white 6–9% gradient + 1px `rgba(255,255,255,.14)` edge) |
| `--accent` | `#3b82f6` | What works / with us / the good news |
| `--accent-text` | `#7cb4ff` | Accent-coloured text on dark |
| `--warn` | `#ef4444` | Bad agencies, lead-gen sites, the bad news, ✕ stamps only |
| `--text` | `#ffffff` | Primary text; numbers use a white→`#cfe0ff` gradient + blue halo |
| `--text-dim` | `#a9b4c7` | Labels, secondary lines |

Ember orange (`#f97316`) appears only inside the "setting it ablaze" burn, as part of the red family.

## Typography
- **Inter** throughout (brand font). Captions 800 at 72px. Numbers 900, `tabular-nums`. Labels 700, uppercase, +0.08em.
- Phone-first sizes (16:9 watched on a phone): numbers ≥ 110px, card titles ≥ 48px, labels ≥ 32px, nothing under 30px.

## Motion
- Entrances 0.25–0.5s from blur(8–18px) + y/x/scale offset; `expo.out`, `power3.out`, `back.out(1.5–2)`; at least 3 eases per scene.
- Talking-head joins are hard cuts that alternate framing (wide / tight / offset), always keeping the face in frame, and always cropping out the purple border baked into both recordings (scale ≥ 1.12).
- Graphic sections: split panel (speaker left, panel right) or full-screen canvas; enter with a fast zoom-blur (≈0.3s) + whoosh, exit with blur-out exactly at a join.
- Ambient: glows breathe, grid drifts, cards float ±6px. Nothing fully static.
- Texture: subtle grain everywhere, vignette on camera and graphics.

## What NOT to Do
- No name, business name, logo, or name lower-third on screen (user rule). Jordan says his name; the screen doesn't.
- No third-party logos (Angie's List, HomeAdvisor, Thumbtack): names as plain text only.
- No claims on screen beyond what is spoken (no invented numbers, results, or testimonials).
- No captions that differ from the audio. The placeholder CTA says "follow the call below" and is captioned that way.
- No flat full-screen linear gradients (H.264 banding); solid + radial glow.
