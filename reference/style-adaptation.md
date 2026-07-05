# Matching a project's / brand's style

The common image path (gpt-image via Codex / OpenAI) is text-only — it cannot take a reference image, so **you** are the bridge: read the brand, translate it into a text style-spec + hex palette. (If your provider does accept a reference image, you may also anchor with an approved sheet — but the text spec is what keeps every batch consistent.) Three ways in; all produce the same frozen spec.

## A. Derive from the project's design tokens / assets (recommended)

1. Find the design tokens: theme CSS variables, tailwind/theme config, a design-system file, or existing icons and screenshots.
2. Extract:
   - **Palette** — the real hex values (background, foreground, primary, accent). Convert HSL or other formats to hex. If only images are available, sample the dominant colours.
   - **Shape language** — line vs fill, stroke weight, corner radius, geometric vs organic.
   - **Mood / finish** — flat / duotone / 3D / hand-drawn; calm vs energetic; warm vs cool.
3. Pick the closest built-in as a base, then override its `palette` and `preamble` to match. Lock the extracted hex.
4. Add a **construction system** (grid, stroke, corner radius, terminal style, detail budget) and, ideally, a **brand motif** that recurs across every icon. This — not the colour — is what makes a set feel designed and brand-specific rather than generic-tinted. Calibrate any accent by **visual weight** — keep it lighter and smaller than the defining element (a thin line carries only a light, small accent), and consider a soft gradient / material for a library-grade feel; see `reference/construction.md` → Visual weight & accents.

## B. Adapt a built-in preset

The user picks the closest built-in and gives a tweak ("our blue is #1A73E8, rounder corners"). Merge it into the preset spec.

## C. Describe from scratch

The user describes the look in words. Draft a spec, generate one small board, iterate the preamble.

## Freeze it

Save the result with the same fields as `styles/<name>.json`. Every future batch reuses it verbatim → consistent output. Keep project-specific specs **outside** this skill — they are cases, not part of the general library.

## Scope

Generated raster icons suit spot / feature / marketing / card-header placements. Keep dense functional UI on a vector icon library; match the style anyway so the two families feel related.
