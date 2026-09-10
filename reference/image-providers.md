# Image-generation providers

The slicing pipeline is provider-agnostic: it only needs a **PNG sheet rendered on flat grey `#808080`** from a text prompt. Never assume a specific tool is present — pick a provider by capability detection, in this order.

## Detection order

1. **Built-in / host imagegen first.** If you (the agent running this skill) already have a callable text-to-image tool — Codex's built-in `image_gen`, the `imagegen` skill, another image-generation tool, or an MCP — use it directly. Do not launch external Codex CLI in this case. Built-in imagegen may write to `$CODEX_HOME/generated_images/...` instead of a requested path; after generation, move or copy the selected PNG to `raw/<style>.png`.
2. **Codex CLI fallback.** Only if the running agent has no callable image-generation tool, and Codex is available — 从已安装 Skill 清单定位 `codex` 的包装脚本，或使用 PATH 中已有的 `codex` — delegate generation to it: pass the composed prompt and have it save the PNG to `raw/<style>.png`.
3. **External API fallback.** Only if neither of the above exists, 沿用已授权的供应商；缺少供应商选择时询问，凭据通过安全配置入口提供，不进入聊天. For **OpenAI Images (gpt-image)**, `scripts/gen_image.py --prompt "…" --out raw/<style>.png` is ready (reads `OPENAI_API_KEY`). For any other API (Replicate, Fal, Stability, a self-hosted model...), call it directly to produce the PNG.

## The contract

Any provider must satisfy one thing: **text prompt → one PNG**, rendered as the 4×4 (or 3×3) sheet on a solid flat grey `#808080` background, roughly square. That is all the slicer needs; everything downstream is identical regardless of provider.

## Provider notes

- **Reference images** — bundled `gen_image.py` 的当前入口使用文本提示；其他宿主或供应商是否支持参考图，按实际工具能力判断。支持时可传入已确认的图标 sheet 作为风格参考，仍需验收偏差。
- **Output size** — providers differ (gpt-image ≈ 1024²). The slicer reads real dimensions, so exact size does not matter.
- **Output path** — host image tools may not accept an exact destination path. Generate first, then move or copy the chosen PNG into the task directory’s `raw/<style>.png`.
- **Background / alpha** — oil-icon asks the image provider for a flat grey `#808080` sheet, not a transparent PNG. The oil-icon slicer creates transparency later; do not use a provider's transparent-output or chroma-key workflow for this step unless the user is doing a non-oil-icon image task.
- **One sheet, not one icon** — always prefer one sheet of 16 (or 9): 一次生成有助于统一，但仍需逐个检查风格. Fall back to one-icon-per-image only if a provider cannot hold a coherent multi-icon layout.
