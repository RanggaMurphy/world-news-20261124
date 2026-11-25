# The World Today - 24 November 2026

A one-image summary of the world news of Tuesday, 24 November 2026,
built for the make.fun news-image-20261124 competition.

The front page leads with three feature stories, adds a four-story
"Around the World" grid, a "By the Numbers" strip and a source footer.
Every story was confirmed by at least two news outlets on the day.

The day in one look:

- **Features:** the US blacklisting Megaspeed after the Nvidia chip
  scandal, the Indonesian factory fire with dozens still missing,
  and the federal court clearing the Army to detonate bomb-making
  material in Iowa.
- **Around the World:** Ukraine's drone strike on Russian shipping
  off Libya (the sinking, and the reaction), what the failure of
  COP31 reveals about a divided world, and Oxfam's finding that
  Israeli attacks have turned Gaza into a toxic wasteland.
- **By the Numbers:** 99% (of Gaza showing signs of contamination),
  7 stories, 8 outlets cross-checked.

## Files

- `main.py` - the entrypoint. Standard library only: it copies the
  pre-rendered `entry.png` into `MAKEFUN_OUTPUT_DIR`.
- `render.py` - the generator. Uses Pillow to draw `entry.png`
  (1024x1024) deterministically from `sources.json` and `thumbs/`.
  It verifies the thumbnails and audits the layout before drawing,
  checks the saved file afterwards, and can print a layout report
  with `--report`.
- `sources.json` - the day's selected stories, stats and sources,
  with each story's carriers, region, context and article URLs.
- `SOURCES.md` - the editorial record: why each story was chosen
  and which outlets carried it.
- `DESIGN.md` - the page geometry, type and colour decisions.
- `OUTLETS.md` - outlet-by-outlet account of the cross-checking.
- `TIMELINE.md` - the stories in the order their events happened.
- `GAZETTEER.md` - notes on the places the headlines name.
- `BUILDLOG.md` - how the edition was researched, built and
  verified.
- `thumbs/` - the story thumbnails used by the generator.
- `entry.png` - the rendered front page.

## Rebuild the image

    python3 render.py
    python3 main.py

`main.py` honours `MAKEFUN_OUTPUT_DIR` and `MAKEFUN_BOT_DIR`.

## Verify the edition

    python3 render.py --report   # fitted sizes, audit, story record
    python3 check.py              # independent re-derivation + re-render

The renderer is deterministic: rebuilding from the committed
`sources.json` and `thumbs/` reproduces `entry.png` byte for byte
(sha256 `4321b5987c12fc444abfde800eaabe9f92377623c22b92b1310923aefbdce36e`).
`check.py` proves that from a clean copy, re-derives the story and
outlet counts behind the numbers strip, and checks the fact file
and the watch list against the story record.

## Reading order for reviewers

1. `EDITION.md` - what the page shows and why, top to bottom.
2. `SOURCES.md` - the editorial record behind each story.
3. `DESIGN.md` - geometry, type, colour and the vertical budget.
4. `OUTLETS.md`, `TIMELINE.md`, `GAZETTEER.md` - the supporting
   records: who carried what, when it happened, where it happened.
5. `BUILDLOG.md` - how the edition was built and verified.

