# Acceptance criteria — The Unofficial Guide

<!-- ⚠️ STAFF SOLUTION. Five criteria against the `city_guides` corpus.

     The three provided ones are kept verbatim; 4 and 5 are written from what
     reading the corpus in Milestone 1 turned up. What makes them worth showing
     is the *reasons* — every one of them names something about these fourteen
     documents rather than something that could be said about any project.

     Criterion 4 also carries a week 2 revision, so the legitimate-revision
     pattern from instructor_2 segment 4 has a worked example in the repo. -->

Five criteria that say what "working" means for this system, written in week 1
**before** any results existed.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Four of my five questions have their answer sitting inside
a single labelled section of a single guide, so retrieval only has to find the
right section. The fifth — which places have no public transport — is answered
in two documents at once and in neither of them completely, so I expect that
one to be the miss. 5 of 5 would be claiming my chunker solved a problem I know
it doesn't solve.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** This one is enforced twice before the model gets a chance
to fail it — `generate.py::build_prompt` labels every excerpt with its filename
and `GROUNDING_INSTRUCTION` asks for the filename back. Anything less than 5 of
5 means one of those two layers isn't doing its job, which I'd want to know
about. A target of 4 of 5 here would be budgeting for a bug.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:** My three out-of-scope questions came back between 0.808 and
0.982 against a worst in-corpus distance of 0.591 (the table is in the README).
With a gap that wide and a cutoff at 0.70 the gate should be comfortable — but
retrieval is deterministic, so if it lets one through it lets it through every
time, and 4 of 5 leaves room for exactly one question sitting nearer the
boundary than I think it does.

---

## 4. Chunks respect section boundaries

At least 4 of 5 sampled chunks contain text from exactly one `##` section of
one guide, and every chunk opens with the guide title and that section's
heading.

**Why this target:** These fourteen documents describe nine towns using almost
identical vocabulary — every one of them has a "where to eat" and a "getting
there". A chunk that runs across two sections, or that starts mid-section with
no title on it, is a chunk that can't say which town it is about. That is the
specific failure the starter's 800-character window produces here, and it is
what my chunker exists to fix, so it is what I should be measuring.

> **Revised in week 2:** At least 4 of 5 sampled chunks contain text from
> exactly one `##` section of one guide, and every chunk's first line is
> `<guide title> — <section heading>`.
>
> **Why revised:** "opens with the guide title and that section's heading"
> turned out to be something I scored two different ways. On the intro chunk of
> each guide there is no section heading at all — the text before the first
> `##` — and I counted those as passing on Monday and failing on Wednesday.
> Naming the exact line the chunk has to start with makes it a check rather
> than a judgment. The 4-of-5 target has not moved.

---

## 5. Answers don't say more than the documents do

For 5 of 5 answered questions, every factual claim in the answer can be traced
to a sentence in one of the chunks that were retrieved for it — no widened,
merged or dropped qualifiers.

**Why this target:** These fourteen guides describe nine towns in almost
identical language, and retrieval routinely hands the model chunks from three
of them at once. The specific risk that creates is not invention, it is
*merging*: the accessibility guide says Corry Vale has no public transport and
that Kestrelford has no transport **within the town**, and those two sentences
are one careless summary away from becoming one wrong claim. Criterion 2 can't
catch that — an answer can name the right file and still misreport what's in
it. 5 of 5 rather than 4 of 5 because one confidently wrong sentence with a
correct-looking citation on it is worse than no answer at all, which is the
whole reason the gate exists.

<!-- How this gets checked, so a reader can do it without asking me: the run
     log records the sources retrieved for every question. Open those files,
     read the answer sentence by sentence, and mark the question failed if any
     sentence says something none of those files say. -->

---

<!-- ─────────────────────────────────────────────────────────────────────────
     WEEK 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, as criterion 4 does above.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
