#!/usr/bin/env python3
"""Front page for one day's world news: Sunday 22 November 2026.

Everything on the page is drawn with Pillow at build time — masthead,
the COP31 lead, six story cards with small spot illustrations, and an
also-today strip — then saved as a single 1024x1024 entry.png.
"""

import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (250, 246, 236)
INK = (28, 26, 23)
ACCENT = (168, 32, 26)
NAVY = (34, 74, 110)
MUTED = (96, 91, 80)
HAIR = (172, 165, 146)
SKY = (186, 218, 238)
LEAF = (92, 146, 78)
FIRE = (216, 112, 30)
GOLD = (240, 190, 40)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = f"{FONT_DIR}/LiberationSerif-Regular.ttf"
SERIF_BOLD = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SANS = f"{FONT_DIR}/LiberationSans-Regular.ttf"
SANS_BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, path, size, fill):
    f = fnt(path, size)
    draw.text((cx - draw.textlength(text, font=f) / 2, y), text, font=f,
              fill=fill)


def wrapped_lines(draw, text, f, max_width):
    """Split text into lines that fit max_width in the given font."""
    lines = []
    line = ""
    for word in text.split():
        trial = word if line == "" else line + " " + word
        if line == "" or draw.textlength(trial, font=f) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def paragraph(draw, x, y, text, path, size, max_width, fill=INK, step=None):
    f = fnt(path, size)
    if step is None:
        step = round(size * 1.3)
    for line in wrapped_lines(draw, text, f, max_width):
        draw.text((x, y), line, font=f, fill=fill)
        y += step
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([x0, y, x1, y], fill=fill, width=width)


def star_points(cx, cy, outer, inner, count, phase=-math.pi / 2):
    pts = []
    for i in range(count * 2):
        r = outer if i % 2 == 0 else inner
        a = phase + math.pi * i / count
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_blast(d, x, y):
    d.polygon(star_points(x + 27, y + 27, 27, 12, 8), fill=FIRE)
    d.ellipse([x + 18, y + 18, x + 36, y + 36], fill=PAPER)


def icon_span(d, x, y):
    d.line([x + 2, y + 46, x + 52, y + 46], fill=INK, width=4)
    for px in (10, 44):
        d.line([x + px, y + 8, x + px, y + 46], fill=INK, width=3)
    d.arc([x + 2, y - 6, x + 52, y + 46], start=180, end=360, fill=INK,
          width=3)
    for fx in (18, 27, 36):
        d.line([x + fx, y + 30, x + fx, y + 46], fill=INK, width=2)


def icon_tanker(d, x, y):
    d.polygon([(x + 2, y + 30), (x + 52, y + 30), (x + 46, y + 42),
               (x + 8, y + 42)], fill=NAVY)
    d.rectangle([x + 10, y + 18, x + 24, y + 30], fill=ACCENT)
    d.rectangle([x + 27, y + 21, x + 39, y + 30], fill=INK)
    d.rectangle([x + 42, y + 12, x + 47, y + 30], fill=MUTED)
    for wx in (2, 29):
        d.arc([x + wx, y + 44, x + wx + 25, y + 54], start=0, end=180,
              fill=NAVY, width=3)


def icon_flame(d, x, y):
    d.polygon([(x + 27, y + 2), (x + 42, y + 24), (x + 46, y + 38),
               (x + 38, y + 52), (x + 16, y + 52), (x + 8, y + 38),
               (x + 13, y + 22)], fill=FIRE)
    d.polygon([(x + 27, y + 22), (x + 36, y + 36), (x + 32, y + 50),
               (x + 22, y + 50), (x + 18, y + 36)], fill=GOLD)


def icon_badge(d, x, y):
    d.polygon(star_points(x + 27, y + 27, 26, 15, 5), fill=NAVY)
    d.ellipse([x + 18, y + 18, x + 36, y + 36], fill=PAPER)


def icon_plant(d, x, y):
    d.polygon([(x + 2, y + 26), (x + 15, y + 14), (x + 28, y + 26),
               (x + 41, y + 14), (x + 52, y + 26), (x + 52, y + 52),
               (x + 2, y + 52)], fill=MUTED)
    d.rectangle([x + 42, y + 2, x + 50, y + 20], fill=INK)
    for cx, cy, r in ((48, 0, 5), (54, -6, 6)):
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(128, 124, 114))


def icon_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK,
              width=3)
    for frac in (-0.5, 0.0, 0.5):
        yy = cy + frac * r
        half = r * math.sqrt(1 - frac * frac)
        d.line([cx - half, yy, cx + half, yy], fill=NAVY, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=NAVY,
              width=2)
    d.ellipse([cx - 70, cy - 66, cx - 14, cy - 14], fill=LEAF)
    d.ellipse([cx + 16, cy + 18, cx + 78, cy + 74], fill=LEAF)
    d.ellipse([cx + 30, cy - 80, cx + 84, cy - 30], fill=LEAF)
    zigzag = [(cx - 58, cy - 88), (cx - 30, cy - 44), (cx - 50, cy - 2),
              (cx - 14, cy + 40), (cx - 30, cy + 80), (cx + 2, cy + 100)]
    d.line(zigzag, fill=ACCENT, width=4, joint="curve")


