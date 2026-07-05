#!/usr/bin/env python3
"""图标切图器：4x4 分格 + 每格抠图 + 连通域清理，丢掉邻格漂进来的碎片。

关键：gpt-image 不会把图标摆在完美网格上，图标会上下左右漂。固定分格会把上一格
探进来的部分带进当前格。这里每格切完后做连通域分析：只保留【居中的主图标 + 紧挨
它的部件】，隔着间距的邻格碎片一律丢弃。

cutout 模式：
  floodfill —— 扁平图标 / 灰底，从边界连通域去背景（快、准）
  rembg     —— 软边 / 3D / 反光 / 照片，ML 抠图
"""
import sys, argparse
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage


def floodfill_alpha(rgb, thresh, bg=(128, 128, 128)):
    """rgb: HxWx3 int。删掉所有接近灰底色的像素——包括图标内部被包围的镂空
    （放大镜镜片、齿轮中心、日历格子、锁孔），否则这些洞会残留灰底。
    背景基准用固定 #808080（我们生成时就固定这个灰），不逐格采样——避免大图标/
    带底色瓷砖的角落被误判成背景，从而把 cream 底当灰删掉。
    仅对『扁平图标 + 纯灰底』安全：这些风格的图标/瓷砖颜色都远离灰。"""
    bg = np.array(bg)
    diff = np.abs(rgb - bg).max(axis=2)
    return np.where(diff < thresh, 0, 255).astype(np.uint8)


def clean(alpha):
    """连通域清理：保留居中主图标 + 紧邻部件，丢掉邻格碎片和小杂点。"""
    mask = alpha > 40
    if not mask.any():
        return None
    labels, n = ndimage.label(mask)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    h, w = mask.shape
    cx, cy = w / 2.0, h / 2.0
    coms = ndimage.center_of_mass(mask, labels, range(1, n + 1))
    # 居中候选：质心落在中央 68% 框内
    cand = [l for l in range(1, n + 1)
            if abs(coms[l - 1][1] - cx) < 0.34 * w and abs(coms[l - 1][0] - cy) < 0.34 * h]
    if not cand:
        cand = [int(np.argmax(sizes))]
    main = max(cand, key=lambda l: sizes[l])
    slices = ndimage.find_objects(labels)
    mb = slices[main - 1]
    link = 0.05 * max(h, w)          # 与主体的间隙 < 5% 视为同一图标的部件
    min_area = 0.02 * sizes[main]     # 小于主体 2% 的当杂点丢掉
    keep = {main}
    for l in range(1, n + 1):
        if l == main or sizes[l] < min_area:
            continue
        b = slices[l - 1]
        dy = max(0, b[0].start - mb[0].stop, mb[0].start - b[0].stop)
        dx = max(0, b[1].start - mb[1].stop, mb[1].start - b[1].stop)
        if dy <= link and dx <= link:
            keep.add(l)
    out = alpha.copy()
    out[~np.isin(labels, list(keep))] = 0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("outdir")
    ap.add_argument("--mode", choices=["floodfill", "rembg"], default="floodfill")
    ap.add_argument("--grid", type=int, default=4)
    ap.add_argument("--thresh", type=int, default=24)
    ap.add_argument("--size", type=int, default=512)
    a = ap.parse_args()

    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)
    im = Image.open(a.sheet).convert("RGB")
    W, H = im.size
    g = a.grid
    cw, ch = W // g, H // g
    pad = int(0.06 * min(cw, ch))     # 略微外扩，兜住漂出格子的图标
    session = None
    if a.mode == "rembg":
        from rembg import new_session
        session = new_session("u2net")

    warned = []
    idx = 1
    for r in range(g):
        for c in range(g):
            x0, y0 = c * cw, r * ch
            px0, py0 = max(0, x0 - pad), max(0, y0 - pad)
            px1, py1 = min(W, x0 + cw + pad), min(H, y0 + ch + pad)
            cell = im.crop((px0, py0, px1, py1))
            rgb = np.array(cell).astype(int)
            if a.mode == "floodfill":
                alpha = floodfill_alpha(rgb, a.thresh)
            else:
                from rembg import remove
                alpha = np.array(remove(cell, session=session).split()[-1])
            cleaned = clean(alpha)
            if cleaned is None or (cleaned > 0).sum() < 40:
                warned.append(f"{idx:02d}(空)")
                Image.new("RGBA", (a.size, a.size), (0, 0, 0, 0)).save(outdir / f"{idx:02d}.png")
                idx += 1
                continue
            ys, xs = np.where(cleaned > 0)
            rgba = np.dstack([rgb.astype(np.uint8), cleaned])[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            obj = Image.fromarray(rgba, "RGBA")
            side = int(max(obj.size) * 1.16)
            canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
            canvas.paste(obj, ((side - obj.width) // 2, (side - obj.height) // 2), obj)
            canvas.resize((a.size, a.size), Image.LANCZOS).save(outdir / f"{idx:02d}.png")
            idx += 1
    print(f"{a.sheet} -> {a.outdir}  mode={a.mode}  cells={idx-1}" + (f"  ⚠ {warned}" if warned else "  ✓"))


if __name__ == "__main__":
    main()
