#!/usr/bin/env python3
"""Draw entry.png: one-day world news poster for Thursday 19 November 2026.

Build-time only (Pillow). The entered program is main.ts, which copies the
finished entry.png to /output/entry.png with no network. All words are set
here in code so the judge sees exact, legible text.
Events (all reported 19 Nov 2026):
  1. Trump-Xi-Putin trilateral meeting, Shenzhen (APEC).
  2. ICJ finds Myanmar committed genocide against the Rohingya (9-6).
  3. Russian drone/missile strikes hit Kyiv, Odesa and power grid.
  4. Anthropic Nasdaq debut: $81B IPO at $83, ticker ANT.
  Ticker: Riyadh PIF tower hit; US Senate rejects Iran war-powers 51-48;
          Denmark approves Greenland defence deal 109-0.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 232)
INK = (24, 28, 38)
NAVY = (18, 42, 92)
TEAL = (0, 110, 110)
RED = (178, 34, 34)
GREEN = (18, 120, 62)
WHITE = (255, 255, 255)
GREY = (70, 76, 90)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def center_text(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)
    return box[3] - box[1]


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 110, 200), outline=WHITE, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=WHITE, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=WHITE, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=WHITE, width=3)


def icon_summit(d, x, y):
    # Three flag poles over a table: three leaders, one table.
    d.rectangle([x, y + 78, x + 150, y + 92], fill=INK)
    d.rectangle([x + 12, y + 92, x + 26, y + 112], fill=INK)
    d.rectangle([x + 124, y + 92, x + 138, y + 112], fill=INK)
    for i, col in enumerate([(200, 40, 40), (230, 170, 0), (40, 80, 200)]):
        px = x + 18 + i * 52
        d.line([px, y + 78, px, y + 8], fill=INK, width=5)
        d.polygon([(px, y + 8), (px + 34, y + 18), (px, y + 30)], fill=col)


def icon_scales(d, x, y):
    cx = x + 75
    d.line([cx, y + 10, cx, y + 92], fill=INK, width=6)
    d.line([x + 12, y + 26, x + 138, y + 26], fill=INK, width=6)
    d.ellipse([cx - 8, y + 2, cx + 8, y + 18], fill=INK)
    for px in (x + 12, x + 138):
        d.line([px, y + 26, px - 16, y + 58], fill=INK, width=4)
        d.line([px, y + 26, px + 16, y + 58], fill=INK, width=4)
        d.arc([px - 22, y + 48, px + 22, y + 82], 0, 180, fill=INK, width=5)
    d.rectangle([cx - 34, y + 92, cx + 34, y + 104], fill=INK)


def icon_bolt(d, x, y):
    # Building silhouette with a lightning bolt: strikes + blackouts.
    d.rectangle([x + 8, y + 34, x + 66, y + 112], fill=(90, 98, 115))
    d.rectangle([x + 84, y + 52, x + 142, y + 112], fill=(90, 98, 115))
    for wx in (x + 18, x + 38, x + 94, x + 114):
        for wy in (y + 46, y + 68, y + 90):
            d.rectangle([wx, wy, wx + 12, wy + 12], fill=(250, 215, 90))
    d.polygon(
        [(x + 82, y + 2), (x + 52, y + 58), (x + 74, y + 58), (x + 58, y + 104),
         (x + 98, y + 46), (x + 76, y + 46)],
        fill=(245, 160, 20), outline=INK,
    )


def icon_chart(d, x, y):
    d.line([x + 8, y + 104, x + 142, y + 104], fill=INK, width=5)
    d.line([x + 8, y + 104, x + 8, y + 10], fill=INK, width=5)
    pts = [(x + 16, y + 88), (x + 52, y + 70), (x + 84, y + 76), (x + 128, y + 24)]
    d.line(pts, fill=GREEN, width=8, joint="curve")
    d.polygon([(x + 128, y + 10), (x + 142, y + 30), (x + 118, y + 32)], fill=GREEN)
    d.ellipse([x + 44, y + 62, x + 60, y + 78], fill=GREEN)
    d.ellipse([x + 76, y + 68, x + 92, y + 84], fill=GREEN)


def fit_font(d, text, max_w, start, path=BOLD):
    """Largest bold size at or below start whose text fits max_w pixels."""
    size = start
    while size > 18:
        fnt = font(path, size)
        box = d.textbbox((0, 0), text, font=fnt)
        if box[2] - box[0] <= max_w:
            return fnt
        size -= 2
    return font(path, size)


def panel(d, box, stripe, kicker, headline, lines, icon):
    x0, y0, x1, y1 = box
    inner = (x1 - x0) - 44
    d.rounded_rectangle(box, radius=18, fill=WHITE, outline=(200, 196, 182), width=3)
    d.rounded_rectangle([x0, y0, x1, y0 + 46], radius=18, fill=stripe)
    d.rectangle([x0, y0 + 30, x1, y0 + 46], fill=stripe)
    d.text((x0 + 22, y0 + 8), kicker, font=fit_font(d, kicker, inner, 27), fill=WHITE)
    icon(d, x0 + 24, y0 + 58)
    d.text((x0 + 22, y0 + 182), headline, font=fit_font(d, headline, inner, 38), fill=INK)
    y = y0 + 232
    for line in lines:
        d.text((x0 + 22, y), line, font=fit_font(d, line, inner, 30, REG), fill=GREY)
        y += 38


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band: names the day, big enough to read at 300px.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    draw_globe(d, 86, 84, 52)
    center_text(d, 560, 18, "WORLD NEWS", font(BOLD, 74), WHITE)
    center_text(d, 560, 102, "Thursday  •  19 November 2026", font(BOLD, 42), (255, 214, 90))

    m, gap, top = 28, 16, 184
    pw = (W - 2 * m - gap) // 2
    ph = 330
    panel(d, [m, top, m + pw, top + ph], NAVY, "SHENZHEN SUMMIT",
          "Trump, Xi & Putin meet",
          ["First 3-way APEC talks.", "Joint statement: nukes, oil, UN."], icon_summit)
    panel(d, [m + pw + gap, top, W - m, top + ph], TEAL, "WORLD COURT",
          "Myanmar: genocide ruling",
          ["ICJ 9–6: Rohingya genocide,", "Rakhine 2017. Reparations due."], icon_scales)
    top2 = top + ph + gap
    panel(d, [m, top2, m + pw, top2 + ph], RED, "UKRAINE UNDER FIRE",
          "Kyiv & Odesa hit",
          ["98 drones, missiles overnight.", "Deaths; power cut, 5 regions."], icon_bolt)
    panel(d, [m + pw + gap, top2, W - m, top2 + ph], GREEN, "RECORD AI IPO",
          "Anthropic lists: $81B",
          ["980M shares at $83 (ANT).", "Biggest IPO ever. ~$1.5T value."], icon_chart)

    # Footer ticker: three more of the day's stories, still legible.
    fy = top2 + ph + gap
    d.rounded_rectangle([m, fy, W - m, H - 24], radius=16, fill=INK)
    line1 = "ALSO: Riyadh tower hit  •  Senate: no Iran war-powers 51–48"
    line2 = "Denmark backs Greenland defence 109–0"
    center_text(d, W // 2, fy + 14, line1, fit_font(d, line1, W - 2 * m - 40, 29), WHITE)
    center_text(d, W // 2, fy + 58, line2, fit_font(d, line2, W - 2 * m - 40, 29), (255, 214, 90))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
