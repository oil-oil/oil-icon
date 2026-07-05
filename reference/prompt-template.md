# Composing a generation prompt

A sheet prompt = **style preamble** + **construction** + **palette lock** + **icon list** + **composition**, in that order. Send it to your chosen image provider (see `reference/image-providers.md`) to render one sheet on flat grey.

## Composition (fixed for every sheet, use verbatim)

> A neat {GRID} grid of {N} separate icons on a solid flat medium-grey background, hex #808080. Even and generous equal gaps between every icon so they never touch, each icon centered in its own cell, all the same size. No grid lines, no borders, no frames, no text, no labels, no numbers, and no drop shadow cast onto the grey background. Square image.

- {GRID} = `4x4`, {N} = `16` by default — or `3x3` / `9` for maximum slicing stability.
- Generous gaps are load-bearing: they give the slicer clean gutters so neighbouring icons stay separate and no fragment bleeds across.

## Palette lock

If the style has a `palette`, append:

> Use only these colours and no others: {hex list}. Keep the saturation as given; do not brighten or shift the hues.

Omit for styles with no fixed palette (e.g. realistic).

## Icon list

Number the concepts row-major, each a short concrete metaphor, no text:

> The {N} icons in row-major order: 1. …, 2. …, … Each is a simple, clear metaphor. No text anywhere.

## Full shape

```
{style.preamble}

{construction — render the style's construction fields as short guidance, e.g. "Construction: uniform 2-unit stroke, rounded joins; one consistent corner radius; one core idea per icon; reuse shared sub-shapes; single perspective; a recurring <motif> as the signature."}

{palette-lock line, if the style has a palette}

{icon list}

{composition}
```

Keep one clear idea per icon and a consistent detail level across the set — mixed complexity reads as "not designed".
