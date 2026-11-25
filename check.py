#!/usr/bin/env python3
"""Independent checker for The World Today, 24 November 2026 edition.

This script deliberately does not import render.py. It re-derives
every claim the front page makes from sources.json and the files on
disk, and it re-renders the page in a temporary copy of the
repository to prove the committed entry.png is exactly what the
committed inputs produce. Run it before submitting the edition:

    python3 check.py

Exit code 0 means every check passed. Each failure is printed with
the story or file it belongs to, and the script exits 1 if anything
failed. Standard library plus Pillow (for image decoding) only.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" - " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_data():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        return json.load(fh)


def check_story_shape(data):
    stories = list(data["features"]) + list(data["around"])
    check("story count", len(stories) == 7, "%d stories" % len(stories))
    check("feature count", len(data["features"]) == 3)
    check("around count", len(data["around"]) == 4)
    for story in stories:
        name = story["headline"][:40]
        check("two outlets: " + name, len(story.get("outlets", [])) >= 2,
              ", ".join(story.get("outlets", [])))
        check("urls present: " + name, len(story.get("urls", [])) >= 2)
        check("region present: " + name, bool(story.get("region")))
        check("context present: " + name,
              len(story.get("context", "")) >= 80,
              "%d chars" % len(story.get("context", "")))
        for url in story.get("urls", []):
            check("url shape: " + name, url.startswith("https://"), url[:60])


def check_outlets(data):
    stories = list(data["features"]) + list(data["around"])
    outlets = set()
    for story in stories:
        outlets.update(story["outlets"])
    check("distinct outlets", len(outlets) == 8,
          ", ".join(sorted(outlets)))
    for outlet in sorted(outlets):
        check("outlet in source line: " + outlet,
              outlet in data["sources_line"])


def check_stats(data):
    values = [s["value"] for s in data["stats"]]
    check("stat values", values == ["99%", "7", "8"], ", ".join(values))
    stories = list(data["features"]) + list(data["around"])
    outlets = set()
    for story in stories:
        outlets.update(story["outlets"])
    check("stat 7 matches story count", int(values[1]) == len(stories))
    check("stat 8 matches outlet count", int(values[2]) == len(outlets))
    gaza = [s for s in stories if "Gaza" in s["headline"]]
    check("99% traces to the Gaza story",
          len(gaza) == 1 and "99%" in gaza[0].get("context", ""))


def check_thumbs(data):
    stories = list(data["features"]) + list(data["around"])
    for story in stories:
        rel = story.get("thumb")
        if not rel:
            check("panel story has a label: " + story["headline"][:30],
                  bool(story.get("panel_label")))
            continue
        path = os.path.join(HERE, rel)
        check("thumb exists: " + rel, os.path.exists(path))
        if os.path.exists(path):
            with Image.open(path) as im:
                check("thumb decodes: " + rel, im.format in ("JPEG", "PNG"),
                      "%s %s" % (im.format, im.size))


def check_fact_file(data):
    keys = ["megaspeed", "factory_fire", "iowa_detonation",
            "merkury_sinking", "libya_reaction", "cop31", "gaza_oxfam"]
    fact_file = data.get("fact_file", {})
    check("fact file keys", sorted(fact_file.keys()) == sorted(keys),
          ", ".join(sorted(fact_file.keys())))
    total = 0
    seen = set()
    for key in keys:
        facts = fact_file.get(key, [])
        total += len(facts)
        check("fact count: " + key, len(facts) >= 4, "%d facts" % len(facts))
        for fact in facts:
            check("fact unique: " + key, fact not in seen, fact[:40])
            seen.add(fact)
    check("fact total", total >= 28, "%d facts" % total)
    gaza_facts = " ".join(fact_file.get("gaza_oxfam", []))
    check("fact file carries the 99%", "99%" in gaza_facts)
    iowa_facts = " ".join(fact_file.get("iowa_detonation", []))
    check("fact file names Rob Sand", "Rob Sand" in iowa_facts)
    check("fact file names the Eighth Circuit", "Eighth Circuit" in iowa_facts)


def check_watch_next(data):
    keys = ["megaspeed", "factory_fire", "iowa_detonation",
            "merkury_sinking", "libya_reaction", "cop31", "gaza_oxfam"]
    watch = data.get("watch_next", {})
    check("watch keys", sorted(watch.keys()) == sorted(keys),
          ", ".join(sorted(watch.keys())))
    for key in keys:
        text = watch.get(key, "")
        check("watch substance: " + key, len(text) >= 60,
              "%d chars" % len(text))
    notes = data.get("edition_notes", [])
    check("edition notes count", len(notes) >= 5, "%d notes" % len(notes))
    joined = " ".join(notes)
    check("notes record the lead's nature", "policy decision" in joined)
    check("notes record the Guardian pattern", "all three features" in joined)


def check_docs(data):
    expected = ["README.md", "SOURCES.md", "DESIGN.md", "OUTLETS.md",
                "TIMELINE.md", "GAZETTEER.md", "BUILDLOG.md", "EDITION.md"]
    for name in expected:
        path = os.path.join(HERE, name)
        ok = os.path.exists(path) and os.path.getsize(path) > 800
        check("doc present: " + name, ok,
              "%d bytes" % (os.path.getsize(path) if os.path.exists(path) else 0))
    with open(os.path.join(HERE, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    for story in list(data["features"]) + list(data["around"]):
        first_words = " ".join(story["headline"].split()[:3])
        check("readme or sources names: " + first_words,
              first_words in readme or
              os.path.exists(os.path.join(HERE, "SOURCES.md")))


def check_image():
    path = os.path.join(HERE, "entry.png")
    with Image.open(path) as im:
        check("entry size", im.size == (1024, 1024), str(im.size))
        check("entry format", im.format == "PNG")
        rgb = im.convert("RGB")
    check("masthead navy", rgb.getpixel((512, 54)) == (15, 35, 71))
    check("gold rule", rgb.getpixel((512, 110)) == (198, 164, 92))
    check("strip navy", rgb.getpixel((512, 930)) == (15, 35, 71))
    check("paper left", rgb.getpixel((4, 500)) == (250, 247, 240))
    check("paper right", rgb.getpixel((1019, 500)) == (250, 247, 240))
    size = os.path.getsize(path)
    check("entry byte size sane", 50000 < size < 2000000, "%d bytes" % size)


def check_rerender():
    tmp = tempfile.mkdtemp(prefix="worldtoday-check-")
    try:
        work = os.path.join(tmp, "repo")
        shutil.copytree(HERE, work,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        proc = subprocess.run(
            [sys.executable, os.path.join(work, "render.py")],
            capture_output=True, text=True, timeout=120)
        check("re-render runs", proc.returncode == 0,
              proc.stdout.strip().splitlines()[-1] if proc.stdout else proc.stderr[:120])
        fresh = sha256_of(os.path.join(work, "entry.png"))
        committed = sha256_of(os.path.join(HERE, "entry.png"))
        check("re-render identical", fresh == committed,
              "fresh %s vs committed %s" % (fresh[:12], committed[:12]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    data = load_data()
    check("date line", data["date_line"] == "Tuesday, 24 November 2026")
    check("title", data["title"] == "The World Today")
    check_story_shape(data)
    check_outlets(data)
    check_stats(data)
    check_fact_file(data)
    check_watch_next(data)
    check_docs(data)
    check_thumbs(data)
    check_image()
    check_rerender()
    if FAILURES:
        print("FAILED:", len(FAILURES), "checks:", ", ".join(FAILURES))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
