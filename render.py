#!/usr/bin/env python3
"""Render 'The World Today' front page for one day's world news.

Reads sources.json and the thumbnails in thumbs/ next to this file and
writes a deterministic 1024x1024 entry.png beside it. No network, no
randomness, no timestamps inside the image: two runs on the same inputs
produce byte-identical output.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024
MARGIN = 28

NAVY = (15, 35, 71)
NAVY_LIGHT = (27, 55, 102)
GOLD = (198, 164, 92)
CREAM = (247, 243, 234)
PAPER = (250, 247, 240)
INK = (18, 22, 30)
GREY = (105, 105, 100)
RULE = (196, 186, 166)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def spaced(text, gap=" "):
    return gap.join(list(text.replace(" ", ""))) if False else " ".join(text)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def centered(draw, y, text, fnt, fill):
    x = (W - text_w(draw, text, fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return x


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_w, max_lines, start_size, min_size, path=SERIF_BOLD):
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines, size
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w), min_size


def cover(img, box_w, box_h):
    """Resize and centre-crop img so it exactly covers box_w x box_h."""
    src_w, src_h = img.size
    scale = max(box_w / src_w, box_h / src_h)
    new_w = max(box_w, int(round(src_w * scale)))
    new_h = max(box_h, int(round(src_h * scale)))
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - box_w) // 2
    top = (new_h - box_h) // 2
    return img.crop((left, top, left + box_w, top + box_h))


def load_thumb(rel_path):
    path = os.path.join(HERE, rel_path)
    with Image.open(path) as im:
        return im.convert("RGB")


def draw_panel(draw, img, x, y, w, h, story):
    """Paste a thumbnail, or a navy label panel when no photo is usable."""
    thumb_rel = story.get("thumb")
    if thumb_rel and os.path.exists(os.path.join(HERE, thumb_rel)):
        photo = cover(load_thumb(thumb_rel), w, h)
        img.paste(photo, (x, y))
        return
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_LIGHT)
    cx, cy, r = x + w // 2, y + h // 2 - 12, min(w, h) // 5
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=GOLD, width=2)
    label = story.get("panel_label", "WORLD")
    fnt = font(SANS_BOLD, 20)
    lx = x + (w - text_w(draw, label, fnt)) / 2
    draw.text((lx, cy + r + 8), label, font=fnt, fill=(255, 255, 255))


def main():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, W, 108], fill=NAVY)
    kicker = "W O R L D   N E W S   I N   O N E   I M A G E"
    centered(draw, 13, kicker, font(SANS_BOLD, 14), GOLD)
    centered(draw, 34, data["title"], font(SERIF_BOLD, 52), (255, 252, 244))
    draw.rectangle([0, 108, W, 112], fill=GOLD)

    # --- Date line: big, centred, directly under the masthead -----------
    centered(draw, 124, data["date_line"], font(SERIF_BOLD, 37), NAVY)
    draw.line([MARGIN, 176, W - MARGIN, 176], fill=NAVY, width=2)

    # --- Three feature stories ------------------------------------------
    feat_y = 192
    thumb_h = 196
    col_w = 310
    col_xs = [MARGIN, MARGIN + col_w + 19, MARGIN + 2 * (col_w + 19)]
    for x, story in zip(col_xs, data["features"]):
        draw_panel(draw, img, x, feat_y, col_w, thumb_h, story)
        draw = ImageDraw.Draw(img)
        fnt, lines, size = fit_headline(draw, story["headline"], col_w, 5, 29, 22)
        ty = feat_y + thumb_h + 12
        for line in lines:
            draw.text((x, ty), line, font=fnt, fill=INK)
            ty += size + 7
    feat_rule_y = 578
    for x in col_xs:
        draw.line([x, feat_rule_y, x + col_w, feat_rule_y], fill=RULE, width=2)

    # --- Around the World grid -------------------------------------------
    grid_title_y = feat_rule_y + 14
    draw.text((MARGIN, grid_title_y), "A R O U N D   T H E   W O R L D",
              font=font(SANS_BOLD, 17), fill=NAVY)
    draw.line([MARGIN, grid_title_y + 28, W - MARGIN, grid_title_y + 28],
              fill=NAVY, width=2)

    cell_w = (W - 2 * MARGIN - 24) // 2
    cell_thumb_w = 168
    cell_thumb_h = 112
    rows_y = [grid_title_y + 42, grid_title_y + 42 + cell_thumb_h + 18]
    for idx, story in enumerate(data["around"]):
        cx = MARGIN + (idx % 2) * (cell_w + 24)
        cy = rows_y[idx // 2]
        draw_panel(draw, img, cx, cy, cell_thumb_w, cell_thumb_h, story)
        draw = ImageDraw.Draw(img)
        hx = cx + cell_thumb_w + 14
        hw = cell_w - cell_thumb_w - 14
        fnt, lines, size = fit_headline(draw, story["headline"], hw, 4, 22, 17)
        ty = cy + 2
        for line in lines:
            draw.text((hx, ty), line, font=fnt, fill=INK)
            ty += size + 5

    # --- By the Numbers strip ---------------------------------------------
    # Fixed columns: each stat gets the same width so the labels wrap
    # evenly and never crowd the strip's bottom edge.
    strip_y = 890
    draw.rectangle([0, strip_y, W, strip_y + 80], fill=NAVY)
    draw.text((MARGIN, strip_y + 16), "BY THE", font=font(SANS_BOLD, 15), fill=GOLD)
    draw.text((MARGIN, strip_y + 38), "NUMBERS", font=font(SANS_BOLD, 15), fill=GOLD)
    stat_xs = [168, 448, 728]
    for stat_x, stat in zip(stat_xs, data["stats"]):
        vf = font(SERIF_BOLD, 30)
        draw.text((stat_x, strip_y + 8), stat["value"], font=vf, fill=(255, 252, 244))
        lf = font(SANS, 11)
        label_lines = wrap(draw, stat["label"], lf, 248)
        ly = strip_y + 46
        for line in label_lines[:2]:
            draw.text((stat_x, ly), line, font=lf, fill=(214, 218, 228))
            ly += 14

    # --- Footer ------------------------------------------------------------
    draw.line([MARGIN, 982, W - MARGIN, 982], fill=RULE, width=1)
    centered(draw, 990, data["sources_line"], font(SANS, 12), GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=False)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
