# The Unofficial Guide

# Project 9 Extension

## Shape C
I will be updating this project with a new retrieval strategy for an extension in week 9.
This retrieval strategy will introduce a new chunking strategy that will change the way files are searched through. 
 What is out of scope for me is hardening against failure and deploying this project. 

It will be difficult to measure the difference between the chunker and the new chunking method because the sizes of text sample are too small to measure a change in retrieval quality. 


**Staff solution — `city_guides` corpus.**

<!-- ⚠️ THIS IS THE STAFF EXEMPLAR, not a student submission. It is what a
     strong submission looks like at the end of week 2: both weeks' sections
     present, week 1's text left exactly as it was written before any results
     existed, and every number in it produced by actually running the thing.

     Two things to point at when you show it to a room:

       1. Criterion 5 MISSED, and the miss is the most valuable part of the
          document. Do not "fix" this exemplar into a clean sweep.
       2. The improvement is a prompt change, not hybrid search. It is the
          boring option, and it is the one the diagnosis pointed at. That is
          the behaviour the week is trying to teach.

     See SOLUTION_NOTES.md for how to use this repo in class.

     Everything below this comment is written in the student's voice. -->

---

# Week 1

## What This Does

This answers questions about a fictional English region from fourteen travel
guides — nine towns, plus five guides that cut across all of them on eating,
walking, regional transport, seasons and accessibility. You ask it something a
visitor would actually ask — *"how often do the Marchwood trams run?"*, *"where
do I eat in Brightwater without paying riverside prices?"* — and it answers
from those documents and names the file it used. Questions the guides don't
cover get refused rather than guessed at. It is a command-line tool: `python
app.py ask "..."`.

## Chunking Strategy

**Chunk size:** 1200 (a ceiling, not a target — see below)
**Overlap:** 200

Every one of these fourteen documents is a markdown file split into labelled
`##` sections: *getting there*, *getting around*, *eat and drink*, *when to go*.
So I chunk on those headings — one section, one chunk — rather than on a
character count.

Two things I read in Milestone 1 pushed me here. The first is that the starter's
800-character window turned 14 documents into 51 chunks and its cuts had nothing
to do with the headings: chunks ended halfway through "Where to eat" and began
halfway through "What to see". The second is worse and took longer to notice.
These guides describe nine different towns in nearly identical vocabulary — they
all have a "where to eat", they all have a "getting there". A chunk that starts
mid-section carries no sign of *which town* it belongs to. "Four pubs, two cafés,
and a bakery that sells out by 11am" is a useless retrieval hit if you can't tell
it's Kestrelford.

So every chunk gets `<guide title> — <section heading>` prepended as its first
line. That single line is doing more work than the boundary change is.

1200 is a ceiling rather than a size. The longest section in the corpus is a
shade under 1100 characters, so at 1200 every section survives whole and the
packing path only fires on the handful that genuinely need it. I started at 800
out of habit, found it was splitting about a third of the sections for no reason
at all, and raised it until it stopped. 200 for the overlap because the overlap
here carries a whole trailing *paragraph* into the next piece rather than a fixed
number of characters, and 200 is roughly one paragraph in this corpus — longer
just duplicated text.

The numbers moved: 51 chunks averaging 650 characters (shortest 24, longest 800)
became **94 chunks averaging 318 characters (shortest 172, longest 758)**. More
chunks, all smaller, none of them a 24-character orphan.

## Sample Chunks

Printed with `python app.py chunks -n 5`.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
Corry Vale — Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
Givens Mill — Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
Pellew Sands — When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

Chunks 2 through 5 each read as one complete answer to one question and say
which town they are about. Chunk 1 is the intro paragraph that sits before the
first `##` heading, so it has the title but no section heading. I noticed that
here and did nothing about it, which turned out to matter in week 2 — see the
revision on criterion 4.

## Sample Answer

**Question:** What time do the pubs in Kestrelford stop serving food in the evening?

**Answer:**

