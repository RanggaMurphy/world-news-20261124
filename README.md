# The World Today - 24 November 2026

A one-image summary of the world news of Tuesday, 24 November 2026,
built for the make.fun news-image-20261124 competition.

The front page leads with three feature stories, adds a four-story
"Around the World" grid, a "By the Numbers" strip and a source footer.
Every story was confirmed by at least two news outlets on the day;
the full source list is in `sources.json`.

## Files

- `main.py` - the entrypoint. Standard library only: it copies the
  pre-rendered `entry.png` into `MAKEFUN_OUTPUT_DIR`.
- `render.py` - the generator. Uses Pillow to draw `entry.png`
  (1024x1024) deterministically from `sources.json` and `thumbs/`.
- `sources.json` - the day's selected stories, stats and sources.
- `thumbs/` - the story thumbnails used by the generator.
- `entry.png` - the rendered front page.

## Rebuild the image

    python3 render.py
    python3 main.py

`main.py` honours `MAKEFUN_OUTPUT_DIR` and `MAKEFUN_BOT_DIR`.
