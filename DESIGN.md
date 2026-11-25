# Design notes - The World Today, 24 November 2026

The page is a broadsheet front page compressed into a square:
a navy masthead, a centred date line, three feature columns, a
four-story world grid, a numbers strip and a one-line source
footer. It is drawn, not assembled from screenshots, so every
element's position is a number in `render.py` and the output is
byte-identical between runs.

## Geometry

- Canvas 1024x1024, side margin 28 px.
- Masthead band 0-108 in navy, with a gold rule at 108-112. The
  kicker sits at y=13 in letterspaced capitals; the title is set in
  DejaVu Serif Bold at 52 pt, centred, at y=34.
- The edition date line is set big and bold (Serif Bold, 37 pt),
  centred, directly under the masthead at y=124, with a navy rule
  at y=176. It is the largest text on the page after the title
  itself, by design: a reader should know which day they are
  looking at before they read a single headline.
- Features start at y=192. Each column is 310 px wide with 19 px
  gutters; thumbnails are 196 px tall and headlines begin at
  y=400, fitted between 29 and 22 pt with at most five lines.
  A light rule at y=578 closes the section. The renderer checks
  every fitted headline against that rule before drawing.
- "Around the World" opens at y=592 with its rule at 620. The grid
  is two columns of two: 168x112 thumbnails with the headline
  beside them, fitted between 22 and 17 pt, at most four lines.
  Rows start at 634 and 764.
- The numbers strip is a navy band at 890-970. Unlike a flowing
  layout, its three stats sit in fixed columns at x=168, 448 and
  728, values in Serif Bold 30 pt and labels in Sans 11 pt wrapped
  to 248 px and capped at two lines, so no label can crowd the
  strip's bottom edge.
- The footer rule sits at y=982 and the centred source line at
  y=990, in grey Sans 12 pt.

## Type and colour

- Serif Bold for the title, the date line, headlines and stat
  values; Sans for kickers, section titles, labels and the footer.
- Navy (15, 35, 71) for the masthead and the numbers strip, gold
  (198, 164, 92) for rules and accents, paper (250, 247, 240) for
  the page, ink (18, 22, 30) for headlines.
- There is no article body text anywhere on the page. The format
  is thumbnails and headlines: the reader gets the shape of the
  day in one look, and follows the URLs in `sources.json` for the
  full stories.

## Failure behaviour

- A story whose thumbnail file is missing is drawn as a navy panel
  with a gold globe glyph and a label (this edition has one panel
  label defined, for the Libya story, though its photo was usable
  in the end). A thumbnail that exists but does not decode, or is
  smaller than 300x150, fails the build.
- The layout audit runs before any drawing: a headline that would
  cross its section boundary stops the build and names the story.
- After saving, the renderer probes the masthead, the gold rule,
  the numbers strip and both paper edges, and verifies the stats
  against the edition record, so a truncated or misdrawn page
  cannot be shipped by accident.

## Why fixed strip columns

An early sketch let the numbers strip flow its columns by content
width; long labels then wrapped unevenly and one edition's label
nearly touched the strip's bottom edge. Fixed columns trade a
little flexibility for a guarantee: with the label width and the
two-line cap fixed, the strip's contents provably fit, and the
audit can check that proof mechanically on every build.

## Thumbnail treatment

Photographs are centre-cropped to their boxes with the `cover`
rule: scale by the larger axis ratio, crop the overflow
symmetrically. Nothing is letterboxed and nothing is stretched, so
every thumbnail fills its rectangle exactly and the grid's edges
stay straight. Feature thumbnails are 310x196 (roughly 8:5) and
grid thumbnails 168x112 (3:2); wire photography survives both
crops because its subjects sit near the centre of the frame.

A thumbnail must decode and measure at least 300x150 before the
build will use it. Below that, upscaling would smear the photo
across a 310 px column; the story then falls back to its panel.

## Determinism

