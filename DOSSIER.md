# Dossier index - The World Today, 24 November 2026

One file per story lives in `stories/`. Each dossier holds the
same seven things: the headline as printed, the story's position
on the page, its carriers, what happened, the facts on record,
why the story was selected and how its headline was chosen, what
was deliberately not printed, what to watch next, and the
articles themselves.

| # | Story | Position | File |
|---|-------|----------|------|
| 1 | Megaspeed blacklist | Feature 1 | stories/01-megaspeed.md |
| 2 | Indonesian factory fire | Feature 2 | stories/02-factory-fire.md |
| 3 | Iowa detonation ruling | Feature 3 | stories/03-iowa-detonation.md |
| 4 | The Merkury sinking | Grid 1 | stories/04-merkury-sinking.md |
| 5 | The Libya reaction | Grid 2 | stories/05-libya-reaction.md |
| 6 | The failure of COP31 | Grid 3 | stories/06-cop31.md |
| 7 | Gaza, the Oxfam report | Grid 4 | stories/07-gaza-oxfam.md |

## How the dossiers relate to the other documents

- `SOURCES.md` is the edition-level record: selection, counting
  and method across all seven stories.
- The dossiers are the story-level record: everything about one
  story in one place.
- `sources.json` is the machine-readable record the renderer and
  the checkers consume; where a dossier and the JSON disagree,
  the JSON is what the page printed, and the dossier is wrong.
- The fact file inside `sources.json` is the compressed form of
  the dossiers' "facts on record" sections; `verify.py` checks
  that the compression is faithful.

## Reading order

For a reviewer with ten minutes: this index, then the dossier of
the story being questioned. For a reviewer with an hour: the
dossiers in page order, then SOURCES.md, then the checker
output. The dossiers assume the page; they do not repeat the
design documents.
