#!/usr/bin/env python3
"""Generate note header image for Claude Code hooks article"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os

W, H = 1280, 670

# ── Font paths (macOS) ──────────────────────────────────────
FONT_PATHS_JP = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc",
]
FONT_PATHS_EN = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/SFNSDisplay.ttf",
]

def load_font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_title  = load_font(FONT_PATHS_JP, 72)
font_sub    = load_font(FONT_PATHS_JP, 32)
font_tag    = load_font(FONT_PATHS_JP, 26)
font_label  = load_font(FONT_PATHS_JP, 22)

# ── Canvas ───────────────────────────────────────────────────
img = Image.new("RGB", (W, H), (18, 26, 18))
d   = ImageDraw.Draw(img)

# ── Background: subtle grid dots ────────────────────────────
for gx in range(0, W, 48):
    for gy in range(0, H, 48):
        d.ellipse([gx-1, gy-1, gx+1, gy+1], fill=(40, 58, 38))

# ── Left accent bar ──────────────────────────────────────────
d.rectangle([0, 0, 6, H], fill=(100, 140, 70))

# ── Flow diagram: 3 nodes connected by arrows ────────────────
# Node positions
nodes = [
    (220, 335, "Edit / Write", "#4E6B3E"),
    (640, 335, "Hook",         "#7A9A55"),
    (1060, 335, "自動実行",    "#9DBB6E"),
]
node_w, node_h = 200, 70
arrow_y = 335

for (nx, ny, label, col) in nodes:
    # Node box
    x0, y0 = nx - node_w//2, ny - node_h//2
    x1, y1 = nx + node_w//2, ny + node_h//2
    # Shadow
    d.rounded_rectangle([x0+4, y0+4, x1+4, y1+4], radius=14,
                         fill=(10, 18, 10))
    # Box
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=col)
    # Label
    bbox = d.textbbox((0, 0), label, font=font_tag)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((nx - tw//2, ny - th//2), label,
           font=font_tag, fill=(240, 240, 230))

# Arrows between nodes
def draw_arrow(d, x1, y1, x2, y2, col=(140, 180, 100)):
    margin = node_w // 2 + 14
    sx, sy = x1 + margin, y1
    ex, ey = x2 - margin, y2
    # Line
    d.line([(sx, sy), (ex, ey)], fill=col, width=3)
    # Arrowhead
    aw = 14
    d.polygon([(ex, ey),
               (ex - aw, ey - aw//2),
               (ex - aw, ey + aw//2)], fill=col)

for i in range(len(nodes) - 1):
    draw_arrow(d, nodes[i][0], nodes[i][1],
                  nodes[i+1][0], nodes[i+1][1])

# ── Sub-labels under nodes ───────────────────────────────────
sublabels = [
    (220, 395, "ファイル保存"),
    (640, 395, "settings.json"),
    (1060, 395, "git push / reload"),
]
for (sx, sy, sl) in sublabels:
    bbox = d.textbbox((0, 0), sl, font=font_label)
    tw = bbox[2] - bbox[0]
    d.text((sx - tw//2, sy), sl,
           font=font_label, fill=(100, 130, 80))

# ── Title ────────────────────────────────────────────────────
title1 = "Claude Codeのフック機能で"
title2 = "開発作業を全自動化した話"

bbox1 = d.textbbox((0, 0), title1, font=font_title)
bbox2 = d.textbbox((0, 0), title2, font=font_title)
tw1 = bbox1[2] - bbox1[0]
tw2 = bbox2[2] - bbox2[0]

# Slight shadow for readability
for off in [(2, 2), (3, 3)]:
    d.text(((W - tw1)//2 + off[0], 100 + off[1]), title1,
           font=font_title, fill=(10, 20, 10))
    d.text(((W - tw2)//2 + off[0], 182 + off[1]), title2,
           font=font_title, fill=(10, 20, 10))

d.text(((W - tw1)//2, 100), title1, font=font_title, fill=(235, 240, 225))
d.text(((W - tw2)//2, 182), title2, font=font_title, fill=(235, 240, 225))

# ── Tags ─────────────────────────────────────────────────────
tags = ["#ClaudeCode", "#自動化", "#開発効率化", "#GitHubActions"]
tx = 80
ty = 580
for tag in tags:
    bbox = d.textbbox((0, 0), tag, font=font_tag)
    tw = bbox[2] - bbox[0]
    # Pill background
    pad = 14
    d.rounded_rectangle([tx - pad, ty - 8,
                          tx + tw + pad, ty + 34],
                         radius=20, fill=(35, 52, 28))
    d.text((tx, ty), tag, font=font_tag, fill=(140, 185, 100))
    tx += tw + pad * 2 + 12

# ── Bottom line ──────────────────────────────────────────────
d.rectangle([80, H - 6, W - 80, H - 2], fill=(80, 115, 55))

# ── Subtle vignette ──────────────────────────────────────────
vignette = Image.new("RGB", (W, H), (0, 0, 0))
vd = ImageDraw.Draw(vignette)
for i in range(120):
    alpha = int(80 * (i / 120))
    vd.rectangle([i, i, W-i, H-i], outline=(0, 0, 0, 0))

# Apply vignette as overlay
vig_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
for i in range(80):
    a = int(120 * ((80 - i) / 80) ** 2)
    ImageDraw.Draw(vig_layer).rectangle(
        [i, i, W-1-i, H-1-i], outline=(0, 0, 0, a))
img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, vig_layer)
img = img_rgba.convert("RGB")

out = "/Users/zett/bookshelf/note_header.png"
img.save(out, quality=95)
print(f"Saved: {out}")