STORIES = [
    ("UKRAINE WAR", "RUSSIAN DRONES STRIKE HOMES OUTSIDE KYIV",
     "An overnight barrage of 186 drones hit a five-storey apartment "
     "block in the Kyiv region, killing three people.", icon_blast),
    ("UKRAINE WAR", "KERCH BRIDGE RAIL LINK HIT A THIRD TIME",
     "Kyiv's forces struck the railway span of the bridge linking "
     "Russia to occupied Crimea once again.", icon_span),
    ("MIDDLE EAST", "THREE TANKERS HIT NEAR STRAIT OF HORMUZ",
     "Iran struck three oil tankers as its confrontation with the US "
     "over a naval blockade sharpened.", icon_tanker),
    ("WEST BANK", "SETTLER ARSON DENOUNCED AS TERRORISM",
     "Cars and houses were set alight overnight; Gadi Eisenkot "
     "condemned the attacks as \u201cJewish terrorism\u201d.", icon_flame),
    ("MEXICO", "CARTEL FIGURE \u2018EL CHAPO ISIDRO\u2019 SEIZED",
     "Mexican forces captured the Sinaloa cartel boss after a gun "
     "battle that left 11 people dead.", icon_badge),
    ("INDONESIA", "CANDY FACTORY BLAZE LEAVES DOZENS MISSING",
     "Fire swept through a Banten candy factory; three deaths are "
     "confirmed and about 36 people are still missing.", icon_plant),
]

BRIEFS = [
    ("ISRAEL POLITICS", "Netanyahu\u2013Eisenkot coalition talks end "
     "after four hours with no agreement."),
    ("NIGERIA", "A boat ferrying funeral guests capsizes in Bayelsa; "
     "at least 24 people drown."),
    ("ASIA", "Nepal's prime minister opens his first visit to India; "
     "Beijing loosens margin-lending rules."),
]


def story_card(d, x, y, w, h, section, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], outline=HAIR, width=1)
    d.rectangle([x, y, x + w, y + 4], fill=ACCENT)
    icon(d, x + 12, y + 14)
    tx = x + 78
    d.text((tx, y + 13), section, font=fnt(SANS_BOLD, 13), fill=ACCENT)
    hy = paragraph(d, tx, y + 34, headline, SANS_BOLD, 19,
                   w - (tx - x) - 12, step=23)
    paragraph(d, x + 12, max(y + 106, hy + 4), body, SANS, 14, w - 24,
              fill=MUTED, step=18)


def build_page():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    left, right = 40, SIZE - 40

    centered(d, SIZE / 2, 28, "THE WORLD IN ONE PAGE", SERIF_BOLD, 54, INK)
    rule(d, left, right, 100, width=3)
    centered(d, SIZE / 2, 112, "SUNDAY 22 NOVEMBER 2026", SANS_BOLD, 40,
             ACCENT)
    centered(d, SIZE / 2, 166,
             "T H E   D A Y ' S   W O R L D   N E W S   —   I N   O N E   "
             "P I C T U R E", SANS, 14, MUTED)
    rule(d, left, right, 192, width=2)

    d.text((left, 210), "CLIMATE  •  ANTALYA, TURKEY",
           font=fnt(SANS_BOLD, 15), fill=ACCENT)
    hy = paragraph(d, left, 238,
                   "COP31 CLIMATE TALKS BREAK DOWN AFTER 48 HOURS OF "
                   "OVERTIME", SERIF_BOLD, 33, 600, step=39)
    paragraph(d, left, hy + 12,
              "Two weeks of UN climate talks in Antalya ended without a "
              "final agreement on Sunday, deadlocked over wording on "
              "phasing out fossil fuels. The UN secretary-general said "
              "he was deeply disappointed by the outcome.",
              SANS, 17, 600, step=23)
    icon_globe(d, 824, 322, 106)
    centered(d, 824, 442, "No deal at COP31", SANS, 14, MUTED)
    rule(d, left, right, 482, width=2)

    cw, chh, gap = 301, 172, 16
    for i, (section, headline, body, icon) in enumerate(STORIES):
        story_card(d, left + (i % 3) * (cw + gap), 500 + (i // 3) * (chh + gap),
                   cw, chh, section, headline, body, icon)

    ay = 876
    rule(d, left, right, ay, width=2)
    d.text((left, ay + 12), "ALSO TODAY", font=fnt(SANS_BOLD, 15),
           fill=ACCENT)
    for i, (section, text) in enumerate(BRIEFS):
        bx = left + i * (cw + gap)
        d.text((bx, ay + 40), section, font=fnt(SANS_BOLD, 13), fill=ACCENT)
        paragraph(d, bx, ay + 60, text, SANS, 13, cw, step=17)
    rule(d, left, right, 986, fill=HAIR, width=1)
    centered(d, SIZE / 2, 994,
             "Events of Sunday 22 November 2026, as reported by AP, "
             "Reuters, Al Jazeera, The Hindu and WION.", SANS, 11, MUTED)
    return img


if __name__ == "__main__":
    page = build_page()
    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)