The renderer reads only `sources.json` and the files in `thumbs/`,
both committed. It consults no clock, no random source and no
network. Pillow's PNG encoder is run with fixed settings, so two
runs on the same inputs produce the same bytes, a property the
independent checker (`check.py`) proves on every run by rendering
in a temporary copy and comparing hashes. Determinism is what
makes the committed `entry.png` reviewable: the file in the repo
is the file the renderer makes, not a relative of it.

## Legibility rules

- Headlines never go below 22 pt in the features or 17 pt in the
  grid; if a headline cannot fit at those floors, the build fails
  and the headline is shortened editorially, never shrunk.
- The date line is set at 37 pt because an edition misread as
  another day's is worse than a headline set a point smaller.
- Contrast is structural: ink on paper, white on navy, gold only
  for rules and the strip's label. No text sits on a photograph.

## The vertical budget, section by section

The page's 1024 px divide as follows, and the audit's job is to
keep every section inside its allotment:

- 0-108 masthead: kicker at 13, title at 34, nothing else may
  enter the band.
- 108-112 the gold rule, the page's only full-width ornament.
- 112-176 the date block: date line at 124, its baseline clear of
  the navy rule at 176.
- 176-192 breathing room between the rule and the first
  thumbnails; the features begin at 192 exactly.
- 192-388 feature thumbnails; 388-400 a gap; 400-578 feature
  headlines, the tallest of which (five lines at 29 pt) ends at
  573, five pixels above the rule.
- 578 the features rule; 592 the grid title; 620 its rule.
- 634-746 grid row one; 764-876 grid row two; the 18 px between
  rows is the grid's only internal gap.
- 876-890 breathing room; 890-970 the numbers strip.
- 970-982 breathing room; 982 the footer rule; 990-1002 the
  source line; the last 22 px are margin.

Every gap in that budget is deliberate. A page with no body text
has nothing to absorb a layout error, so the whitespace is part
of the specification, not what is left over.

## Colour, and why these three

The palette is three colours and a paper. Navy carries authority
without black's finality; it is the colour of the masthead and
the strip, the two bands that frame the news. Gold is used only
where a line must be seen but not read: the rule under the
masthead, the globe on a panel, the strip's small label. It never
sets a headline. Paper is a warm off-white rather than a screen
white, because the page quotes a printed object and because ink
on warm paper keeps its contrast at thumbnail size, where many
readers will actually meet this image. Ink is a near-black with
a blue bias, chosen to sit calmly next to the navy. No other
colours are admitted, including in the panels: a photograph
brings its own colours, and the drawn parts of the page refuse
to compete with them. The colour probes in the output check
sample exactly these decisions, masthead, rule, strip and paper,
so a palette drift fails the build like a geometry drift.

## What the audit cannot see

Fit is all the audit proves; quality is beyond it. Whether a
headline is fair, whether a crop halves a face, whether the day
was selected well: none of that is visible to a geometry check.
Those judgements are recorded where they belong (SOURCES.md for
fairness, EDITION.md for selection) and exercised in the build's
review step, where the layout report is read and the image is
opened by a person. The audit's trustworthiness comes from its
narrowness: it certifies that what was decided editorially is
what physically appears, inside the boundaries the design
promises. A bad edition can pass it. A broken page cannot.

## The page at other sizes

The page is one fixed 1024 px image, so its behaviour at other
sizes is a property of other people's software, and the design
anticipates three cases:

- **Feed thumbnails** (a few hundred pixels wide): the masthead
  and the feature headlines survive; the grid headlines and the
  strip labels do not. That ordering is deliberate: the edition's
  identity and its three decisions remain legible at the size
  most readers will actually meet it.
- **Full-screen reading** (the intended case): every element is
  at its designed size, and the vertical budget is the reading
  experience.
- **Print**: the navy masthead prints as a heavy dark block on
  cheap printers; the page tolerates it because no text sits on
  the navy. The hairline rules print at the edge of visibility,
  which is acceptable: they organise the screen version, and the
  print version organises itself by whitespace.

A design that only worked at exactly 1024 px would be a poster,
not a newspaper page. This one degrades in the order the
editorial priorities dictate: identity first, features second,
grid third, apparatus last.