```
Best distance 0.166 (cutoff 0.70)

The pubs in Kestrelford stop serving food in the evening at 8:30.

Source: guide_kestrelford.md and guide_eating.md

Sources retrieved: guide_eating.md, guide_givens_mill.md, guide_kestrelford.md
```

**My relevance cutoff:** 0.70

I ran the five questions my guides cover and the five in `OUT_OF_SCOPE` that
they clearly don't, and wrote down the best distance for each.

| Question | In corpus? | Best distance |
|---|---|---|
| What time do the pubs in Kestrelford stop serving food in the evening? | yes | 0.165 |
| Which year did the railway line north of Brightwater close? | yes | 0.243 |
| How often do the Marchwood trams run on weekdays? | yes | 0.257 |
| Where should I eat in Brightwater to avoid riverside prices? | yes | 0.266 |
| Which places in the region have no public transport at all? | yes | 0.591 |
| What is the capital of Mongolia? | no | 0.808 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.835 |
| How do I write a for loop in Rust? | no | 0.859 |
| How do I change the oil in a diesel engine? | no | 0.881 |
| Who won the 1994 World Cup? | no | 0.982 |

The two groups don't overlap and there is nothing at all between 0.591 and
0.808, so the cutoff goes in that gap: **0.70**.

The interesting number is 0.591. Four of my five questions land under 0.27; the
fifth is more than twice as far out, and it's the one whose answer isn't in any
single section — it has to be assembled from two. The starter's default of 0.6
would have refused it by a margin of nine thousandths, which is close enough
that I'd have blamed the gate for a chunking problem. Measuring the two groups
rather than keeping the shipped number is what made that visible.

## How I Used AI

**1.** I asked Claude to write the section-aware chunker from a description —
*"split markdown on `##` headings, one chunk per section, prepend the document
title and heading."* What came back split on the headings correctly but dropped
the intro text above the first `##` entirely, so the opening paragraph of every
guide vanished from the index. I only caught it because the chunk count came out
lower than the number of sections I had counted by hand in three files. I added
the leading section back myself — it's the `sections.append((heading, ...))`
before the loop in `_split_into_sections`.

**2.** I pasted my five draft criteria in and asked *"for each of these, tell me
exactly how you would test it using only what the sentence says — don't suggest
improvements."* It could describe a test for four of them. For my chunk
criterion it asked what "reads as a complete thought" meant, which was fair, and
I rewrote that one as a check on `##` section boundaries instead. It still
wasn't quite measurable and I didn't find that out until week 2 — see the
revision on criterion 4.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     None attempted.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

## Run Log — Before

Raw output: [`results/run_2026-08-24_1047_before.md`](results/run_2026-08-24_1047_before.md),
written by `run_eval.py::main`. Three runs of all five questions with the
response cache off, plus one pass over the five out-of-scope questions through
`run_eval.py::check_out_of_scope`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks respect section boundaries | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answers don't say more than the documents do | 5 of 5 | 4/5 | 4/5 | 4/5 | MISSED |

**Criterion 1** — scored by `scorer.py::retrieval_hit`, which checks whether the
`expects` phrase appears in any retrieved chunk. From the before log:

```
| What time do the pubs in Kestrelford stop serving food in the evening? | pass | pass | pass |
| Which year did the railway line north of Brightwater close? | pass | pass | pass |
| Where should I eat in Brightwater to avoid riverside prices? | pass | pass | pass |
| How often do the Marchwood trams run on weekdays? | pass | pass | pass |
| Which places in the region have no public transport at all? | pass | pass | pass |
```

**Criterion 2** — read off the answers in the before log, produced by
`generate.py::answer_from_chunks`. Every one of the fifteen names a file:

```
The railway line north of Brightwater closed in 1963.

Sources: `guide_regional_transport.md` and `guide_walking.md`.
```

**Criterion 3** — `run_eval.py::check_out_of_scope`, straight from the before log:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.808 | refused |
| How do I change the oil in a diesel engine? | 0.881 | refused |
| Who won the 1994 World Cup? | 0.982 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.859 | refused |

