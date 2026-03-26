#!/usr/bin/env python3
"""Generate Lumina icons — Apple-designer level v6"""
from PIL import Image, ImageDraw, ImageFilter
import math

def rr(draw, xy, r, fill):
    x0,y0,x1,y1 = [int(v) for v in xy]
    r = max(1, int(r))
    draw.rectangle([x0+r,y0,x1-r,y1], fill=fill)
    draw.rectangle([x0,y0+r,x1,y1-r], fill=fill)
    draw.ellipse([x0,y0,x0+2*r,y0+2*r], fill=fill)
    draw.ellipse([x1-2*r,y0,x1,y0+2*r], fill=fill)
    draw.ellipse([x0,y1-2*r,x0+2*r,y1], fill=fill)
    draw.ellipse([x1-2*r,y1-2*r,x1,y1], fill=fill)

def clip(S, bg_r):
    m = Image.new("L",(S,S),0)
    rr(ImageDraw.Draw(m),[0,0,S-1,S-1],bg_r,255)
    return m

def blend(img, layer, mask_fn=None):
    result = Image.alpha_composite(img, layer)
    return result

def make_icon(size):
    sc = 4
    S  = size * sc
    cx = S / 2
    cy = S / 2
    bg_r = int(S * 0.22)

    # ─── Background ─────────────────────────────────────────
    img = Image.new("RGBA",(S,S),(0,0,0,0))
    d = ImageDraw.Draw(img)
    rr(d,[0,0,S-1,S-1],bg_r,(78,98,62,255))
    img.putalpha(clip(S,bg_r))

    # ─── Book ───────────────────────────────────────────────
    bw   = int(S * 0.72)
    bh   = int(S * 0.43)
    bx   = int(cx - bw/2)
    by   = int(cy - bh/2 + S*0.08)
    tck  = int(S * 0.020)
    pr   = int(S * 0.018)
    lw   = bw // 2       # half width (pages meet at center, no gap)
    rx   = bx + lw

    # Orb: clearly floating above book
    orb_r  = int(S * 0.065)
    orb_cy = int(by - S*0.085)

    # ─── Drop shadow ────────────────────────────────────────
    sh = Image.new("RGBA",(S,S),(0,0,0,0))
    so = int(S*0.020)
    rr(ImageDraw.Draw(sh),
       [bx-so//2, by+so*2, bx+bw+so//2, by+bh+tck+so*3],
       pr+so, (10,22,8,110))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=S*0.042))
    img = Image.alpha_composite(img,sh); img.putalpha(clip(S,bg_r))

    # ─── Halo ───────────────────────────────────────────────
    ha = Image.new("RGBA",(S,S),(0,0,0,0))
    hr = int(S*0.27)
    ImageDraw.Draw(ha).ellipse(
        [cx-hr, orb_cy-hr*0.45, cx+hr, orb_cy+hr*0.45],
        fill=(255,215,68,50))
    ha = ha.filter(ImageFilter.GaussianBlur(radius=S*0.09))
    img = Image.alpha_composite(img,ha); img.putalpha(clip(S,bg_r))

    d = ImageDraw.Draw(img)

    # ─── Rays ───────────────────────────────────────────────
    rw = max(3, int(S*0.018))
    for deg in [-64,-40,-16,16,40,64]:
        rad = math.radians(deg - 90)
        r0  = orb_r + int(S*0.016)
        r1  = orb_r + int(S*0.092)
        d.line([
            (cx + r0*math.cos(rad), orb_cy + r0*math.sin(rad)),
            (cx + r1*math.cos(rad), orb_cy + r1*math.sin(rad))
        ], fill=(250,207,58,218), width=rw)

    # ─── Page shapes ────────────────────────────────────────
    def left_pts():
        pts = [(bx,by+bh),(bx+lw,by+bh),(bx+lw,by)]
        n = 28
        for i in range(n+1):
            t = i/n
            sag = int(bh*0.050*math.sin(t*math.pi*0.5))
            pts.append((bx+lw*(1-t), by-sag))
        return pts

    def right_pts():
        pts = [(rx+lw,by+bh),(rx,by+bh),(rx,by)]
        n = 28
        for i in range(n+1):
            t = i/n
            sag = int(bh*0.050*math.sin(t*math.pi*0.5))
            pts.append((rx+lw*t, by-sag))
        return pts

    # Bottom edge thickness
    d.polygon([(bx,by+bh),(bx+lw,by+bh),(bx+lw,by+bh+tck),(bx,by+bh+tck)],
              fill=(210,202,188,255))
    d.polygon([(rx,by+bh),(rx+lw,by+bh),(rx+lw,by+bh+tck),(rx,by+bh+tck)],
              fill=(210,202,188,255))

    # Pages
    d.polygon(left_pts(),  fill=(246,242,233,255))
    d.polygon(right_pts(), fill=(239,234,224,255))

    # ─── Fold: soft blurred shadow strip at center ──────────
    fold = Image.new("RGBA",(S,S),(0,0,0,0))
    fd = ImageDraw.Draw(fold)
    fw = int(S*0.025)   # half-width of fold shadow
    fd.rectangle([int(cx)-fw, by+pr, int(cx)+fw, by+bh-pr],
                 fill=(30,22,12,100))
    fold = fold.filter(ImageFilter.GaussianBlur(radius=S*0.018))
    # Clip fold shadow to be only within book area
    book_mask = Image.new("L",(S,S),0)
    bmd = ImageDraw.Draw(book_mask)
    rr(bmd,[bx,by,bx+bw,by+bh],pr,255)
    fold_r,fold_g,fold_b,fold_a = fold.split()
    fold_a = Image.composite(fold_a, Image.new("L",(S,S),0), book_mask)
    fold = Image.merge("RGBA",[fold_r,fold_g,fold_b,fold_a])
    img = Image.alpha_composite(img,fold); img.putalpha(clip(S,bg_r))

    d = ImageDraw.Draw(img)

    # ─── Orb glow ───────────────────────────────────────────
    og = Image.new("RGBA",(S,S),(0,0,0,0))
    ow = int(orb_r*1.9)
    ImageDraw.Draw(og).ellipse(
        [cx-ow,orb_cy-ow,cx+ow,orb_cy+ow], fill=(255,206,48,185))
    og = og.filter(ImageFilter.GaussianBlur(radius=S*0.023))
    img = Image.alpha_composite(img,og); img.putalpha(clip(S,bg_r))

    d = ImageDraw.Draw(img)

    # ─── Orb ────────────────────────────────────────────────
    d.ellipse([cx-orb_r,orb_cy-orb_r,cx+orb_r,orb_cy+orb_r],
              fill=(252,200,48,255))
    ir = int(orb_r*0.46); hx = int(orb_r*0.17); hy = int(orb_r*0.20)
    d.ellipse([cx-ir-hx,orb_cy-ir-hy,cx+ir-hx,orb_cy+ir-hy],
              fill=(255,250,200,255))

    img.putalpha(clip(S,bg_r))
    return img.resize((size,size), Image.LANCZOS)


for sz in [192, 512]:
    make_icon(sz).save(f"/Users/zett/bookshelf/icons/icon-{sz}.png")
    print(f"Saved icon-{sz}.png")
print("Done!")
