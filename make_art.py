"""
FindIt - draws the 5 level characters ("Findy") as SVG files in assets/levels/.
Run once: python make_art.py   (the SVG files are already included)

Findy is a round little finder with a magnifying glass. It grows up level by level:
  1 New Finder    - a sprout on top
  2 Finder        - a cap
  3 Super Finder  - a cape and an eye mask
  4 Finder Hero   - a cape and a star headband
  5 FindIt Legend - a crown, a royal cape and sparkles
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "levels")
INK = "#1B1B1B"

LEVEL_ART = [
    # body color, darker shade
    ("#7FE0B5", "#3FB585"),
    ("#5AC8FA", "#2E95CC"),
    ("#FF6FAE", "#D9478A"),
    ("#9A7BFF", "#6C4FD6"),
    ("#FFC83D", "#E29A00"),
]


def cape(color):
    return (f'<path d="M54 104 Q14 170 24 204 L176 204 Q186 170 146 104 Z" fill="{color}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')


def body(fill, shade):
    return f'''
<ellipse cx="80" cy="196" rx="20" ry="10" fill="{shade}" stroke="{INK}" stroke-width="6"/>
<ellipse cx="120" cy="196" rx="20" ry="10" fill="{shade}" stroke="{INK}" stroke-width="6"/>
<ellipse cx="100" cy="132" rx="64" ry="60" fill="{fill}" stroke="{INK}" stroke-width="7"/>
<ellipse cx="78" cy="104" rx="20" ry="11" fill="#FFFFFF" opacity="0.45"/>
<ellipse cx="80" cy="128" rx="13" ry="16" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>
<ellipse cx="120" cy="128" rx="13" ry="16" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>
<circle cx="83" cy="132" r="7" fill="{INK}"/><circle cx="123" cy="132" r="7" fill="{INK}"/>
<circle cx="86" cy="128" r="2.6" fill="#FFFFFF"/><circle cx="126" cy="128" r="2.6" fill="#FFFFFF"/>
<ellipse cx="64" cy="152" rx="9" ry="6" fill="#FF8FB1" opacity="0.8"/>
<ellipse cx="136" cy="152" rx="9" ry="6" fill="#FF8FB1" opacity="0.8"/>
<path d="M88 156 Q100 170 112 156" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'''


def magnifier():
    return f'''
<path d="M150 150 Q166 150 172 140" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
<line x1="186" y1="132" x2="208" y2="160" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
<line x1="186" y1="132" x2="208" y2="160" stroke="#E8833A" stroke-width="6" stroke-linecap="round"/>
<circle cx="176" cy="116" r="24" fill="#D8F3FF" fill-opacity="0.85" stroke="{INK}" stroke-width="7"/>
<path d="M164 108 Q170 100 178 100" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'''


def sprout():
    return f'''
<path d="M100 74 Q100 60 100 52" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M100 56 Q78 34 66 52 Q84 64 100 56 Z" fill="#5BC236" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
<path d="M100 56 Q122 34 134 52 Q116 64 100 56 Z" fill="#5BC236" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'''


def cap():
    return f'''
<path d="M50 96 Q52 50 100 48 Q148 50 150 96 Z" fill="#FFD23F" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<path d="M140 92 Q176 88 186 100 Q166 106 140 102 Z" fill="#FFD23F" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
<circle cx="100" cy="50" r="6" fill="#E8833A" stroke="{INK}" stroke-width="4"/>
<path d="M66 84 Q100 70 134 84" fill="none" stroke="#E8833A" stroke-width="5"/>'''


def mask():
    return (f'<path d="M58 118 Q80 108 100 122 Q120 108 142 118 L142 138 Q120 146 100 134 '
            f'Q80 146 58 138 Z" fill="#E4002B" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            '<ellipse cx="80" cy="128" rx="10" ry="8" fill="#FFFFFF"/><ellipse cx="120" cy="128" rx="10" ry="8" fill="#FFFFFF"/>'
            f'<circle cx="82" cy="129" r="5.5" fill="{INK}"/><circle cx="122" cy="129" r="5.5" fill="{INK}"/>')


def star(cx, cy, r, fill):
    import math
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'


def headband():
    return (f'<path d="M40 102 Q100 72 160 102 L158 114 Q100 86 42 114 Z" fill="#FFD23F" stroke="{INK}" '
            f'stroke-width="5" stroke-linejoin="round"/>' + star(100, 90, 15, "#FF6FAE"))


def crown():
    return (f'<path d="M62 84 L66 44 L84 64 L100 36 L116 64 L134 44 L138 84 Z" fill="#FFD23F" stroke="{INK}" '
            f'stroke-width="6" stroke-linejoin="round"/>'
            f'<circle cx="100" cy="66" r="6" fill="#E4002B" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="78" cy="72" r="4.5" fill="#3FA9F5" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="122" cy="72" r="4.5" fill="#3FA9F5" stroke="{INK}" stroke-width="3"/>')


def sparkles():
    return star(30, 60, 13, "#FFF3B0") + star(186, 54, 10, "#FFF3B0") + star(22, 150, 9, "#FFF3B0")


def findy(level):
    fill, shade = LEVEL_ART[level - 1]
    parts = []
    if level == 5:
        parts.append('<circle cx="100" cy="122" r="96" fill="#FFF3B0" opacity="0.7"/>')
    if level == 3:
        parts.append(cape("#E4002B"))
    if level == 4:
        parts.append(cape("#FFD23F"))
    if level == 5:
        parts.append(cape("#7A5CC2"))
    parts.append(body(fill, shade))
    parts.append({1: sprout(), 2: cap(), 3: mask(), 4: headband(), 5: crown()}[level])
    if level == 5:
        parts.append(sparkles())
    parts.append(magnifier())
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="220" height="220">'
            + "".join(parts) + "</svg>")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for lv in range(1, 6):
        with open(os.path.join(OUT, f"level{lv}.svg"), "w") as f:
            f.write(findy(lv))
    print("saved", OUT)
