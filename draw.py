#!/usr/bin/env python3
"""Draw the front page: world news of Tuesday 24 November 2026.

Fresh artwork for the make.fun news-image-20261124 competition.
Renders a deterministic 1024x1024 PNG with no network access.
Run:  python3 draw.py   (writes entry.png next to this file)

Revision 3: base type enlarged by about a fifth throughout (body 18 -> 22,
headlines 21 -> 24, briefs 17 -> 20) after an independent review found the
small text hard to read at 300 px wide. The Solomon Islands–Australia
security pact is promoted to a full panel; the Pennsylvania measles story
moves down to the brief band, which is trimmed from six items to three.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
RED = (176, 42, 30)
NAVY = (22, 50, 79)
GOLD = (176, 132, 32)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (206, 200, 186)
STRIP_BG = (22, 50, 79)
STRIP_TEXT = (247, 243, 234)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictograms
# Every icon is drawn from primitives (lines, ellipses, polygons) in a
# square box of side s with its top-left corner at (x, y).

def icon_scales(d, x, y, s, c=NAVY):
    """Scales of justice."""
    cx, top = x + s // 2, y + s // 8
    d.line([(cx, top), (cx, y + s * 7 // 8)], fill=c, width=5)
    d.line([(x + s // 8, top + s // 8), (x + s * 7 // 8, top + s // 8)],
           fill=c, width=5)
    d.ellipse([cx - 5, top - 5, cx + 5, top + 5], fill=c)
    for sx in (x + s // 8, x + s * 7 // 8):
        d.line([(sx, top + s // 8), (sx, y + s // 2)], fill=c, width=3)
        d.polygon([(sx - s // 5, y + s // 2), (sx + s // 5, y + s // 2),
                   (sx, y + s * 5 // 8)], fill=c)
    d.line([(cx - s // 4, y + s * 7 // 8), (cx + s // 4, y + s * 7 // 8)],
           fill=c, width=5)


def icon_rocket(d, x, y, s, c=RED):
    cx = x + s // 2
    d.polygon([(cx, y + s // 12), (cx + s // 5, y + s // 2),
               (cx, y + s * 7 // 12), (cx - s // 5, y + s // 2)], fill=c)
    d.ellipse([cx - s // 10, y + s // 4, cx + s // 10, y + s // 2], fill=PAPER)
    d.polygon([(cx - s // 5, y + s // 2), (cx - s // 3, y + s * 3 // 4),
               (cx - s // 8, y + s * 7 // 12)], fill=c)
    d.polygon([(cx + s // 5, y + s // 2), (cx + s // 3, y + s * 3 // 4),
               (cx + s // 8, y + s * 7 // 12)], fill=c)
    d.polygon([(cx - s // 12, y + s * 7 // 12), (cx + s // 12, y + s * 7 // 12),
               (cx, y + s * 7 // 8)], fill=GOLD)
    d.ellipse([x + s // 8, y + s // 8, x + s // 4, y + s // 4], fill=GOLD)
    d.ellipse([x + s * 3 // 4, y + s // 6, x + s * 7 // 8, y + s // 3],
              fill=GOLD)


def icon_ship(d, x, y, s, c=NAVY):
    d.polygon([(x + s // 8, y + s * 5 // 8), (x + s * 7 // 8, y + s * 5 // 8),
               (x + s * 3 // 4, y + s * 7 // 8), (x + s // 4, y + s * 7 // 8)],
              fill=c)
    d.line([(x + s // 2, y + s // 8), (x + s // 2, y + s * 5 // 8)],
           fill=c, width=4)
    d.polygon([(x + s // 2, y + s // 8), (x + s // 2, y + s // 3),
               (x + s * 3 // 4, y + s // 3)], fill=RED)
    d.rectangle([x + s // 8, y + s * 3 // 8, x + s * 7 // 8, y + s // 2],
                fill=c)
    for wx in range(3):
        wx0 = x + s // 4 + wx * s // 5
        d.rectangle([wx0, y + s // 2, wx0 + s // 12, y + s * 9 // 16],
                    fill=GOLD)


def icon_chip(d, x, y, s, c=NAVY):
    m = s // 6
    d.rectangle([x + m, y + m, x + s - m, y + s - m], outline=c, width=5)
    d.rectangle([x + s // 3, y + s // 3, x + s * 2 // 3, y + s * 2 // 3],
                fill=c)
    for i in range(3):
        off = m + i * (s - 2 * m) // 2
        d.line([(x + off, y), (x + off, y + m)], fill=c, width=4)
        d.line([(x + off, y + s - m), (x + off, y + s)], fill=c, width=4)
        d.line([(x, y + off), (x + m, y + off)], fill=c, width=4)
        d.line([(x + s - m, y + off), (x + s, y + off)], fill=c, width=4)


def icon_shield(d, x, y, s, c=NAVY):
    """Shield with a check mark (security pact)."""
    cx = x + s // 2
    d.polygon([(cx - s * 3 // 8, y + s // 8), (cx + s * 3 // 8, y + s // 8),
               (cx + s * 3 // 8, y + s // 2), (cx, y + s * 7 // 8),
               (cx - s * 3 // 8, y + s // 2)], fill=c)
    d.line([(cx - s // 5, y + s // 2), (cx - s // 20, y + s * 5 // 8),
            (cx + s // 4, y + s // 3)], fill=GOLD, width=6, joint="curve")


def icon_tower(d, x, y, s, c=NAVY):
    cx = x + s // 2
    d.polygon([(cx - s // 6, y + s * 7 // 8), (cx - s // 12, y + s // 8),
               (cx + s // 12, y + s // 8), (cx + s // 6, y + s * 7 // 8)],
              fill=c)
    d.line([(cx, y + s // 8), (cx, y)], fill=c, width=4)
    for i, wy in enumerate((s // 4, s // 2, s * 3 // 4)):
        w = s // 10 + i * s // 60
        d.rectangle([cx - w, y + wy, cx + w, y + wy + s // 14], fill=GOLD)
    d.polygon([(cx - s // 5, y + s * 7 // 8), (cx + s // 5, y + s * 7 // 8),
               (cx + s // 8, y + s), (cx - s // 8, y + s)], fill=RED)


def icon_bars(d, x, y, s, c=NAVY):
    """Ascending bars with a falling arrow (shares down)."""
    bw = s // 6
    for i, hfrac in enumerate((0.35, 0.55, 0.8)):
        bx0 = x + s // 8 + i * (bw + s // 12)
        bh = int(s * hfrac)
        d.rectangle([bx0, y + s - s // 8 - bh, bx0 + bw, y + s - s // 8],
                    fill=c)
    d.line([(x + s // 8, y + s // 4), (x + s // 2, y + s * 5 // 12),
            (x + s * 7 // 8, y + s // 6)], fill=RED, width=5, joint="curve")
    d.polygon([(x + s * 7 // 8, y + s // 6), (x + s * 3 // 4, y + s // 6),
               (x + s * 7 // 8, y + s // 3)], fill=RED)


# ------------------------------------------------------------------- layout
def panel(d, x, y, w, h, kicker, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_LINE,
                width=2)
    pad = 12
    icon(d, x + pad, y + pad, 56)
    tx = x + pad + 56 + 10
    tw = x + w - pad - tx
    d.text((tx, y + pad + 2), kicker, font=font(SANS_B, 19), fill=RED)
    hl = wrap(d, headline, font(SANS_B, 24), tw)
    if len(hl) > 3:
        raise SystemExit("headline overflows panel: %r" % headline)
    draw_lines(d, hl, tx, y + pad + 28, font(SANS_B, 24), INK, 29)
    by = y + pad + 28 + 29 * len(hl)
    bl = wrap(d, body, font(SANS, 22), w - 2 * pad)
    if len(bl) > 4:
        raise SystemExit("body overflows panel: %r" % body)
    draw_lines(d, bl, x + pad, by + 6, font(SANS, 22), MUTED, 26)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 20  # outer margin

    # ---- masthead
    d.text((mx, 12), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 55), fill=INK)
    rule(d, mx, 76, W - mx, 3)
    d.text((mx, 84), "TUESDAY 24 NOVEMBER 2026",
           font=font(SANS_B, 38), fill=RED)
    d.text((W - mx - d.textlength("ONE DAY  •  ONE PAGE", font=font(SANS_B, 22)),
            92), "ONE DAY  •  ONE PAGE", font=font(SANS_B, 22), fill=MUTED)
    d.text((mx, 126), "Every story here was reported on Tuesday 24 November 2026.",
           font=font(SANS, 20), fill=MUTED)
    rule(d, mx, 152, W - mx, 2)

    # ---- lead story: ICJ ruling on Myanmar / Rohingya
    lx, ly, lw, lh = mx, 164, W - 2 * mx, 134
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL_BG,
                outline=PANEL_LINE, width=2)
    icon_scales(d, lx + 14, ly + 14, 96)
    tx = lx + 14 + 96 + 16
    d.text((tx, ly + 14), "TOP STORY  •  THE HAGUE — 14 STATES BACK THE RULING",
           font=font(SANS_B, 19), fill=RED)
    d.text((tx, ly + 40), "ICJ: Myanmar committed genocide",
           font=font(SANS_B, 34), fill=INK)
    d.text((tx, ly + 81), "against the Rohingya",
           font=font(SANS_B, 34), fill=INK)

    # ---- grid: six panels, 3 columns x 2 rows
    gx, gy = mx, 310
    gw = (W - 2 * mx - 2 * 12) // 3
    gh = 258
    panels = [
        ("SPACE", "Shenzhou-24 reaches Tiangong",
         "Two Chinese astronauts and Pakistan's Zeeshan Ali, "
         "the first foreigner on Tiangong.",
         icon_rocket),
        ("WAR IN UKRAINE", "Ukraine hits Russian ship in Gulf of Finland",
         "Zelenskyy confirms the strike; leaked data put Russian "
         "war losses above 700,000 troops.",
         icon_ship),
        ("AI", "UN chief: rein in AI risks within a year",
         "Guterres urges a multilateral framework to limit the "
         "risks of artificial intelligence.",
         icon_chip),
        ("SOLOMON ISLANDS", "Australia named top security partner",
         "The pact makes Australia the Solomons' main security "
         "partner, leaving China out.",
         icon_shield),
        ("MIDDLE EAST", "Houthi strike hits Riyadh's tallest tower",
         "The second hit in a week; 11 people were hurt.",
         icon_tower),
        ("TECH", "Huang back as Nvidia CEO; shares fall 7%",
         "Trump intervened to restore Jensen Huang as chief "
         "executive of Nvidia.",
         icon_bars),
    ]
    for i, (kick, head, body, ic) in enumerate(panels):
        px = gx + (i % 3) * (gw + 12)
        py = gy + (i // 3) * (gh + 12)
        panel(d, px, py, gw, gh, kick, head, body, ic)

    # ---- in brief band: three stories, one row
    bx, by = mx, 850
    d.text((bx, by), "IN BRIEF", font=font(SANS_B, 22), fill=RED)
    rule(d, bx, by + 30, W - mx, 2)
    briefs = [
        ("MEASLES — ", "9th death as outbreak hits 46 counties."),
        ("GAZA — ", "Oxfam: Gaza has become toxic land."),
        ("IRAN — ", "No US talks until seven conditions are met."),
    ]
    bw = (W - 2 * mx - 2 * 16) // 3
    f_b = font(SANS, 20)
    f_bb = font(SANS_B, 20)
    for i, (lead, rest) in enumerate(briefs):
        cx0 = bx + i * (bw + 16)
        cy0 = by + 40
        lead_w = d.textlength(lead, font=f_bb)
        # first line shares the row with the bold lead-in, later lines
        # use the full column width
        first = wrap(d, rest, f_b, bw - lead_w)
        lines = [first[0]]
        if len(first) > 1:
            lines += wrap(d, " ".join(first[1:]), f_b, bw)
        if len(lines) > 2:
            raise SystemExit("brief overflows: %r" % (lead + rest))
        d.text((cx0, cy0), lead, font=f_bb, fill=INK)
        d.text((cx0 + lead_w, cy0), lines[0], font=f_b, fill=MUTED)
        if len(lines) > 1:
            d.text((cx0, cy0 + 25), lines[1], font=f_b, fill=MUTED)

    # ---- markets strip
    sy = H - 20 - 54
    d.rectangle([mx, sy, W - mx, sy + 54], fill=STRIP_BG)
    strip = ("MARKETS: S&P +4.73% • Nasdaq +6.51% • "
             "Nikkei +3.91% • Gold $3,620 • Brent $86.70")
    for size in (19, 18, 17, 16):
        f_strip = font(SANS_B, size)
        if d.textlength(strip, font=f_strip) <= W - 2 * mx - 32:
            break
    else:
        raise SystemExit("markets strip does not fit at any size")
    d.text((mx + 16, sy + 27 - size // 2), strip, font=f_strip,
           fill=STRIP_TEXT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
