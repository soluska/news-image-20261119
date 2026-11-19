#!/usr/bin/env python3
"""THE WORLD IN ONE DAY -- front page of Thursday 19 November 2026.

A newspaper front page summarising the day's world news in a single image.
Everything is drawn in code with Pillow: vector shapes, flags, icons and
real typography (DejaVu fonts, bundled in fonts/). No photographs, no AI
images, no network. Fully deterministic: two runs produce identical bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas ---
W, H = 1024, 1024

PAPER = (247, 243, 232)   # newsprint cream
INK = (17, 17, 17)        # near-black ink
RED = (164, 30, 34)       # headline accent red
GREY = (70, 70, 70)
WHITE = (255, 255, 255)
SAND = (232, 222, 196)

BASE = os.path.dirname(os.path.abspath(__file__))

img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)


def load_font(name, size):
    for cand in (os.path.join(BASE, "fonts", name),
                 "/usr/share/fonts/truetype/dejavu/" + name):
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def F(kind, size):
    return load_font({
        "serif_b": "DejaVuSerif-Bold.ttf",
        "serif": "DejaVuSerif.ttf",
        "sans_b": "DejaVuSans-Bold.ttf",
        "sans": "DejaVuSans.ttf",
    }[kind], size)


def tw(text, font):
    return dr.textlength(text, font=font)


def text(x, y, s, font, color=INK, align="left"):
    if align == "center":
        x = x - tw(s, font) / 2
    elif align == "right":
        x = x - tw(s, font)
    dr.text((x, y), s, font=font, fill=color)
    return x + tw(s, font)


def wrap_px(s, font, max_w):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, font, color, max_w, lh):
    for ln in wrap_px(s, font, max_w):
        dr.text((x, y), ln, font=font, fill=color)
        y += lh
    return y


# ------------------------------------------------------------ draw helpers --
def rect(x, y, w, h, c):
    dr.rectangle([x, y, x + w - 1, y + h - 1], fill=c)


def rect_outline(x, y, w, h, c, width=1):
    dr.rectangle([x, y, x + w - 1, y + h - 1], outline=c, width=width)


def hline(x, y, w, c=INK, width=1):
    dr.line([x, y, x + w - 1, y], fill=c, width=width)


def vline(x, y, h, c=INK, width=1):
    dr.line([x, y, x, y + h - 1], fill=c, width=width)


def line(x0, y0, x1, y1, c, width=1):
    dr.line([x0, y0, x1, y1], fill=c, width=width)


def circle_fill(cx, cy, r, c):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def circle_outline(cx, cy, r, c, width=1):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=width)


def poly(pts, c):
    dr.polygon(pts, fill=c)


def double_rule(x, y, w, c=INK):
    rect(x, y, w, 2, c)
    rect(x, y + 4, w, 1, c)


def star(cx, cy, r, c):
    """Small 5-point star (flag use)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    poly(pts, c)

# ------------------------------------------------------------------ flags ---
def flag_china(x, y, w, h):
    rect(x, y, w, h, (222, 41, 16))
    star(x + w * 0.16, y + h * 0.26, h * 0.17, (255, 222, 0))
    for dx, dy in ((0.30, 0.13), (0.34, 0.27), (0.34, 0.42), (0.29, 0.55)):
        star(x + w * dx, y + h * dy, h * 0.075, (255, 222, 0))


def flag_usa(x, y, w, h):
    rect(x, y, w, h, WHITE)
    sh = h / 13.0
    for i in range(0, 13, 2):
        rect(x, int(y + i * sh), w, int(sh) + 1, (178, 34, 52))
    cw, chh = int(w * 0.42), int(sh * 7)
    rect(x, y, cw, chh, (60, 59, 110))
    for r in range(4):
        for c in range(5):
            circle_fill(x + 5 + c * (cw - 8) // 4, y + 4 + r * (chh - 7) // 3,
                        1, WHITE)


