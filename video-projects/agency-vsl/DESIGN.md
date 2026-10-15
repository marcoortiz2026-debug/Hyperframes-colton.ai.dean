# DESIGN: HVAC pre-call VSL

## Style Prompt
A credible, premium direct-response VSL. The speaker on camera is the anchor. Graphics are lit, not decorated: a near-black canvas, one electric-blue accent glow, glass cards with a thin bright edge, big confident numbers. Motion is snappy and purposeful: things arrive on the spoken word with a short blur and settle, then hold. Style source: `@agency-vsl-blend` (stat cards with counters that land on the spoken number, split-panel lists, UI mockups, hard cuts on the talking head, stylised transitions only into and out of graphic sections), re-skinned in this brand.

## Colors
| Token | Hex | Role |
|---|---|---|
| `--bg` | `#0a0a0f` | Graphics canvas, panels |
| `--surface` | `#141a26` | Glass cards (with a white 6–9% gradient + a 1px `rgba(255,255,255,.14)` edge) |
| `--accent` | `#3b82f6` | Benefit / result / "with us". Glows, card edges, highlights |
| `--accent-text` | `#7cb4ff` | Accent-coloured *text* (a lighter tint of the accent so it passes contrast on dark) |
| `--warn` | `#ef4444` | Pain / the old way (alternatives, X stamps) only |
| `--text` | `#ffffff` | Primary text; numbers use a white→`#cfe0ff` vertical gradient + blue halo |
| `--text-dim` | `#a9b4c7` | Labels, secondary lines |

Five hues, each with one meaning. No other colours.

## Typography
- **Inter** for everything (brand font). Captions 800 at 74px. Numbers 900, `tabular-nums`. Labels 700, uppercase, +0.06em tracking.
- **Phone-first sizes** (the audience watches 16:9 on a phone): numbers ≥ 110px, card titles ≥ 54px, labels ≥ 34px. No text under 30px anywhere.

## Motion
- Entrances: 0.25–0.5s, from blur(10–16px) + y/scale offset, `expo.out` / `power3.out` / `back.out(1.6)` (at least 3 eases per scene).
- Counters land on the spoken number (`power2.out`, snapped integers).
- Graphic sections enter and exit with a fast zoom-blur (0.3s) + whoosh; talking-head joins are hard cuts that alternate the framing (wide / tight / offset), as in the references.
- Ambient: canvas glow breathes, grid drifts, and cards float ±4px. Nothing is fully static.
- Texture: subtle grain on everything, and a vignette on graphics and the camera.

## What NOT to Do
- No name, business name, logo, or name lower-third (user rule; see `PREFERENCES.md`).
- No full-screen or half-screen testimonial images: testimonials are compact proof cards (≤ 16% of the frame), above the captions, never over the face.
- No decorative motion: every graphic maps to a spoken claim, number, step, or contrast.
- No third-party logos (Angi, HomeAdvisor, Facebook, Instagram). Names as text only.
- No flat linear full-screen gradients (H.264 banding); use solid + radial glow.