**Criterion 4** — the five chunks in the Sample Chunks section above, from
`chunker.py::split_documents`. Four of the five open with
`<guide title> — <section heading>` and none contains text from two sections.
The fifth is `guide_accessibility.md#0`:

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Criterion 5** — read by hand against the sources the log says were retrieved.
Four of five answers stay inside their documents. The fifth, all three runs:

```
Based on the provided documents, **Kestrelford** and **Corry Vale** have no public transport.

Source: `guide_accessibility.md`
```

`guide_accessibility.md` says *"**Corry Vale** has no public transport"* and,
separately, *"**Kestrelford** is built on a slope … There is no transport
**within the town**."* The answer is wrong about Kestrelford, which has an
hourly bus from Brightwater on weekdays.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | 5/5 on all three runs, and retrieval is deterministic so the three runs were always going to agree. Target was 4 of 5. |
| 2 | Every answer names a source | MET | All fifteen answers name at least one file. Not close. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused, worst distance 0.808 against a 0.70 cutoff. Target was 4 of 5. |
| 4 | Chunks respect section boundaries | MET | 4 of 5, which hits the target exactly — but only after I pinned down what the criterion meant. See the revision. |
| 5 | Answers don't say more than the documents do | MISSED | 4 of 5 against a target of 5 of 5. The same question failed the same way in all three runs, so this is the system's behaviour, not a bad run. |

**On the revision to criterion 4.** I wrote *"every chunk opens with the guide
title and that section's heading"* and then scored it two different ways on two
different days. The intro chunk of each guide — the text above the first `##` —
has a title and no heading. Monday I read that as passing, because there is no
section for it to be wrong about; Wednesday I read it as failing, because the
criterion says heading. Both readings are defensible and that's the problem: a
criterion I score by mood isn't a criterion. The revision names the exact first
line a chunk has to have. **The 4-of-5 target has not moved** — I hit it either
way, and lowering a number I met would be pointless as well as against the rules.

**On criterion 5 and the scorer.** Worth saying plainly, because it nearly fooled
me: `scorer.py::judge` marked question 5 **pass** on all three runs. The `expects`
phrase is "Corry Vale" and the answer contains "Corry Vale" — while also
containing a claim about Kestrelford that isn't true. My scorer is a substring
test and a substring test cannot see a sentence that was added. The only reason
I caught it is that criterion 5 is one I check by reading rather than by
scoring. That's an argument for keeping some criteria manual, not for a better
scorer.

## Diagnoses

**Criterion 5 — generation.**

Not retrieval. The chunks that came back are right: `guide_accessibility.md`
and `guide_corry_vale.md`, best distance 0.591, and the correct answer is in
them. The retrieved text distinguishes two different claims — Corry Vale has no
public transport, Kestrelford has no transport *within the town* — and the model
merged them into one by dropping the qualifier. That is the print-the-chunks
check from the brief coming out on the generation side: the answer was sitting
right there in a chunk and the answer still came out wrong.

The mechanism is specific to what this corpus looks like. Nine towns described
in near-identical language means retrieval routinely hands the model three
towns' worth of chunks for one question, and a question phrased as *"which
places…"* invites exactly the summarising move that loses qualifiers. The
starter's `GROUNDING_INSTRUCTION` says *"use only the information in the
documents"*, and the model did — it used it and then generalised it. "Only this
information" and "only these claims" are not the same instruction, and the
prompt only asked for the first.

**No pattern across misses,** because there is only one. What I'd flag instead is
a pattern across *passes*: the four questions that behaved are all questions with
a single number or name as the answer, sitting in one section of one guide.
Every question in my set that needs two documents is the one that failed. If I
had written a second question of that shape I'd probably have two misses and a
real pattern, and that is a fault in my question set rather than in my system.

## The Improvement

