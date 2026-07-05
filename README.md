# oil-icon

`oil-icon` is a personal icon-system skill by [oil-oil](https://github.com/oil-oil).

It generates cohesive transparent-background icon sets from one 4x4 image sheet. The workflow locks a visual style, asks an image model to draw a grey-background sheet, then slices and removes backgrounds into clean PNG icons.

## What It Is For

- Product icon packs
- Brand-matched spot icons
- Feature, category, empty-state, and marketing icons
- Style systems such as line, filled, color block, cartoon, isometric, 3D, sticker, realistic, and animal badge

It is not meant for tiny 16-24px functional UI glyphs. Use a vector icon library for those.

## Install

Use this repository as a local agent skill:

```bash
git clone https://github.com/oil-oil/oil-icon.git ~/.claude/skills/oil-icon
```

For Codex-style local skills, clone it to:

```bash
git clone https://github.com/oil-oil/oil-icon.git ~/.codex/skills/oil-icon
```

## Contents

- `SKILL.md` - the main skill instructions
- `styles/` - built-in visual style specs
- `reference/` - design rules, prompting, construction, and provider guidance
- `scripts/` - image generation fallback and slicing tools

## Basic Workflow

1. Pick a built-in style or derive a custom brand-matched style.
2. List 16 icon concepts as clear concrete metaphors.
3. Generate a 4x4 sheet on a flat `#808080` grey background.
4. Run `scripts/setup.sh` once.
5. Slice the sheet with `scripts/slice_icons.py`.
6. QA the PNGs on a contrasting background before shipping.

## License

MIT
