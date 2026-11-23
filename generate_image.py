#!/usr/bin/env python3
"""Draw the front page of Sunday 22 November 2026's world news.

A single 1024x1024 PNG, drawn from scratch with Pillow: masthead, a lead
story on the COP31 collapse, six illustrated story cards, and an
also-today strip. No text is pasted in as an image; every word is set
with Liberation fonts so it stays crisp at any size.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
RED = (155, 28, 28)
BLUE = (31, 78, 121)
GREY = (90, 86, 76)
RULE = (150, 144, 128)
LIGHT = (233, 227, 210)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font, never overflowing."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A simple globe: sea circle, latitude arcs, land blobs, a crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 214, 235),
                 outline=INK, width=3)
    for dy, rw in ((-52, 96), (-18, 116), (18, 116), (52, 96)):
        draw.arc([cx - rw, cy + dy - 26, cx + rw, cy + dy + 26],
                 start=200, end=340, fill=BLUE, width=2)
    draw.arc([cx - 52, cy - r, cx + 52, cy + r], start=270, end=90,
             fill=BLUE, width=2)
    draw.arc([cx - 52, cy - r, cx + 52, cy + r], start=90, end=270,
             fill=BLUE, width=2)
    # Land masses as rough blobs.
    draw.ellipse([cx - 92, cy - 78, cx - 18, cy - 8], fill=(86, 140, 74))
    draw.ellipse([cx - 58, cy - 58, cx - 6, cy - 20], fill=(86, 140, 74))
    draw.ellipse([cx + 8, cy + 12, cx + 88, cy + 82], fill=(106, 158, 88))
    draw.ellipse([cx + 34, cy - 88, cx + 96, cy - 34], fill=(96, 148, 80))
    # A crack running across the globe: the talks broke down.
    crack = [(cx - 70, cy - 96), (cx - 38, cy - 52), (cx - 58, cy - 8),
             (cx - 12, cy + 34), (cx - 34, cy + 78), (cx + 6, cy + 108)]
    draw.line(crack, fill=RED, width=4, joint="curve")


def icon_burst(draw, x, y, s):
    """Orange blast star for the drone strike card."""
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rad = s if i % 2 == 0 else s * 0.45
        pts.append((x + s + rad * math.cos(ang), y + s + rad * math.sin(ang)))
    draw.polygon(pts, fill=(214, 110, 30))
    draw.ellipse([x + s * 0.7, y + s * 0.7, x + s * 1.3, y + s * 1.3],
                 fill=(248, 244, 232))


def icon_bridge(draw, x, y, s):
    """A suspension bridge silhouette."""
    draw.line([(x, y + s * 1.6), (x + 2 * s, y + s * 1.6)], fill=INK, width=4)
    draw.arc([x + s * 0.2, y + s * 0.1, x + s * 1.8, y + s * 1.7],
             start=180, end=360, fill=INK, width=3)
    for fx in (0.35, 0.65, 0.95, 1.25, 1.55):
        draw.line([(x + fx * s, y + s * 0.75), (x + fx * s, y + s * 1.6)],
                  fill=INK, width=2)
    draw.line([(x + s * 0.2, y + s * 0.2), (x + s * 0.2, y + s * 1.6)],
              fill=INK, width=3)
    draw.line([(x + s * 1.8, y + s * 0.2), (x + s * 1.8, y + s * 1.6)],
              fill=INK, width=3)


def icon_ship(draw, x, y, s):
    """A tanker on waves."""
    draw.polygon([(x, y + s), (x + 2 * s, y + s), (x + 1.8 * s, y + s * 1.5),
                  (x + 0.2 * s, y + s * 1.5)], fill=(31, 78, 121))
    draw.rectangle([x + 0.3 * s, y + 0.5 * s, x + 0.8 * s, y + s], fill=RED)
    draw.rectangle([x + 0.9 * s, y + 0.6 * s, x + 1.4 * s, y + s], fill=INK)
    draw.rectangle([x + 1.5 * s, y + 0.35 * s, x + 1.7 * s, y + s], fill=GREY)
    for wy in (1.75, 1.95):
        draw.arc([x, y + wy * s, x + s, y + (wy + 0.25) * s],
                 start=0, end=180, fill=BLUE, width=3)
        draw.arc([x + s, y + wy * s, x + 2 * s, y + (wy + 0.25) * s],
                 start=0, end=180, fill=BLUE, width=3)


def icon_flame(draw, x, y, s):
    """A flame built from two polygons, no glyph needed."""
    outer = [(x + s, y), (x + 1.7 * s, y + 0.9 * s), (x + 1.9 * s, y + 1.5 * s),
             (x + 1.4 * s, y + 2 * s), (x + 0.6 * s, y + 2 * s),
             (x + 0.1 * s, y + 1.5 * s), (x + 0.3 * s, y + 0.9 * s)]
    draw.polygon(outer, fill=(214, 110, 30))
    inner = [(x + s, y + 0.7 * s), (x + 1.4 * s, y + 1.3 * s),
             (x + 1.2 * s, y + 1.9 * s), (x + 0.8 * s, y + 1.9 * s),
             (x + 0.6 * s, y + 1.3 * s)]
    draw.polygon(inner, fill=(240, 190, 40))


def icon_badge(draw, x, y, s):
    """A sheriff-style badge star for the cartel capture."""
    import math
    pts = []
    for i in range(10):
        ang = math.pi * i / 5 - math.pi / 2
        rad = s if i % 2 == 0 else s * 0.55
        pts.append((x + s + rad * math.cos(ang), y + s + rad * math.sin(ang)))
    draw.polygon(pts, fill=(31, 78, 121))
    draw.ellipse([x + s * 0.65, y + s * 0.65, x + s * 1.35, y + s * 1.35],
                 fill=(248, 244, 232))


def icon_factory(draw, x, y, s):
    """A factory with a sawtooth roof and a smoking chimney."""
    draw.polygon([(x, y + s), (x + 0.5 * s, y + 0.5 * s),
                  (x + s, y + s), (x + 1.5 * s, y + 0.5 * s),
                  (x + 2 * s, y + s), (x + 2 * s, y + 2 * s),
                  (x, y + 2 * s)], fill=GREY)
    draw.rectangle([x + 1.7 * s, y, x + 2 * s, y + s], fill=INK)
    for sx, sy, sr in ((x + 1.85 * s, y - 0.1 * s, 7),
                       (x + 2.05 * s, y - 0.3 * s, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(120, 118, 110))


def card(draw, x, y, w, h, kicker, headline, body, icon):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    draw.rectangle([x, y, x + w, y + 4], fill=RED)
    ix, iy, isize = x + 14, y + 16, 22
    icon(draw, ix, iy, isize)
    tx = x + 14 + 2 * isize + 12
    draw.text((tx, y + 14), kicker, font=font(SANS_B, 13), fill=RED)
    hy = para(draw, tx, y + 36, headline, font(SANS_B, 19), w - (tx - x) - 14,
              leading=23)
    para(draw, x + 14, y + 96, body, font(SANS, 14), w - 28, fill=GREY,
         leading=18)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 36
    right = W - mx

    # ---- Masthead -----------------------------------------------------
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF_B, 56)
    draw.text(((W - draw.textlength(title, font=tf)) / 2, 26), title,
              font=tf, fill=INK)
    hline(draw, mx, right, 104, width=3)
    date = "SUNDAY 22 NOVEMBER 2026"
    df = font(SANS_B, 38)
    draw.text(((W - draw.textlength(date, font=df)) / 2, 116), date,
              font=df, fill=RED)
    sub = "T H E   D A Y ' S   W O R L D   N E W S   —   I N   O N E   P I C T U R E"
    sf = font(SANS, 14)
    draw.text(((W - draw.textlength(sub, font=sf)) / 2, 164), sub,
              font=sf, fill=GREY)
    hline(draw, mx, right, 188, width=2)

    # ---- Lead story ---------------------------------------------------
    ly = 206
    draw.text((mx, ly), "CLIMATE SUMMIT  •  ANTALYA, TURKEY",
              font=font(SANS_B, 15), fill=RED)
    hy = para(draw, mx, ly + 28,
              "CLIMATE TALKS COLLAPSE AFTER A RECORD 48 HOURS OF OVERTIME",
              font(SERIF_B, 34), 620, leading=40)
    para(draw, mx, hy + 10,
         "Nations at the UN COP31 summit failed to agree a final deal on "
         "Sunday, as a standoff over phasing out fossil fuels blocked any "
         "consensus after two weeks of talks. The UN chief said he was "
         "deeply disappointed.",
         font(SANS, 17), 620, fill=INK, leading=23)
    draw_globe(draw, 826, 318, 112)
    cap = "COP31 ends with no deal"
    cf = font(SANS, 14)
    draw.text((826 - draw.textlength(cap, font=cf) / 2, 446), cap,
              font=cf, fill=GREY)
    hline(draw, mx, right, 486, width=2)

    # ---- Six story cards ----------------------------------------------
    cards = [
        ("UKRAINE", "DRONES HIT HOMES NEAR KYIV",
         "Russia fired 186 drones overnight; a five-storey block was hit "
         "and three people were killed.", icon_burst),
        ("UKRAINE", "KERCH BRIDGE HIT AGAIN",
         "Ukraine struck the railway section of the bridge to Crimea for a "
         "third time.", icon_bridge),
        ("THE GULF", "TANKERS STRUCK NEAR HORMUZ",
         "Iran hit three tankers as its standoff with the United States "
         "over a naval blockade deepened.", icon_ship),
        ("WEST BANK", "SETTLER ARSON CONDEMNED",
         "Settlers torched cars and homes overnight; Israel's opposition "
         "leader called it \u201cJewish terrorism\u201d.", icon_flame),
        ("MEXICO", "CARTEL BOSS CAPTURED",
         "\u201cEl Chapo Isidro\u201d was seized in Sinaloa after a gun "
         "battle that left 11 people dead.", icon_badge),
        ("INDONESIA", "FACTORY FIRE: DOZENS MISSING",
         "A blaze tore through a candy factory in Banten; three were "
         "confirmed dead and about 36 missing.", icon_factory),
    ]
    cw, ch, gap = 306, 176, 17
    for i, (kick, head, body, icon) in enumerate(cards):
        cx = mx + (i % 3) * (cw + gap)
        cy = 504 + (i // 3) * (ch + gap)
        card(draw, cx, cy, cw, ch, kick, head, body, icon)

    # ---- Also today ----------------------------------------------------
    ay = 892
    hline(draw, mx, right, ay, width=2)
    draw.text((mx, ay + 12), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    also = [
        ("ISRAEL", "Coalition talks fail: Netanyahu and Eisenkot meet for "
                   "four hours and reach no deal."),
        ("NIGERIA", "A boat carrying mourners to a funeral capsizes in "
                    "Bayelsa; at least 24 people drown."),
        ("ASIA", "Nepal's PM begins his first visit to India; China eases "
                 "margin rules for share buyers."),
    ]
    for i, (kick, text) in enumerate(also):
        ax = mx + i * (cw + gap)
        draw.text((ax, ay + 38), kick, font=font(SANS_B, 13), fill=RED)
        para(draw, ax, ay + 58, text, font(SANS, 13), cw, fill=INK,
             leading=17)
    hline(draw, mx, right, 988, width=1, fill=RULE)
    foot = ("Events of Sunday 22 November 2026, as reported by AP, Reuters, "
            "Al Jazeera, The Hindu and WION.")
    ff = font(SANS, 11)
    draw.text(((W - draw.textlength(foot, font=ff)) / 2, 996), foot,
              font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
