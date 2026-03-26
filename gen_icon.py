#!/usr/bin/env python3
"""Generate Lumina app icons (192x192 and 512x512)"""

import math

def make_icon_svg(size):
    s = size
    r = s * 0.22  # corner radius (maskable)
    cx, cy = s / 2, s / 2

    # Colors
    bg = "#3A4A30"
    book_fill = "#EDE8DF"
    spine = "#C8BFB0"
    glow = "#F5D97A"
    page_shadow = "#C8BFB0"

    # Book dimensions (centered, slightly below center)
    bw = s * 0.46
    bh = s * 0.38
    bx = cx - bw / 2
    by = cy - bh / 2 + s * 0.04

    # Spine width
    sw = s * 0.04

    # Ray angles and lengths
    rays = []
    for angle_deg in [-60, -30, 0, 30, 60]:
        angle_rad = math.radians(angle_deg - 90)
        ray_start = s * 0.13
        ray_end = s * 0.22
        x1 = cx + ray_start * math.cos(angle_rad)
        y1 = (by - s * 0.04) + ray_start * math.sin(angle_rad)
        x2 = cx + ray_end * math.cos(angle_rad)
        y2 = (by - s * 0.04) + ray_end * math.sin(angle_rad)
        rays.append((x1, y1, x2, y2))

    ray_width = s * 0.025

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 {s} {s}">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#4A5E3C"/>
      <stop offset="100%" stop-color="#2A3622"/>
    </radialGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FDE68A" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.6"/>
    </radialGradient>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="{s*0.015}" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="{s}" height="{s}" rx="{r}" ry="{r}" fill="url(#bgGrad)"/>

  <!-- Glow halo above book -->
  <ellipse cx="{cx}" cy="{by - s*0.02}" rx="{s*0.18}" ry="{s*0.10}"
           fill="#FDE68A" opacity="0.18"/>

  <!-- Light rays -->'''

    for x1, y1, x2, y2 in rays:
        svg += f'''
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
        stroke="{glow}" stroke-width="{ray_width:.1f}" stroke-linecap="round" opacity="0.85"/>'''

    svg += f'''

  <!-- Book shadow -->
  <rect x="{bx + s*0.015:.1f}" y="{by + s*0.015:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{s*0.02}"
        fill="#1A2415" opacity="0.3"/>

  <!-- Book left page -->
  <rect x="{bx:.1f}" y="{by:.1f}" width="{bw/2 - sw/2:.1f}" height="{bh:.1f}" rx="{s*0.015}"
        fill="{book_fill}"/>

  <!-- Book right page -->
  <rect x="{bx + bw/2 + sw/2:.1f}" y="{by:.1f}" width="{bw/2 - sw/2:.1f}" height="{bh:.1f}" rx="{s*0.015}"
        fill="{book_fill}" opacity="0.92"/>

  <!-- Page lines left -->
  <line x1="{bx + bw*0.1:.1f}" y1="{by + bh*0.25:.1f}" x2="{bx + bw*0.42:.1f}" y2="{by + bh*0.25:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.1:.1f}" y1="{by + bh*0.42:.1f}" x2="{bx + bw*0.42:.1f}" y2="{by + bh*0.42:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.1:.1f}" y1="{by + bh*0.59:.1f}" x2="{bx + bw*0.35:.1f}" y2="{by + bh*0.59:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.1:.1f}" y1="{by + bh*0.76:.1f}" x2="{bx + bw*0.42:.1f}" y2="{by + bh*0.76:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>

  <!-- Page lines right -->
  <line x1="{bx + bw*0.58:.1f}" y1="{by + bh*0.25:.1f}" x2="{bx + bw*0.90:.1f}" y2="{by + bh*0.25:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.58:.1f}" y1="{by + bh*0.42:.1f}" x2="{bx + bw*0.90:.1f}" y2="{by + bh*0.42:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.58:.1f}" y1="{by + bh*0.59:.1f}" x2="{bx + bw*0.82:.1f}" y2="{by + bh*0.59:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>
  <line x1="{bx + bw*0.58:.1f}" y1="{by + bh*0.76:.1f}" x2="{bx + bw*0.90:.1f}" y2="{by + bh*0.76:.1f}"
        stroke="{page_shadow}" stroke-width="{s*0.012:.1f}" stroke-linecap="round"/>

  <!-- Spine -->
  <rect x="{bx + bw/2 - sw/2:.1f}" y="{by:.1f}" width="{sw:.1f}" height="{bh:.1f}"
        fill="{spine}" rx="{sw*0.3}"/>

  <!-- Sun / light gem above book -->
  <circle cx="{cx:.1f}" cy="{by - s*0.02:.1f}" r="{s*0.065:.1f}"
          fill="url(#glowGrad)" filter="url(#softGlow)"/>
  <circle cx="{cx:.1f}" cy="{by - s*0.02:.1f}" r="{s*0.038:.1f}"
          fill="#FFFBEB"/>
</svg>'''

    return svg


for size in [192, 512]:
    svg_content = make_icon_svg(size)
    with open(f"/Users/zett/bookshelf/icons/icon-{size}.svg", "w") as f:
        f.write(svg_content)
    print(f"Created icon-{size}.svg")

print("Done! Convert SVGs to PNG using:")
print("  python3 -c \"import cairosvg; cairosvg.svg2png(url='icons/icon-192.svg', write_to='icons/icon-192.png', output_width=192)\"")
print("or open the SVGs in a browser/Inkscape to export as PNG.")
