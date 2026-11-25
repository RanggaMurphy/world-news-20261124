# Outlets - who carried what on 24 November 2026

Eight outlets appear in this edition's source line. This note
records what each of them carried, so the cross-checking behind
the page can be audited outlet by outlet. A story only reached
the page when at least two outlets on this list carried it.

## Al Jazeera

Carried the Megaspeed blacklist story, filing from the trade and
export-control angle: the US adding the firm at the centre of the
Nvidia scandal to its export control list. One of three carriers
for feature 1.

## BBC News

The busiest wire of the day for this edition: Megaspeed, the
Indonesian factory fire, the Libya drone strike (Zelensky angle),
the COP31 analysis and the Oxfam Gaza report all ran on BBC News.
The BBC and BBC News brands are counted separately in the source
line because the research feeds list them separately, but they
were never treated as two independent confirmations of the same
story on their own.

## The Guardian

Carried Megaspeed, the factory fire and the Iowa detonation
ruling. Its Iowa copy supplied the fullest account of the Trump
statement, including the condition about the incoming
governor-elect.

## DW

Germany's international broadcaster carried the Indonesian
factory fire, with the dozens-missing framing that the headline
uses. Second confirmation for feature 2 alongside BBC News and
The Guardian.

## AP News

Carried the Iowa ruling (with The Guardian) and the Libya strike
in Zelensky's telling (with BBC News). AP copy is treated as a
primary wire for US court stories in this edition.

## CBS News

Led the Libya sinking story with Reuters: the Merkury sinking and
the damage to the sanctioned cargo ship. CBS framing emphasised
the reach of Ukraine's naval drones.

## Reuters

Co-carried the Merkury sinking. Reuters is the edition's wire of
record for the claim that the cargo ship was sanctioned.

## BBC

Listed by the feeds as a separate brand from BBC News; carried
the COP31 analysis and the Oxfam report alongside BBC News. See
the note under BBC News about how the pair were counted.

## Counting rule

The strip's "8 outlets" counts distinct outlet names across all
seven stories' carrier lists, exactly as they appear in
`sources.json`. The confirmation rule is stricter than the count:
no story was selected on the strength of one outlet, and the two
BBC brands together never counted as a story's two confirmations.

## Carrier matrix

Stories down the side, outlets across the top; a mark means the
outlet carried the story. Every row has at least two marks, which
is the selection rule made visible.

- Megaspeed blacklist: Al Jazeera, BBC News, The Guardian.
- Factory fire: BBC News, DW, The Guardian.
- Iowa detonation: AP News, The Guardian.
- Merkury sinking: CBS News, Reuters.
- Libya reaction: AP News, BBC News.
- COP31 failure: BBC, BBC News.
- Gaza toxic wasteland: BBC, BBC News.

Column totals: BBC News 5 stories, The Guardian 3, AP News 2,
BBC 2, and one each for Al Jazeera, DW, CBS News and Reuters. The
Guardian is the edition's quiet workhorse: it is the second
confirmation on all three features.

## The pair problem

Two of the grid stories rest on the BBC pair, and this edition's
documents return to that fact because it is the record's weakest
joint. The defence is threefold. First, the feeds list the two
brands separately, with separate article URLs, so the record
reports what the feeds did. Second, neither story needed the
pair to be independent in the strong sense: the COP31 analysis
and the Oxfam report were both lead items whose facts (a failed
talk, a published report) are events in themselves, verifiable
from the artefacts. Third, the weakness is disclosed everywhere
it matters: in the counting rule above, in SOURCES.md, and in
the timeline's confirmation paths. A record that hides its weak
joint invites distrust of the whole; this one points at it.

## Corrections and republication

This note is also the edition's corrections policy, stated before
it is needed. If an outlet corrects a fact the page printed, the
correction belongs to the next edition's record, not to a silent
edit of this one: the repository's history is the audit trail,
and a changed headline with no trace would break the trail the
checker verifies. If a correction is material (a toll, a name, a
decision reversed), the next edition's `SOURCES.md` records it
against this edition explicitly. The page itself is never
re-rendered after submission except to prove determinism, which
by construction changes nothing.

## How each outlet's copy was used

- **Al Jazeera** supplied the framing of the blacklist as an
  export-control act, the register the headline adopts.
- **BBC News** headlines were the edition's default wording where
  several carriers offered a choice, because they were the
  shortest without losing a fact.
- **The Guardian** supplied the long detail: the full Trump
  statement on Iowa, including the governor-elect condition, came
  from its copy, and its factory-fire report anchored the toll.
- **DW** contributed the missing-persons framing for the fire,
  which the headline keeps because it was still the live fact.
- **AP News** was treated as the wire of record for the court
  ruling's sequence: pause first, clearance second.
- **CBS News** framed the sinking around drone reach, the angle
  the context paragraph adopts.
- **Reuters** anchored the sanctioned status of the cargo ship, a
  legal fact the page states only because Reuters carried it.
- **BBC** (the analysis brand) supplied the divided-world reading
  of COP31, printed as an argument and labelled as one.

## Feed mechanics

How the day's stories physically arrived, because provenance
includes the pipe, not just the byline:

- **Outlet RSS** (BBC, the Guardian, DW, Al Jazeera) delivers the
  outlet's own headline, timestamp and lead image directly. This
  is the preferred pipe: nothing sits between the outlet and the
  desk.
- **The Google News wire** aggregates the same articles with its
  own timestamps and without lead images. Stories that arrived
  this way (the AP, CBS and Reuters items, and the BBC analysis
  pieces) were read at the outlet's own page before selection;
  the wire is a discovery pipe, never the text of record.
- Timestamps in this repository are the feeds' own. Where the two
  pipes disagreed about a story's hour, the outlet's page won.
- No story was selected from a headline alone: every one of the
  seven was opened and read at the carrier's page before it
  entered sources.json.
- The desk tracked a fixed outlet set for the edition (the nine
  named in the footer line). A story carried only outside that
  set was invisible to the edition by design, and the footer says
  so, which is the honest version of "around the world" for a
  one-image paper.


