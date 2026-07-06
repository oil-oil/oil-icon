---
name: oil-icon
description: Generate a cohesive set of transparent-background icons in a chosen or brand-matched visual style. Use when the user wants custom icons, an icon pack / set, system icons, spot / feature / category icons, or icons matching a specific look (line, filled, colorblock, cartoon, isometric, 3D, sticker, realistic, animal badge) or a project's own design tokens. Renders 4x4 sheets via image generation on a flat grey backdrop, then slices and removes backgrounds into clean PNGs. Not for a single one-off icon (draw SVG instead) or dense 16-24px functional UI glyphs (use a vector icon library there).
---

# oil-icon

Generate a **set** of icons that share one visual style, output as transparent PNGs.

Image generation runs on a flat grey backdrop as a 4×4 sheet — 16 icons in one generation, so the set is stylistically consistent by construction — then each cell is sliced out and background-removed.

Claude owns the design decisions (which style, which palette, which metaphors, whether to match a brand); image generation and slicing are mechanical steps.

## When to use / not

Use for: an icon pack, a product or brand icon set, spot / feature / marketing / empty-state / category icons, or icons matching a specific style or a project's design tokens.

Not for: a single one-off icon (draw an SVG), or dense functional UI glyphs at 16–24px (use a vector icon library such as lucide — raster icons are not crisp at tiny sizes). Generated icons are best at larger "spot" sizes.

## Workflow

1. **Choose the style.** Either pick a built-in from `styles/` (table below), or **match the user's brand** by reading their project's design tokens / assets and deriving a custom style-spec — see `reference/style-adaptation.md`. Freeze the result as a style-spec with the same fields as the built-in JSONs; the frozen spec is what keeps every future batch identical.
2. **List the icons.** Write each concept as `name — short concrete metaphor` (e.g. `settlement — a wallet with a coin`). One clear idea per icon; keep the detail level consistent across the set. Batch into sheets of **16**, or **9** when you want maximum slicing stability.
3. **Compose the prompt.** `style.preamble` + the style's `construction` fields (as short guidance) + palette-lock line + numbered metaphors + the fixed composition text — see `reference/prompt-template.md` and `reference/construction.md`.
4. **Generate the sheet(s).** Choose an image provider by capability, in order (see `reference/image-providers.md`) — never assume Codex is present:
   1. **Built-in / host imagegen first** — if the running agent already has a callable image-generation tool, including Codex's built-in `image_gen` tool or the `imagegen` skill, call it directly. Do not delegate to external Codex CLI just to reach imagegen from another process.
   2. **Codex CLI fallback** — only if this agent has no callable image-generation tool, and Codex is available (`~/.claude/skills/codex/scripts/ask_codex.sh` or `codex` on PATH), delegate generation to it.
   3. **External API fallback** — only if neither of the above exists, ask the user which image API + key to use; for OpenAI Images, `scripts/gen_image.py --prompt "…" --out raw/<style>.png` is ready.
   Save or copy each generated sheet to `raw/<style>.png` on flat grey `#808080`. Built-in imagegen may save under `$CODEX_HOME/generated_images/...`; after generation, move or copy the selected PNG into the oil-icon `raw/` folder. One sheet = one generation = one consistent style; a provider only has to turn the prompt into a grey-background PNG.
5. **Slice.** Run `scripts/setup.sh` once, then:
   `.venv/bin/python3 scripts/slice_icons.py <raw>.png <outdir> --mode <cutout> [--thresh N] [--grid 4]`
   using the style's `cutout` mode (`floodfill` for flat/hard-edge, `rembg` for soft / 3D / glossy / photo).
6. **QA (mandatory).** Composite the sliced PNGs onto a contrasting colour (e.g. magenta) and check every icon for (a) a fragment bled in from a neighbouring cell, (b) leftover grey, and (c) consistency against the style's `construction` — uniform stroke, one radius, matched detail level, shared parts, motif present, single perspective, and no accent out-weighting the defining element (in line styles the accent must be lighter and smaller than the stroke). Re-slice or regenerate any that fail — never ship an icon carrying part of the one above it.
7. **Deliver** the transparent PNGs, organized and named.

## Built-in styles

| style | look | cutout | fits |
|---|---|---|---|
| linear | mono line / outline | floodfill | utility, settings |
| filled | solid single-colour glyphs | floodfill | mobile nav / tab bars |
| colorblock | bold flat multi-colour blocks | floodfill | kids, creative |
| cartoon | sticker-style cartoon | rembg | games, entertainment |
| isometric | isometric 3D miniatures | rembg | SaaS, dashboards |
| render3d | glossy puffy 3D | rembg | rewards, onboarding |
| sticker | die-cut glossy vinyl | rembg | social, reactions |
| realistic | photoreal product renders | rembg | e-commerce, hero |
| animal-badge | animal emblems in badges | rembg | avatars, kids |

Each `styles/<name>.json` holds the preamble, locked palette, cutout mode, threshold, construction system, and what it fits.

## Key rules (see `reference/design-rules.md`)

- **Lock the palette as hex** in the spec — colourful styles drift run-to-run otherwise.
- **Never make black filled icons** — near-black / black may be used as a thin outline or line stroke, but never as the dominant filled mass of an icon set. If the brand foreground is black, map it to strokes only; for filled or duotone styles, choose a mid-light brand colour for the main shape and keep dark colours small.
- **Start from the real product context** — when a user gives a live site, screenshot, mascot, logo, or brand asset, derive the icon concepts and construction from that source first. Do not jump straight into generic style families such as isometric, duotone, 3D, or colorblock; those are finishes applied after the product motif, real navigation, and real feature names are locked.
- **Slicing drops neighbour bleed** — the slicer keeps only the centred icon per cell.
- **Cutout by edge type** — flat/hard-edge → floodfill; soft / 3D / glossy / photo → rembg.
- **Design sophistication comes from a construction system + a brand motif**, not from tinting a generic set — each style's `construction` object encodes the grid, stroke, radius, detail budget, shared parts, and motif (see `reference/construction.md`). A rigorous system ultimately wants vector; raster is for direction and spot icons.