**What I changed:** Two rules added to `GROUNDING_INSTRUCTION` in `generate.py`
— one requiring qualifiers to be carried through, one forbidding claims that
merge two documents unless both say the same thing. Nothing else changed:
same chunker, same 94 chunks, same cutoff, same top-k.

```
- Keep every qualifier the documents use. If a document says something is true
  "within the town", or "in summer", or "on weekdays", your answer says so too.
  Dropping the qualifier makes the answer wrong.
- Do not combine two documents into a single claim unless both say the same
  thing. If they differ, say what each one says and name both.
```

**Why I picked it:** The diagnosis put the failure at generation — the right
chunks came back and the model widened what they said — so the fix goes in the
prompt, which is the only thing between the right chunks and the wrong sentence.

I want to be honest that this was not my first instinct. Hybrid search is on the
menu, it sounds like more of an engineering answer, and I had already opened
`store.py` to start on it before I re-read my own diagnosis. BM25 would have
changed which chunks came back for a question whose chunks were already correct.
It would have taken an afternoon and moved nothing.

### Run Log — After

Raw output: [`results/run_2026-08-24_1050_after.md`](results/run_2026-08-24_1050_after.md).
Same five criteria, three runs each, same corpus and index.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks respect section boundaries | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answers don't say more than the documents do | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

The question that failed, after:

```
Based on `guide_accessibility.md`, Corry Vale has no public transport.
```

```
According to `guide_accessibility.md`, Corry Vale has no public transport.
```

**Did it help?**

Yes, and I can say how I know: criterion 5 went 4/5 → 5/5 and the specific wrong
sentence is gone from all three runs. The Kestrelford claim doesn't appear
anywhere in the after log.

Two things stop me claiming more than that. **One question is not a
measurement.** I changed a prompt and watched one answer improve — I have not
shown that the rule generalises, only that it fixed the case that motivated it,
which is exactly the shape of result that looks convincing and isn't. **And
prompt changes have costs I didn't measure.** The after answers are noticeably
more clipped, and an instruction that hard against generalising is an
instruction to answer narrowly. On a question where the right answer genuinely
does span two documents, this version may now refuse to give it. Nothing in my
five criteria would catch that, which is a gap in my criteria and not a gap in
the change.

## What's Still Broken

Nothing is missed after the fix, so this is about what my test doesn't reach.

**My question set is too easy, and I can name the number.** Four of five
questions are single-fact lookups where the answer sits in one section. Those
four have never failed anything, in either run log. My whole test rests on one
question, and one question that fails is one coin flip away from a submission
where everything passed and I had nothing to diagnose.

**The scorer can't see an added sentence.** `scorer.py::judge` passed the wrong
answer three times. Substring matching can catch a missing fact and cannot catch
an extra one. The fix I'd want is a second scorer that checks the answer's claims
against the retrieved chunks — which means an LLM judging the output, which
means a scorer that doesn't return the same verdict twice, which is its own
problem. I stopped because building it properly is bigger than this week and
building it badly would have given me a number I trusted less than my own
reading.

**I never tested the narrowing.** Written above under *Did it help?* — I have a
concrete suspicion that the new rules make the system worse at genuinely
cross-document questions, and no question in my set that would show it.

## What I'd Do Differently

**Criterion 1, first.** "Retrieved chunks contain the answer" passed 5/5 before I
made any change and 5/5 after, on every run. A criterion that cannot move is not
measuring my system, it's measuring whether Chroma works. What I actually cared
about was whether retrieval put the right chunk *near the top* — I'd write it as
the answer appearing in the top **two** results, which my question 5 would have
failed at 0.591.

**And I'd write two hard questions instead of one.** The rule I'd give myself is
the one from the brief that I read and didn't act on: write the question you're
afraid of. I wrote one and it's the only question that taught me anything. My
four safe ones cost me three of five criteria that were never going to fail.

The thing I'd keep unchanged is criterion 5. It's the only one I check by
reading rather than scoring, it's the one that found the real bug, and my
automated scorer marked that same bug as a pass.
