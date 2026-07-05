# Construction system

What makes a set feel *designed* rather than a generic set tinted with brand colours. Every style's `construction` object holds these; they are (1) folded into the generation prompt and (2) the QA checklist after slicing. Bitmap generation only **approximates** them — pixel-exact enforcement needs a vector normalisation pass.

## Universal (every style)

- **grid** — one keyline grid; consistent live area (~80%) and padding; optical sizing (a circle icon drawn slightly larger than a square so it reads the same size).
- **angles** — geometry constrained to a fixed angle set (e.g. 45° increments), no random slants.
- **detail_budget** — one core idea per icon, a capped element count, matched abstraction across the whole set.
- **shared_parts** — reuse one canonical sub-shape per recurring concept (the same person head, the same plus, the same frame). A strong "same hand" cue.
- **perspective** — one shared viewpoint (flat front, or one isometric angle).
- **shadow** — no shadow cast on the background (keeps cutout clean); internal form shading is per-style.
- **motif** — optional recurring signature element (a spark, a dot, a corner cut). Brand sets should set one; it is what makes a set unmistakably theirs.
- **weight_hierarchy** — the style's *defining element* (the stroke in line styles, the solid silhouette in filled) stays the visually heaviest; every accent / fill / detail is calibrated to sit *below* it in weight. See **Visual weight & accents** below.

## Style-specific

- **stroke** — weight + caps + joins. Only for stroke-based styles (line, cartoon outline, sticker border); `null` for pure fill.
- **corner_radius** — one radius language across the set.
- **fill_rule** — outline / single solid / colour-block / duotone / 3D material / photoreal.
- **color_rule** — how colour is applied: single colour, locked palette, one semantic accent, or duotone. Duotone needs **value contrast** — two close values mush together; use a light and a dark, or clearly different hues. An accent must stay lighter and smaller than the defining element — see **Visual weight & accents**.

## Visual weight & accents

Every icon has a **defining element** — the thing that carries the style: the stroke in line / outline styles, the solid silhouette in filled styles, the outline in cartoon. It must stay the visually **heaviest** element. Any secondary element (an accent fill, a second tone, a detail) is calibrated to sit *below* it in weight, or the icon stops reading as its style.

**Visual weight ≈ value contrast (vs the background) × area × saturation.** An accent that is dark AND large AND saturated has high weight; drop it into a delicate line icon and the hierarchy inverts — the accent dominates and the linework becomes a thin frame around a heavy block.

Calibrate:
- The **lighter / thinner the defining element, the lighter and smaller the accent** must be. A thin line carries only a light, small accent; a heavy filled style can carry a darker one.
- Prefer an accent **clearly lighter in value** than the defining element — a tint / pastel / reduced-opacity wash over a **small-to-medium** area. A whisper you notice second, not a block you notice first.

**Richness lever** — what makes a library-grade set rather than a generic flat one: an accent can carry a **soft gradient or subtle material** instead of a flat solid. This adds depth and a premium feel that sets the library apart, and a light-to-lighter gradient also reads *lighter* than a flat fill, helping the accent stay subordinate. Keep it subtle and consistent across the set, and match it to the brand (a deliberately flat, minimal brand may want none).

## How it is used

1. **Prompt** — append the construction fields to the style preamble so generation follows them.
2. **QA** — after slicing, check the whole set against the construction: uniform stroke, consistent radius, matched detail level, shared parts reused, motif present, one perspective, and no accent out-weighting the defining element.

## Ceiling

Bitmap generation cannot guarantee pixel-exact stroke or radius — treat construction as prompt guidance plus a QA rubric. For a strict system, add a vector step (trace, then normalise stroke / radius / grid).
