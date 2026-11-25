# The edition - reading the 24 November 2026 front page

This note is the reader's companion to `entry.png`: what the page
shows, in the order a reader meets it, and what each element is
doing there. It is also the reviewer's checklist: if the image and
this note ever disagree, the image is wrong.

## Top to bottom

**The masthead** names the paper, not the day: "The World Today",
with the kicker "World News in One Image" above it. The promise of
the format is in the kicker: one image, the whole day.

**The date line** - "Tuesday, 24 November 2026" - is set almost as
large as the title and directly beneath it. An edition of this
paper is meaningless without its day, so the day gets title-level
prominence. A reader screenshotting the page in a week still knows
exactly which day they are holding.

**The features** are the day's three heaviest stories, given equal
columns because the day had no single dominant event:

1. The Megaspeed blacklist - trade, technology and scandal in one
   story, and the only feature with a named individual (Jensen
   Huang) inside it.
2. The Indonesian factory fire - the day's deadliest event, its
   toll still open.
3. The Iowa detonation ruling - a court decision that reversed a
   presidential pause within the same news cycle.

**Around the World** carries four stories at half weight. The
Libya operation appears twice, deliberately: once as a military
fact (a warship sunk, a cargo ship damaged) and once as politics
(praise from Kyiv, warning from Moscow). COP31's failure is the
day's argument piece. The Oxfam report closes the grid because it
carries the edition's hardest number.

**By the Numbers** mixes one figure from the news (99%) with two
counts of the paper's own process (7 stories, 8 outlets). The
labels say which is which: the process counts are labelled as
counts of stories and outlets, the news figure is attributed to
Oxfam in its label. A reader should never mistake the paper's
housekeeping for a fact about the world.

**The footer** is the source line: eight outlet names, in the
order they first appear across the page's stories. It is the
page's only small print, and it is a claim the rest of the
repository backs up: `SOURCES.md` shows the carrying, `OUTLETS.md`
shows the counting, and `sources.json` shows the URLs.

## What is not on the page

- No article body text. The format is thumbnails and headlines;
  the depth lives in the linked reporting, not in the image.
- No story carried by a single outlet. The two-outlet rule is the
  paper's whole defence against a wire error becoming a headline.
- No number without a source. The strip's figures trace to story
  7, and to the edition's own story and outlet counts.

## The day's character

Read as one page, 24 November 2026 was a day about control: who
may sell chips to whom, who may detonate what and where, whose
drones may reach which sea, who pays for the climate, and what a
blockade does to the land it surrounds. The page does not argue
that thesis; it simply happens to be what seven two-outlet stories
added up to. The thesis, such as it is, is recorded here rather
than printed on the page, because the page's job is the news and
this note's job is the reading of it.

## The features, one at a time

**Megaspeed.** The lead story earns its place on structure, not
sensation: a state decision (the export control list), a strategic
industry (AI chips), a destination that matters (China) and a
human scandal that made the file public. Any two of those would
make a grid story; all four make a lead. Its headline names the
consequence (blacklist) before the cause (scandal), which is the
order a reader needs.

**The factory fire.** The second feature is the page's conscience:
the only story where people died that day in the record. Its
headline carries two numbers, three killed and dozens missing,
and the gap between them is the story. It sits in the middle
column, between the two American stories, so the page's centre of
gravity is a disaster in Indonesia rather than a decision in
Washington.

**Iowa.** The third feature is a process story with a reversal in
it: a demolition halted by a president, then cleared by a court,
with a governor-elect's consent attached as a condition. It is
the edition's best example of why the two-outlet rule matters: a
sequence that strange needs two independent carriers before it
deserves a headline, and it had them (AP and the Guardian).

## The grid, one at a time

**The sinking** is the fact: a warship sunk, a cargo ship damaged,
a new sea reached. **The reaction** is the meaning: praise in
Kyiv, warning in Moscow, condemnation from Libya's government.
Printing both, adjacent, lets the reader see a wire story and its
diplomatic shadow side by side. **COP31** is the argument: three
named causes for one failure. **Oxfam** is the number: 99%, the
only figure on the page that comes from the world rather than
from the paper's own counting, and it is placed last so the page
ends on evidence rather than opinion.

## The page in other hands

Three readers are worth designing for explicitly, because the
format serves each of them differently:

- **The scanner** gives the page five seconds. For them the page
  is the masthead, the date and the three feature headlines, and
  the design rule that follows is the features' font floor: a
  scanner who cannot read the lead headlines at a glance has been
  failed by the page, whatever the grid contains.
- **The checker** arrives suspicious: a number, 99%, looks too
  round to be true. For them the page is the attribution in the
  label ("Oxfam says") and the footer line, and the repository
  behind the page (the record, the URLs, the fact file) is the
  answer to their suspicion. The image alone cannot satisfy a
  checker; it is designed to point at what can.
- **The archivist** arrives in a month. For them the date line's
  size is the feature: editions of this paper are filed by day,
  and a page whose day is unmissable files itself. The timeline
  and the press-time states exist for this reader.

## A glossary for this edition

Terms the page and its documents use in specific senses:

- **Carrier** - an outlet that published the story on the day.
  A story's carriers are listed in `sources.json` and counted by
  the checker; nothing is a carrier by reputation.
- **Feature** - one of the three lead stories, given a full
  column, a large thumbnail and up to five headline lines.
- **Grid story** - one of the four Around the World stories, at
  half weight: a small thumbnail and up to four headline lines.
- **Panel** - the drawn fallback for a story without a usable
  photograph: navy field, gold globe, white label. Defined for
  one story in this edition, drawn for none.
- **Press time** - the moment the edition's research closed.
  Facts are stated as they stood at press time, and TIMELINE.md
  records that state story by story.
- **The strip** - the By the Numbers band. Its figures are either
  from the news (attributed in the label) or counts of the
  edition itself (labelled as counts).
- **Two-outlet rule** - the selection rule: no story reaches the
  page on one outlet's reporting. It is the edition's only
  hard editorial law, and the checker enforces it mechanically.

## If you only read three headlines

For the reader with ten seconds, the page is designed so the
three features alone carry the day: a blacklist that redraws the
chip map, a fire whose toll is still open, and a court letting an
army blow up its own stockpile. Everything below the features
rule either deepens one of those themes (control, danger,
consequence) or closes the day with its hardest number. The
masthead, the date line and the three features are the minimum
viable edition; the grid and the strip are the argument that the
day was bigger than its three heaviest stories.

## A note on the two Libya stories

Editors merging the pair into one story would have gained a grid
slot and lost the edition's clearest piece of structure: fact on
the left of the grid's top row, reaction beside it. The sinking
is what happened; the reaction is what it means, and on a page
with no body text the only way to show both is to print both.
The duplication is the design, and `SOURCES.md` records the
reasoning so a future editor does not "fix" it by accident.

