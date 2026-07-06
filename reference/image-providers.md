# Image-generation providers

The slicing pipeline is provider-agnostic: it only needs a **PNG sheet rendered on flat grey `#808080`** from a text prompt. Never assume a specific tool is present — pick a provider by capability detection, in this order.

## Detection order

1. **Built-in / host imagegen first.** If you (the agent running this skill) already have a callable text-to-image tool — Codex's built-in `image_gen`, the `imagegen` skill, another image-generation tool, or an MCP — use it directly. Do not launch external Codex CLI in this case. Built-in imagegen may write to `$CODEX_HOME/generated_images/...` instead of a requested path; after generation, move or copy the selected PNG to `raw/<style>.png`.
2. **Codex CLI fallback.** Only if the running agent has no callable image-generation tool, and Codex is available — the bundled `codex` skill (`~/.claude/skills/codex/scripts/ask_codex.sh`) or `codex` on PATH — delegate generation to it: pass the composed prompt and have it save the PNG to `raw/<style>.png`.
3. **External API fallback.** Only if neither of the above exists, ask the user which image API to use and where the key lives. For **OpenAI Images (gpt-image)**, `scripts/gen_image.py --prompt "…" --out raw/<style>.png` is ready (reads `OPENAI_API_KEY`). For any other API (Replicate, Fal, Stability, a self-hosted model...), call it directly to produce the PNG.

## The contract

Any provider must satisfy one thing: **text prompt → one PNG**, rendered as the 4×4 (or 3×3) sheet on a solid flat grey `#808080` background, roughly square. That is all the slicer needs; everything downstream is identical regardless of provider.

## Provider notes

- **Reference images** — the common gpt-image path (Codex / OpenAI Images) is text-only, so consistency comes from the frozen text spec + locked palette. Some providers accept an input/reference image; if yours does, you may additionally pass an approved sheet as a style anchor.
- **Output size** — providers differ (gpt-image ≈ 1024²). The slicer reads real dimensions, so exact size does not matter.
- **Output path** — host image tools may not accept an exact destination path. Generate first, then move or copy the chosen PNG into `raw/<style>.png`.
- **Background / alpha** — oil-icon asks the image provider for a flat grey `#808080` sheet, not a transparent PNG. The oil-icon slicer creates transparency later; do not use a provider's transparent-output or chroma-key workflow for this step unless the user is doing a non-oil-icon image task.
- **One sheet, not one icon** — always prefer one sheet of 16 (or 9): a single generation keeps the style consistent. Fall back to one-icon-per-image only if a provider cannot hold a coherent multi-icon layout.
