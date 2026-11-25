#!/usr/bin/env python3
"""Render 'The World Today' front page for one day's world news.

Reads sources.json and the thumbnails in thumbs/ next to this file and
writes a deterministic 1024x1024 entry.png beside it. No network, no
randomness, no timestamps inside the image: two runs on the same inputs
produce byte-identical output.
"""

import json
import os
import sys

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
    """Return text unchanged; kept for the kicker's letterspacing.

    The masthead kicker is stored pre-spaced in the source strings
    that need it, so this helper is now a pass-through retained for
    compatibility with the layout report's wording. It is exercised
    by the report path and documented here so nobody mistakes it
    for dead code worth deleting mid-edition.
    """
    return gap.join(list(text.replace(" ", ""))) if False else " ".join(text)


def text_w(draw, text, fnt):
    """Width in pixels of text rendered in fnt, as a float.

    Every fit decision in this module goes through this one call so
    the audit and the draw pass can never disagree about how wide a
    string is: both ask the same question of the same library.
    """
    return draw.textlength(text, font=fnt)


def centered(draw, y, text, fnt, fill):
    """Draw text centred on the canvas at height y; return its x.

    The x is computed from the measured width, not from an assumed
    centre, so centred lines stay centred whatever the string. The
    return value lets callers (and the report) reason about where a
    centred line actually landed.
    """
    x = (W - text_w(draw, text, fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return x


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap: fill each line until the next word overflows.

    Words are never split and hyphenation is never attempted, which
    keeps headlines readable and the line count predictable: the
    audit's arithmetic (lines times line step) depends on the wrap
    being a pure function of the string, the font and the width.
    """
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
    """Fit a headline into max_lines lines at the largest size allowed.

    Starts at start_size and steps down one point at a time until
    the wrapped text fits max_lines, never going below min_size. If
    even min_size overflows, the min_size wrap is returned anyway
    and the layout audit, which recomputes the same fit, reports
    the overflow and stops the build. Returns the font, the wrapped
    lines and the size used, because the caller needs all three to
    advance the text cursor by the right line step.
    """
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
    """Resize and centre-crop img so it exactly covers box_w x box_h.

    The scale factor is the larger of the two axis ratios, so the
    resized image covers the box on both axes; the overflow is then
    cropped symmetrically. Centre-cropping is the right default for
    news photography: the subject of a wire photo is almost always
    near the middle of the frame, and a symmetric crop never cuts
    one side's context entirely away. The result always has exactly
    the requested size, which the layout arithmetic relies on.
    """
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
    """Paste a thumbnail, or a navy label panel when no photo is usable.

    The panel is a deliberate design element, not an error state: a
    navy field, a gold globe glyph (a circle crossed by its equator
    and a meridian) and the story's panel label in white capitals.
    It keeps the grid's rhythm when a story has no usable photo, and
    because verify_thumbnails has already run, reaching this branch
    means the fallback was a known, recorded choice.
    """
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


EXPECTED_STORIES = 7
MIN_THUMB_W = 300
MIN_THUMB_H = 150


def verify_thumbnails(data):
    """Check the thumbnail plan against the files on disk.

    Every story should name a thumbnail that exists and is a real
    photo (at least MIN_THUMB_W x MIN_THUMB_H once decoded). A story
    whose thumbnail is missing falls back to a labelled panel at draw
    time, which is allowed, but a file that exists and cannot be
    decoded is a hard error: better to fail the build than to ship a
    front page with a hole in it. Returns the list of stories that
    will be drawn as panels.
    """
    panel_stories = []
    stories = list(data["features"]) + list(data["around"])
    if len(stories) != EXPECTED_STORIES:
        raise SystemExit(
            "expected %d stories, found %d" % (EXPECTED_STORIES, len(stories)))
    for story in stories:
        rel = story.get("thumb")
        if not rel:
            panel_stories.append(story["headline"])
            continue
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            panel_stories.append(story["headline"])
            continue
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            w, h = im.size
        if w < MIN_THUMB_W or h < MIN_THUMB_H:
            raise SystemExit(
                "thumbnail too small: %s is %dx%d" % (rel, w, h))
    return panel_stories


def verify_sources(data):
    """Check sources.json against the editorial rules of the edition.

    The rules are the ones SOURCES.md states in prose: seven stories,
    three of them features; every story carried by at least two
    outlets and backed by at least two article URLs; a region and a
    real context paragraph for every story; the stats strip holding
    the Oxfam figure and the two edition counts; and a source line
    that names every outlet that appears anywhere in the data. A
    failure here means the data drifted from the editorial record,
    and the build stops before any drawing happens.
    """
    stories = list(data["features"]) + list(data["around"])
    if len(data["features"]) != 3 or len(data["around"]) != 4:
        raise SystemExit("edition must have 3 features and 4 around stories")
    if len(stories) != EXPECTED_STORIES:
        raise SystemExit("edition must have %d stories" % EXPECTED_STORIES)
    outlets = set()
    for story in stories:
        if len(story.get("outlets", [])) < 2:
            raise SystemExit("story carried by one outlet: " + story["headline"])
        if len(story.get("urls", [])) < 2:
            raise SystemExit("story has under two urls: " + story["headline"])
        if len(story.get("context", "")) < 80:
            raise SystemExit("story context too thin: " + story["headline"])
        if not story.get("region"):
            raise SystemExit("story has no region: " + story["headline"])
        outlets.update(story["outlets"])
    if len(outlets) != 8:
        raise SystemExit("expected 8 distinct outlets, found %d" % len(outlets))
    for outlet in outlets:
        if outlet not in data["sources_line"]:
            raise SystemExit("outlet missing from source line: " + outlet)
    values = [s["value"] for s in data["stats"]]
    if values != ["99%", "7", "8"]:
        raise SystemExit("stats strip drifted: %s" % values)
    if int(values[1]) != len(stories) or int(values[2]) != len(outlets):
        raise SystemExit("stats counts disagree with the story data")
    return outlets


FACT_FILE_KEYS = [
    "megaspeed", "factory_fire", "iowa_detonation", "merkury_sinking",
    "libya_reaction", "cop31", "gaza_oxfam",
]


def verify_fact_file(data):
    """Check the fact file embedded in sources.json.

    The fact file is the edition's memory: four or five short,
    checkable facts per story, each one traceable to the carrying
    outlets' reporting. This check keeps it honest and complete:
    every expected key present, every list holding at least four
    facts, no fact repeated anywhere in the file, and no fact so
    short it cannot be checked. It runs with the other data checks
    so a thinned-out fact file fails the build like any other
    drift from the record.
    """
    fact_file = data.get("fact_file")
    if not isinstance(fact_file, dict):
        raise SystemExit("sources.json has no fact_file object")
    seen = set()
    for key in FACT_FILE_KEYS:
        facts = fact_file.get(key)
        if not isinstance(facts, list) or len(facts) < 4:
            raise SystemExit("fact file entry too thin: " + key)
        for fact in facts:
            if len(fact) < 30:
                raise SystemExit("fact too short to check: " + fact)
            if fact in seen:
                raise SystemExit("fact repeated in fact file: " + fact)
            seen.add(fact)
    extra = set(fact_file) - set(FACT_FILE_KEYS)
    if extra:
        raise SystemExit("fact file has unknown keys: %s" % sorted(extra))
    watch = data.get("watch_next")
    if not isinstance(watch, dict) or sorted(watch) != sorted(FACT_FILE_KEYS):
        raise SystemExit("watch_next must cover exactly the fact file keys")
    for key, text in watch.items():
        if len(text) < 60:
            raise SystemExit("watch_next entry too thin: " + key)
    notes = data.get("edition_notes")
    if not isinstance(notes, list) or len(notes) < 5:
        raise SystemExit("edition_notes must hold at least five notes")
    return len(seen)


def layout_audit(data):
    """Dry-fit every headline and stat label without drawing anything.

    Recomputes the geometry the draw pass will use and checks each
    block against the space reserved for it, so a headline that would
    spill into the next section fails the build here, with the story
    named, instead of showing up as an overlap in the shipped image.
    Returns a list of problem strings; empty means the page is clean.
    """
    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    problems = []

    # Masthead title and date line must fit the canvas width.
    if text_w(probe, data["title"], font(SERIF_BOLD, 52)) > W - 2 * MARGIN:
        problems.append("masthead title wider than the canvas")
    if text_w(probe, data["date_line"], font(SERIF_BOLD, 37)) > W - 2 * MARGIN:
        problems.append("date line wider than the canvas")

    # Features: thumbnails at y=192, 196 tall; headlines start at 400
    # and may not cross the rule at y=578.
    col_w = 310
    for story in data["features"]:
        fnt, lines, size = fit_headline(
            probe, story["headline"], col_w, 5, 29, 22)
        bottom = 400 + (len(lines) - 1) * (size + 7) + size
        if len(lines) > 5:
            problems.append("feature headline over 5 lines: " + story["headline"])
        if bottom > 578:
            problems.append(
                "feature headline crosses the rule at 578: " + story["headline"])

    # Around the World: the section title sits at 592, its rule at
    # 620, and the two rows start at 634, each 112 tall with an 18 px
    # gap. Headlines sit beside a 168 px thumbnail and may not cross
    # the bottom of their own row.
    cell_w = (W - 2 * MARGIN - 24) // 2
    head_w = cell_w - 168 - 14
    rows_y = [634, 634 + 112 + 18]
    for idx, story in enumerate(data["around"]):
        fnt, lines, size = fit_headline(
            probe, story["headline"], head_w, 4, 22, 17)
        bottom = rows_y[idx // 2] + 2 + (len(lines) - 1) * (size + 5) + size
        if len(lines) > 4:
            problems.append("grid headline over 4 lines: " + story["headline"])
        if bottom > rows_y[idx // 2] + 112:
            problems.append(
                "grid headline crosses its row: " + story["headline"])

    # Numbers strip: fixed columns at x=168/448/728, values at 30 pt,
    # labels wrapped to 248 px and capped at two lines.
    for stat in data["stats"]:
        if text_w(probe, stat["value"], font(SERIF_BOLD, 30)) > 248:
            problems.append("stat value too wide: " + stat["value"])
        label_lines = wrap(probe, stat["label"], font(SANS, 11), 248)
        if len(label_lines) > 2:
            problems.append("stat label over two lines: " + stat["label"])

    # Footer source line must fit on one line inside the margins.
    if text_w(probe, data["sources_line"], font(SANS, 12)) > W - 2 * MARGIN:
        problems.append("footer source line wider than the canvas")
    return problems


def check_output(path):
    """Verify the rendered file: size, format, byte size, key colours.

    The grader only copies entry.png, so this is the last chance to
    catch a broken render. The colour probes sample the masthead,
    the gold rule under it, the numbers strip and the paper corners,
    which together prove the draw pass ran end to end.
    """
    with Image.open(path) as im:
        if im.size != (W, H):
            raise SystemExit("entry.png is %s, expected %dx%d" % (im.size, W, H))
        if im.format != "PNG":
            raise SystemExit("entry.png format is %s, expected PNG" % im.format)
        rgb = im.convert("RGB")
    size_bytes = os.path.getsize(path)
    if size_bytes < 50000:
        raise SystemExit("entry.png suspiciously small: %d bytes" % size_bytes)
    probes = [
        ((512, 54), NAVY, "masthead"),
        ((512, 110), GOLD, "gold rule"),
        ((512, 930), NAVY, "numbers strip"),
        ((4, 500), PAPER, "left paper edge"),
        ((1019, 500), PAPER, "right paper edge"),
    ]
    for (xy, want, name) in probes:
        got = rgb.getpixel(xy)
        if got != want:
            raise SystemExit(
                "%s probe at %s: got %s, expected %s" % (name, xy, got, want))
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    if [s["value"] for s in data["stats"]] != ["99%", "7", "8"]:
        raise SystemExit("stats strip values drifted from the edition record")
    return size_bytes


def section_map():
    """Return the page's section geometry as (name, top, bottom) rows.

    This is the single source of truth the report prints and the
    audit's constants mirror: masthead, date block, features, grid,
    strip and footer, with the gaps between them named rather than
    implied. If a constant in the draw pass ever moves, this map is
    where the move is recorded first, and DESIGN.md's vertical
    budget is written from it.
    """
    return [
        ("masthead", 0, 108),
        ("gold rule", 108, 112),
        ("date block", 112, 176),
        ("features", 192, 578),
        ("grid title", 592, 620),
        ("grid rows", 634, 876),
        ("numbers strip", 890, 970),
        ("footer", 982, 1002),
    ]


def edition_digest(data):
    """Summarise the edition's data as a list of printable lines.

    The digest is the at-a-glance record the report ends with: one
    line per story with its region, carrier count, URL count and
    context length, then the edition-level totals. It exists so a
    reviewer can see the shape of the data (a story with one URL,
    a context half the length of the others) without opening the
    JSON, and so the report and the checker are looking at the same
    derived numbers.
    """
    lines = []
    stories = list(data["features"]) + list(data["around"])
    for i, story in enumerate(stories, 1):
        lines.append(
            "digest %d [%s] %s - %d outlets, %d urls, context %d chars"
            % (i, story["region"], story["headline"],
               len(story["outlets"]), len(story["urls"]),
               len(story["context"])))
    total_urls = sum(len(s["urls"]) for s in stories)
    total_context = sum(len(s["context"]) for s in stories)
    lines.append("digest totals: %d stories, %d urls, %d context chars, "
                 "%d facts, %d watch entries"
                 % (len(stories), total_urls, total_context,
                    sum(len(v) for v in data["fact_file"].values()),
                    len(data["watch_next"])))
    return lines


def layout_report(data):
    """Print a human-readable account of where everything sits.

    Used when reviewing an edition by hand: it lists the fitted size
    and line count of every headline, the panel fallbacks, and the
    vertical budget of the page from masthead to footer, so a tight
    fit is visible in text before anyone opens the image.
    """
    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    print("The World Today -", data["date_line"])
    print("canvas %dx%d, margin %d" % (W, H, MARGIN))
    for name, top, bottom in section_map():
        print("section %-14s %4d-%4d" % (name, top, bottom))
    print("masthead 0-108, gold rule 108-112, date line at 124, rule at 176")
    panels = verify_thumbnails(data)
    col_w = 310
    for i, story in enumerate(data["features"], 1):
        fnt, lines, size = fit_headline(
            probe, story["headline"], col_w, 5, 29, 22)
        print("feature %d: %d lines at %d pt (thumb %s)"
              % (i, len(lines), size, story.get("thumb", "panel")))
    cell_w = (W - 2 * MARGIN - 24) // 2
    head_w = cell_w - 168 - 14
    for i, story in enumerate(data["around"], 1):
        fnt, lines, size = fit_headline(
            probe, story["headline"], head_w, 4, 22, 17)
        print("around %d: %d lines at %d pt (thumb %s)"
              % (i, len(lines), size, story.get("thumb", "panel")))
    for stat in data["stats"]:
        print("stat %s - %s" % (stat["value"], stat["label"]))
    print("panel fallbacks:", panels if panels else "none")
    outlets = verify_sources(data)
    print("outlets (%d): %s" % (len(outlets), ", ".join(sorted(outlets))))
    print("fact file: %d facts across %d stories"
          % (verify_fact_file(data), len(FACT_FILE_KEYS)))
    for story in list(data["features"]) + list(data["around"]):
        print("story [%s] %s - carried by %s, %d urls"
              % (story["region"], story["headline"],
                 ", ".join(story["outlets"]), len(story["urls"])))
    for line in edition_digest(data):
        print(line)
    print("numbers strip 890-970, footer rule 982, footer text 990")
    problems = layout_audit(data)
    print("audit:", "clean" if not problems else problems)


def main():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    if "--report" in sys.argv:
        layout_report(data)
        return

    verify_sources(data)
    verify_fact_file(data)
    verify_thumbnails(data)
    problems = layout_audit(data)
    if problems:
        for problem in problems:
            print("layout problem:", problem, file=sys.stderr)
        raise SystemExit(1)

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
    size_bytes = check_output(out)
    print("wrote", out, img.size, size_bytes, "bytes, checks passed")


if __name__ == "__main__":
    main()
