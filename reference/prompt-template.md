# Composing a generation prompt

A sheet prompt = **style preamble** + **construction** + **palette lock** + **icon list** + **composition**, in that order. Send it to your chosen image provider (see `reference/image-providers.md`) to render one sheet on flat grey.

## Composition (fixed for every sheet, use verbatim)

> A neat {GRID} grid on a perfectly uniform solid flat medium-grey background, exact hex #808080. The background must have no gradient, no vignette, no lighting, no texture, no paper grain, and no shadow. Even and generous equal gaps between every cell so icons never touch, each icon centered in its own cell, all icons the same size. No grid lines, no borders, no frames, no text, no labels, no numbers, and no drop shadow cast onto the grey background. Square image.

- {GRID} = `4x4`, {N} = `16` by default — or `3x3` / `9` for maximum slicing stability.
- For an exact requested count below 16, keep `{GRID}` as `4x4`: generate icons only in the first `N` row-major positions, and leave cells `N+1..16` completely empty as plain grey `#808080` background. Do not add placeholder marks, ghost shapes, labels, dots, frames, or faint icons in the empty cells.
- For partial sheets, spell out both the row layout and the real icon center points. Use `x=12.5%, 37.5%, 62.5%, 87.5%` and `y=12.5%, 37.5%, 62.5%, 87.5%` for the 4x4 cells. This is mandatory because image models may otherwise compress a small count into one row or shift the occupied rows upward.
- Generous gaps are load-bearing: they give the slicer clean gutters so neighbouring icons stay separate and no fragment bleeds across.

## Palette lock

If the style has a `palette`, append:

> Use only these colours and no others: {hex list}. Keep the saturation as given; do not brighten or shift the hues.

Omit for styles with no fixed palette (e.g. realistic).

## Icon list

Number the concepts row-major, each a short concrete metaphor, no text:

> The {N} icons in row-major order: 1. …, 2. …, … Each is a simple, clear metaphor. No text anywhere.

For exact counts below 16, append:

> IMPORTANT LAYOUT: This is still a 4x4 sheet with 16 cells total. Keep the full 4-column by 4-row layout even though there are only {N} icons. Do not arrange the {N} icons in a single row. Do not distribute the {N} icons evenly across the full width.
>
> Place icons in row-major positions exactly like this:
> Row 1: {row 1 cells}
> Row 2: {row 2 cells}
> Row 3: {row 3 cells}
> Row 4: {row 4 cells}
>
> Place each real icon at its exact 4x4 cell center:
> 1. icon 1 center at x=12.5%, y=12.5%
> 2. icon 2 center at x=37.5%, y=12.5%
> 3. icon 3 center at x=62.5%, y=12.5%
> 4. icon 4 center at x=87.5%, y=12.5%
> 5. icon 5 center at x=12.5%, y=37.5%
> Continue the same row-major center pattern until icon {N}.
>
> Keep each real icon small enough to fit fully inside its own 25% by 25% cell, with large grey margins around it.
>
> Empty cells must be completely plain grey #808080 background, with no icon, no placeholder, no faint mark, no decoration, no dots, no labels, no numbers, and no frame.

## Full shape

```
{style.preamble}

{construction — render the style's construction fields as short guidance, e.g. "Construction: uniform 2-unit stroke, rounded joins; one consistent corner radius; one core idea per icon; reuse shared sub-shapes; single perspective; a recurring <motif> as the signature."}

{palette-lock line, if the style has a palette}

{icon list}

{composition}
```

Keep one clear idea per icon and a consistent detail level across the set — mixed complexity reads as "not designed".
