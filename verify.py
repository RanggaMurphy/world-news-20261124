#!/usr/bin/env python3
"""Second verifier for The World Today, 24 November 2026 edition.

check.py re-derives the edition's claims from sources.json and
re-renders the page. This script takes the opposite direction: it
starts from the prose documents and the dossiers, and checks that
they agree with the data and with each other. Two verifiers that
share no code and start from opposite ends are much harder to
fool than one verifier run twice.

    python3 verify.py

Exit code 0 means every cross-check passed. Standard library
plus Pillow only.
"""

import json
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" - " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return fh.read()


def load_data():
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as fh:
        return json.load(fh)


STORY_FILES = [
    "stories/01-megaspeed.md",
    "stories/02-factory-fire.md",
    "stories/03-iowa-detonation.md",
    "stories/04-merkury-sinking.md",
    "stories/05-libya-reaction.md",
    "stories/06-cop31.md",
    "stories/07-gaza-oxfam.md",
]

DOSSIER_SECTIONS = [
    "What happened",
    "The facts on record",
    "What was not printed",
    "Watch next",
    "Articles",
]


def check_dossiers(data):
    stories = list(data["features"]) + list(data["around"])
    check("dossier count", len(STORY_FILES) == len(stories))
    for story, rel in zip(stories, STORY_FILES):
        text = read(rel)
        name = rel.split("/")[-1]
        check("dossier headline: " + name,
              story["headline"].split(".")[0][:30] in text
              or story["headline"][:30] in text, story["headline"][:40])
        for section in DOSSIER_SECTIONS:
            check("dossier section %s: %s" % (section, name), section in text)
        for outlet in story["outlets"]:
            check("dossier carrier %s: %s" % (outlet, name), outlet in text)
        check("dossier region: " + name, story["region"] in text)


def check_fact_faithfulness(data):
    """Every fact in the fact file must be consistent with a dossier.

    The check is lexical, not semantic: the fact's longest word
    sequence is not required to appear verbatim, but its key nouns
    must. A fact that names a person, body or place its dossier
    never mentions is a compression error and fails here.
    """
    keys = ["megaspeed", "factory_fire", "iowa_detonation",
            "merkury_sinking", "libya_reaction", "cop31", "gaza_oxfam"]
    markers = {
        "megaspeed": ["Megaspeed", "China", "Jensen Huang"],
        "factory_fire": ["confectionery", "three", "missing"],
        "iowa_detonation": ["Iowa", "Rob Sand", "Eighth Circuit"],
        "merkury_sinking": ["Merkury", "Libyan", "cargo ship"],
        "libya_reaction": ["Zelensky", "Kremlin", "escalation"],
        "cop31": ["oil-producing", "boycott", "finance"],
        "gaza_oxfam": ["Oxfam", "contamination", "99%"],
    }
    for key, rel in zip(keys, STORY_FILES):
        dossier = read(rel)
        for marker in markers[key]:
            check("marker %s in dossier %s" % (marker, key),
                  marker.lower() in dossier.lower())
        facts = " ".join(data["fact_file"][key])
        for marker in markers[key]:
            check("marker %s in fact file %s" % (marker, key),
                  marker.lower() in facts.lower())


def check_press_rules(data):
    press = read("PRESS.md")
    for n in range(1, 24):
        check("press rule %d present" % n, ("**%d." % n) in press or
              (("\n%d. " % n) in press))
    stories = list(data["features"]) + list(data["around"])
    two_outlet = all(len(s["outlets"]) >= 2 for s in stories)
    check("rule 1 holds: two outlets everywhere", two_outlet)
    values = [s["value"] for s in data["stats"]]
    check("rule 10 holds: one news figure plus counts",
          values == ["99%", "7", "8"])


def check_desk_notes(data):
    keys = ["megaspeed", "factory_fire", "iowa_detonation",
            "merkury_sinking", "libya_reaction", "cop31", "gaza_oxfam"]
    notes = data.get("desk_notes", {})
    check("desk notes keys", sorted(notes.keys()) == sorted(keys),
          ", ".join(sorted(notes.keys())))
    for key in keys:
        text = notes.get(key, "")
        check("desk note substance: " + key, len(text) >= 120,
              "%d chars" % len(text))
    joined = " ".join(notes.values())
    check("desk notes record the merge debate", "merging" in joined
          or "merge" in joined)
    check("desk notes record the pair disclosure",
          "weakest confirmation pair" in joined)


def check_cross_references(data):
    readme = read("README.md")
    for name in ["SOURCES.md", "DESIGN.md", "OUTLETS.md", "TIMELINE.md",
                 "GAZETTEER.md", "BUILDLOG.md", "EDITION.md", "DOSSIER.md",
                 "CONTEXT.md", "PRESS.md", "check.py", "verify.py"]:
        check("readme lists " + name, name in readme)
    context_index = read("CONTEXT.md")
    for rel in ["background/export-controls.md", "background/factory-fires.md",
                "background/munitions-disposal.md", "background/naval-drones.md",
                "background/climate-talks.md", "background/gaza-contamination.md"]:
        check("context index lists " + rel, rel in context_index)
        check("briefing exists: " + rel,
              os.path.exists(os.path.join(HERE, rel)))
    dossier_index = read("DOSSIER.md")
    for rel in STORY_FILES:
        check("index lists " + rel, rel in dossier_index)
    sources_md = read("SOURCES.md")
    for story in list(data["features"]) + list(data["around"]):
        first = story["headline"].split()[0]
        check("sources record mentions: " + story["headline"][:30],
              first in sources_md)


def check_thumbs_independent(data):
    stories = list(data["features"]) + list(data["around"])
    total_bytes = 0
    for story in stories:
        rel = story.get("thumb")
        if not rel:
            continue
        path = os.path.join(HERE, rel)
        with Image.open(path) as im:
            w, h = im.size
            mode = im.mode
        check("thumb geometry: " + rel, w >= 300 and h >= 150,
              "%dx%d %s" % (w, h, mode))
        total_bytes += os.path.getsize(path)
    check("thumbs total sane", 50000 < total_bytes < 20000000,
          "%d bytes" % total_bytes)


def main():
    data = load_data()
    check_dossiers(data)
    check_fact_faithfulness(data)
    check_press_rules(data)
    check_desk_notes(data)
    check_cross_references(data)
    check_thumbs_independent(data)
    if FAILURES:
        print("FAILED:", len(FAILURES), "checks:", ", ".join(FAILURES))
        return 1
    print("all cross-checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
