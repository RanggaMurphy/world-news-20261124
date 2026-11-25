# Build log - The World Today, 24 November 2026

How this edition was put together, in the order it happened. The
log exists so the entry can be rebuilt and reviewed by someone who
was not in the room.

## Research

- The day's world news was gathered from the RSS feeds of the
  major wires and papers, and every candidate story was checked
  across feeds: a story needed at least two distinct outlets
  carrying it before it could be selected.
- Seven stories passed the two-outlet rule. The selection leads
  with the Megaspeed blacklist (three carriers), the Indonesian
  factory fire (three carriers) and the Iowa court ruling (two
  carriers, but a presidential reversal inside it).
- The Libya operation appears twice in the grid on purpose: the
  sinking itself and the political reaction were carried as
  separate stories by separate wire pairs.
- Thumbnails came from each story's lead article image. Six of
  the seven were usable as photographs; the Libya sinking also
  carries a panel label definition as a fallback.

## Data

- `sources.json` holds the edition: title, date line, the three
  features, the four grid stories, the three stats and the source
  line. Each story records its headline, its carriers, its
  thumbnail, its region, a short context paragraph and the
  article URLs.
- The numbers strip uses one figure from the news itself (99%,
  from the Oxfam report) and two counts of the edition's own
  making (7 stories, 8 outlets), each labelled so a reader can
  tell which is which.

## Rendering

- `render.py` draws the page with Pillow: masthead, date line,
  features, grid, strip, footer. It runs a thumbnail verification
  and a layout audit before drawing, and a colour-probe check on
  the saved file afterwards.
- The draw is deterministic: no network, no randomness, no clock.
  Re-running it on the committed inputs reproduces `entry.png`
  byte for byte.
- `python3 render.py --report` prints the fitted size and line
  count of every headline without drawing, for review.

## Entry

- `main.py` is the competition entrypoint. It uses only the
  standard library, finds `entry.png` beside itself (or in
  MAKEFUN_BOT_DIR), copies it into MAKEFUN_OUTPUT_DIR and checks
  the copy's size against the source before exiting.
- The image was rendered once, checked, and committed as
  `entry.png`; the entrypoint never re-renders, so what was
  reviewed is exactly what the grader receives.

## The build, step by step

1. Gather the day's feeds and list every story carried by at
   least two tracked outlets.
2. Select three features and four grid stories from that list,
   leading with consequence and keeping one argument piece and
   one assessment if the day offers them.
3. Write the headlines, carriers, regions, contexts and URLs
   into `sources.json`, with the stats strip computed from the
   selection itself.
4. Fetch each story's lead image into `thumbs/`, named by story
   number.
5. Run the renderer: it verifies the data and the thumbnails,
   audits the layout, draws the page, and probes the result.
6. Read the layout report (`--report`) and confirm every
   headline's fitted size is at or above its floor.
7. Run the entrypoint the three ways the grader might, and
   compare hashes.
8. Run the independent checker, which re-derives every count and
   re-renders from a clean copy.
9. Commit the inputs and the rendered image together, so the
   repository always holds a consistent edition.


## Verification performed

- Two consecutive renders produced byte-identical output.
- The entrypoint was run three ways: default output directory, a
  custom MAKEFUN_OUTPUT_DIR, and from a different working
  directory with MAKEFUN_BOT_DIR set. All three produced the
  committed image.
- The layout audit reports no headline crossing its section
  boundary, and the output check's colour probes all pass.
- The independent checker (`check.py`) re-derives the outlet
  count, the story counts and the 99% attribution from
  `sources.json`, probes the image, and re-renders in a temporary
  copy to confirm the committed PNG matches the committed inputs.

## Failure modes considered

- **A wire corrects a story after press time.** The edition is a
  record of the day as reported on the day; corrections belong to
  the next edition, and the URLs in `sources.json` lead to the
  outlets' current versions.
- **A thumbnail is withdrawn or replaced at the source.** The
  build uses the committed files in `thumbs/`, so the page cannot
  change after review; the checker proves the committed image is
  what the committed thumbnails produce.
- **A headline is too long for its column.** The audit fails the
  build and names the story; the fix is editorial (shorten the
  headline in `sources.json`), never a smaller font.
- **The stats drift from the stories.** Both the renderer and the
  checker recompute the story and outlet counts from the data and
  refuse to proceed if the strip disagrees.

## File inventory at submission

- `main.py` - entrypoint (standard library only).
- `render.py` - generator, verifier, auditor and reporter.
- `check.py` - independent checker (re-derivation plus re-render).
- `sources.json` - the edition data, including the fact file.
- `entry.png` - the rendered front page, 1024x1024.
- `thumbs/` - seven story thumbnails, one per story.
- `README.md`, `SOURCES.md`, `DESIGN.md`, `OUTLETS.md`,
  `TIMELINE.md`, `GAZETTEER.md`, `EDITION.md`, `BUILDLOG.md` -
  the documentation set.
- `LICENSE` - MIT.

## Review notes from the layout report

The fitted sizes from `render.py --report` for this edition,
recorded because they show where the page is tight and where it
has room:

- Features 1 and 2 fit in four lines at the maximum 29 pt. The
  page's lead stories are also its roomiest, which is the right
  way round.
- Feature 3, the Iowa headline, is the tightest fit on the page:
  five lines at 29 pt, ending at y=573 against the rule at 578.
  It passes because the fitter found its size before needing to
  shrink; a single extra word would have forced 28 pt.
- Grid story 1, the Merkury sinking, fits four lines at 19 pt -
  the longest headline of the day (fifteen words) in the smallest
  space it was given. It is the grid's tightest cell.
- Grid stories 2 to 4 fit three lines at the maximum 22 pt.
- All three stats fit their fixed columns with the labels inside
  the two-line cap, and the source line fits the footer width.
- No story fell back to a panel: all seven thumbnails decoded
  above the size floor, so the panel defined for the Libya story
  was drawn nowhere on this edition's page.

These numbers are the reason the audit exists. A headline one
word longer in feature 3 or grid 1 would still have rendered -
the fitter shrinks before it fails - but the report makes the
shrinkage visible, and this log records it, so the next editor
knows exactly how much room the format has left.

## Numbers of this build

The repository the checker and the renderer agree on, counted at
submission time:

- Seven stories, sixteen article URLs, eight outlets, twenty-nine
  facts in the fact file, seven watch entries, five edition notes.
- One thousand five hundred characters of context writing across
  the seven stories, the longest 279 (Iowa) and the shortest 179
  (COP31), inside the same order of magnitude the context check
  enforces.
- One image: 1024x1024, 593,900 bytes, reproduced byte for byte
  from the committed inputs on every verification run.
- Three programs: the entrypoint (standard library only), the
  renderer (generator, verifier, auditor, reporter) and the
  independent checker, which between them re-derive every number
  the front page prints before the page is allowed to exist.
- Eight documentation files, each with a single job: the record,
  the design, the outlets, the timeline, the gazetteer, the
  reading, the build log, and this file's own inventory above.