def flag_russia(x, y, w, h):
    rect(x, y, w, h // 3 + 1, WHITE)
    rect(x, y + h // 3, w, h // 3 + 1, (0, 57, 166))
    rect(x, y + 2 * h // 3, w, h - 2 * h // 3, (213, 43, 30))
    rect_outline(x, y, w, h, (150, 150, 150))


# ------------------------------------------------------------- lead scene ---
def draw_summit_scene(x, y, w, h):
    """Shenzhen skyline at dusk, three flags of the summit in front."""
    # dusk sky: horizontal bands, deep blue to warm orange
    top, mid, low = (38, 54, 96), (120, 84, 120), (238, 140, 74)
    for i in range(h - 60):
        t = i / max(1, h - 61)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(mid[k] + (low[k] - mid[k]) * u) for k in range(3))
        hline(x, y + i, w, c)
    # sun disc low on the right
    circle_fill(x + w - 92, y + h - 118, 34, (255, 196, 86))
    circle_fill(x + w - 92, y + h - 118, 26, (255, 220, 130))
    # skyline silhouette (Shenzhen: one tall tapered tower among blocks)
    base = y + h - 60
    sil = (24, 26, 40)
    towers = [(0, 52, 66), (58, 40, 92), (104, 34, 58), (196, 30, 78),
              (232, 44, 50), (282, 36, 96), (324, 52, 62), (382, 40, 84)]
    for dx, twd, th in towers:
        rect(x + dx, base - th, twd, th, sil)
    # tapered landmark tower
    poly([(x + 138, base), (x + 152, base - 148), (x + 162, base - 148),
          (x + 176, base)], sil)
    rect(x + 154, base - 158, 6, 12, sil)
    # lit windows
    for dx, dy in ((20, 30), (70, 55), (120, 22), (210, 40), (250, 18),
                    (300, 60), (345, 30), (400, 45), (36, 48), (292, 26)):
        rect(x + dx, base - dy - 14, 4, 5, (255, 214, 120))
    # ground
    rect(x, base, w, 60, (16, 18, 28))
    # three flag poles with the summit flags
    fw, fh = 96, 58
    for i, draw_flag in enumerate((flag_usa, flag_china, flag_russia)):
        px0 = x + 42 + i * 148
        vline(px0, y + 26, base - y - 26 + 8, (230, 230, 235), width=3)
        circle_fill(px0, y + 24, 4, (255, 210, 90))
        draw_flag(px0 + 4, y + 30, fw, fh)
        rect_outline(px0 + 4, y + 30, fw, fh, (20, 20, 20))
    # caption bar
    rect(x, y + h - 26, w, 26, INK)
    text(x + w // 2, y + h - 21, "SHENZHEN, CHINA — THE APEC SUMMIT",
         F("sans_b", 14), WHITE, align="center")


# -------------------------------------------------------------- card icons --
def icon_bridge(x, y, w, h):
    """Broken bridge over waves, explosion at the break."""
    rect(x, y, w, h, (206, 224, 236))
    rect(x, y + h - 10, w, 10, (31, 78, 121))
    deck = y + h - 24
    rect(x + 2, deck, w // 2 - 8, 5, (90, 96, 104))
    rect(x + w // 2 + 8, deck, w // 2 - 10, 5, (90, 96, 104))
    poly([(x + w // 2 - 6, deck), (x + w // 2 + 2, deck + 4),
          (x + w // 2 + 10, y + h - 12), (x + w // 2 + 2, y + h - 13)],
         (60, 64, 70))
    ex, ey = x + w // 2 - 2, deck - 8
    for dx, dy in ((0, -8), (6, -5), (8, 2), (4, 7), (-4, 7), (-8, 2),
                   (-6, -5)):
        line(ex, ey, ex + dx, ey + dy, (224, 110, 30), width=2)
    circle_fill(ex, ey, 3, (240, 200, 40))


def icon_gulf(x, y, w, h):
    """Missile over the sea, oil derrick, target ring on an island."""
    rect(x, y, w, h, (238, 226, 208))
    rect(x, y + h - 10, w, 10, (31, 78, 121))
    # oil derrick, left
    dx = x + 8
    line(dx + 4, y + h - 10, dx + 10, y + 6, INK, width=2)
    line(dx + 20, y + h - 10, dx + 14, y + 6, INK, width=2)
    line(dx + 10, y + 6, dx + 14, y + 6, INK, width=2)
    line(dx + 7, y + h - 20, dx + 17, y + h - 20, INK, width=1)
    # island + target, right
    ix, iy = x + w - 16, y + h - 12
    circle_fill(ix, iy, 8, (190, 170, 120))
    circle_outline(ix, iy, 5, RED, width=1)
    # missile, diagonal
    line(x + 30, y + h - 16, x + w - 26, y + 8, INK, width=4)
    line(x + 30, y + h - 16, x + w - 26, y + 8, (240, 240, 240), width=2)
    poly([(x + 26, y + h - 12), (x + 34, y + h - 20), (x + 24, y + h - 24)],
         (224, 110, 30))


def icon_vice(x, y, w, h):
    """Vice City: neon sunset disc and palm silhouettes."""
    for i in range(h):
        t = i / max(1, h - 1)
        c = (int(64 + (240 - 64) * t), int(30 + (110 - 30) * t),
             int(120 + (170 - 120) * t))
        hline(x, y + i, w, c)
    circle_fill(x + w // 2, y + h - 8, 13, (255, 214, 90))
    # palms
    for px0, flip in ((x + 12, 1), (x + w - 12, -1)):
        line(px0, y + h, px0 + 5 * flip, y + 12, (20, 16, 28), width=3)
        tx0, ty0 = px0 + 5 * flip, y + 12
        for dx, dy in ((-11, -4), (-6, -8), (0, -9), (7, -7), (11, -3)):
            line(tx0, ty0, tx0 + dx * flip, ty0 + dy, (20, 16, 28), width=2)


def icon_court(x, y, w, h):
    """Peace Palace tower: gabled block with a tall spire."""
    rect(x, y, w, h, (216, 222, 232))
    bx, bw = x + w // 2 - 16, 32
    rect(bx, y + 14, bw, h - 14, (70, 84, 110))
    poly([(bx - 4, y + 14), (bx + bw + 4, y + 14), (bx + bw // 2, y + 2)],
         (50, 60, 84))
    rect(bx + bw // 2 - 3, y + 4, 6, h - 18, (50, 60, 84))
    poly([(bx + bw // 2 - 6, y + 4), (bx + bw // 2 + 6, y + 4),
          (bx + bw // 2, y - 4)], (50, 60, 84))
    rect(bx + bw // 2 - 3, y + 22, 6, 8, (255, 220, 130))
    rect(x + 4, y + h - 12, 14, 12, (70, 84, 110))
    rect(x + w - 18, y + h - 12, 14, 12, (70, 84, 110))


def icon_cyclone(x, y, w, h):
    """Cyclone spiral over waves."""
    import math
    rect(x, y, w, h, (210, 228, 240))
    cx, cy = x + w // 2, y + h // 2 - 3
    for r in (13, 9, 5):
        dr.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
               fill=(31, 78, 121), width=2)
        dr.arc([cx - r, cy - r, cx + r, cy + r], 200, 480,
               fill=(90, 150, 190), width=2)
    circle_fill(cx, cy, 2, (31, 78, 121))
    for sx in range(x + 4, x + w - 12, 14):
        dr.arc([sx, y + h - 9, sx + 12, y + h - 2], 180, 360,
               fill=(31, 78, 121), width=1)


def icon_climate(x, y, w, h):
    """Globe with a rising thermometer: talks under a heating planet."""
    rect(x, y, w, h, (222, 238, 224))
    cx, cy, r = x + 24, y + h // 2, 14
    circle_fill(cx, cy, r, (90, 160, 210))
    circle_outline(cx, cy, r, (40, 110, 60), width=1)
    poly([(cx - 8, cy - 8), (cx - 2, cy - 10), (cx - 3, cy - 3),
          (cx - 9, cy - 2)], (60, 160, 90))
    poly([(cx + 3, cy + 4), (cx + 10, cy + 2), (cx + 9, cy + 9),
          (cx + 2, cy + 9)], (60, 160, 90))
    # thermometer
    tx0 = x + w - 18
    rect(tx0, y + 5, 6, h - 14, WHITE)
    rect_outline(tx0, y + 5, 6, h - 14, INK)
    rect(tx0 + 1, y + h // 2, 4, h // 2 - 10, RED)
    circle_fill(tx0 + 3, y + h - 7, 6, RED)

# ------------------------------------------------------------------ layout --
MX = 32
CW = 960


def draw_masthead():
    text(W // 2, 26, "THE WORLD IN ONE DAY", F("serif_b", 62), INK,
         align="center")
    double_rule(MX, 100, CW)
    text(W // 2, 112, "THURSDAY 19 NOVEMBER 2026", F("sans_b", 37), RED,
         align="center")
    text(W // 2, 156, "ONE DAY · EVERY STORY THAT MATTERED · GLOBAL EDITION",
         F("sans", 15), GREY, align="center")
    double_rule(MX, 180, CW)


def draw_lead():
    y0 = 194
    lx, lw = MX, 484
    text(lx, y0, "LEAD STORY · APEC SUMMIT, SHENZHEN", F("sans_b", 19), RED)
    text(lx, y0 + 27, "TRUMP, XI & PUTIN", F("sans_b", 45), INK)
    text(lx, y0 + 80, "FIRST THREE-WAY SUMMIT", F("sans_b", 31), RED)
    summary = ("The presidents of the United States, China and Russia met in "
               "Shenzhen for their first-ever three-way summit, on the "
               "sidelines of APEC. Ukraine topped the agenda; Trump saw "
               "Putin and Xi separately before the three sat down together.")
    end_y = para(lx, y0 + 124, summary, F("sans", 19), (40, 40, 40), lw, 24)
    fy = y0 + 252
    rect(lx, fy, lw, 24, SAND)
    rect_outline(lx, fy, lw, 24, INK)
    text(lx + lw // 2, fy + 4, "UKRAINE · ARMS CONTROL · TRADE",
         F("sans_b", 14), INK, align="center")
    if end_y > fy - 4:
        print("LEAD OVERFLOW", end_y, fy)
    draw_summit_scene(532, y0, 460, 276)
    rect_outline(532, y0, 460, 276, INK)


def draw_card(x, y, w, h, icon_fn, band, kicker, headline, detail):
    rect_outline(x, y, w, h, INK)
    rect(x, y, w, 44, band)
    icon_fn(x + 6, y + 4, 56, 36)
    text(x + 72, y + 12, kicker, F("sans_b", 15), WHITE)
    hy = y + 52
    for ln in wrap_px(headline, F("sans_b", 23), w - 20):
        text(x + 10, hy, ln, F("sans_b", 23), INK)
        hy += 26
    dy = hy + 2
    last_top = dy
    for ln in wrap_px(detail, F("sans", 16), w - 20):
        text(x + 10, dy, ln, F("sans", 16), (55, 55, 55))
        last_top = dy
        dy += 19
    if last_top + 17 > y + h - 2:
        print("CARD OVERFLOW:", headline, last_top + 17 - y, ">", h)


def draw_grid():
    text(MX, 478, "AROUND THE WORLD", F("sans_b", 20), INK)
    rx = MX + int(tw("AROUND THE WORLD", F("sans_b", 20))) + 18
    hline(rx, 488, MX + CW - rx, INK, width=2)
    cw3 = (CW - 24) // 3
    row1 = [
        (icon_bridge, (70, 96, 128), "UKRAINE WAR",
         "CRIMEA BRIDGE HIT AGAIN",
         "Ukraine's third strike on the bridge in a week hits the "
         "railway; traffic is suspended."),
        (icon_gulf, (140, 44, 40), "MIDDLE EAST",
         "IRAN HITS GULF STATES",
         "Tehran answers the US strike on Qeshm. IEA: Hormuz is "
         "energy's biggest-ever threat."),
        (icon_vice, (150, 44, 110), "CULTURE · GAMING",
         "GTA VI IS HERE AT LAST",
         "After 13 years, Vice City returns: a 99 Metacritic score "
         "and $1.65bn in pre-orders."),
    ]
    for i, (fn, band, kick, hd, sm) in enumerate(row1):
        draw_card(MX + i * (cw3 + 12), 496, cw3, 172, fn, band, kick, hd, sm)
    row2 = [
        (icon_court, (52, 66, 96), "JUSTICE · THE HAGUE",
         "WORLD COURT RULES ON MYANMAR",
         "ICJ genocide judgment: the court finds some 10,000 Rohingya "
         "were killed in the 2017 crackdown."),
        (icon_cyclone, (36, 92, 140), "INDIA · DISASTER",
         "CYCLONE AKVAN: 100,000 FLEE",
         "Over 100,000 evacuated in Odisha as the storm nears landfall "
         "at Gopalpur. Red alert in Andhra."),
        (icon_climate, (46, 110, 64), "CLIMATE · TÜRKIYE",
         "COP31 DEADLOCK IN ANTALYA",
         "Ministers meet to unblock the climate talks, but a final "
         "deal stays elusive."),
    ]
    for i, (fn, band, kick, hd, sm) in enumerate(row2):
        draw_card(MX + i * (cw3 + 12), 680, cw3, 172, fn, band, kick, hd, sm)


def draw_also_today():
    y0 = 864
    text(MX, y0, "ALSO TODAY", F("sans_b", 19), RED)
    rx = MX + int(tw("ALSO TODAY", F("sans_b", 19))) + 12
    hline(rx, y0 + 10, MX + CW - rx, INK, width=2)
    left = [
        "ANTHROPIC'S $81.3BN IPO IS BIGGEST EVER",
        "BANGLADESH: YUNUS HOME TORCHED IN UNREST",
        "VAN GOGH SELLS FOR A RECORD $190.4M",
    ]
    right = [
        "EU PROPOSES €45BN LOAN FOR UKRAINE",
        "IAEA: N. KOREA EXPANDS URANIUM PLANT",
        "UK SENDS UKRAINE 1,000 STRIKE DRONES",
    ]
    col_w = (CW - 12) // 2
    for col, items in enumerate((left, right)):
        ix = MX + col * (col_w + 12)
        iy = y0 + 25
        for it in items:
            text(ix, iy, "· " + it, F("sans_b", 16), INK)
            iy += 23


def draw_footer():
    double_rule(MX, 962, CW)
    text(W // 2, 974,
         "SOURCES: REUTERS · AP · BBC · NYT · THE HINDU · LE MONDE · IEA · ICJ",
         F("sans", 14), GREY, align="center")
    text(W // 2, 994, "DRAWN ENTIRELY IN CODE — NO PHOTOGRAPHS, NO AI IMAGES",
         F("sans", 13), (110, 110, 110), align="center")


def main():
    rect(0, 0, W, H, PAPER)
    rect_outline(10, 10, W - 20, H - 20, (120, 110, 90))
    rect_outline(15, 15, W - 30, H - 30, (120, 110, 90))
    draw_masthead()
    draw_lead()
    draw_grid()
    draw_also_today()
    draw_footer()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
