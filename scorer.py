"""
Does an answer count as correct?

⚠️ STAFF SOLUTION — this is the file built live in the week 2 follow-along
(instructor guide, segment 3). It does NOT ship in the starter, on purpose:
`run_eval.py` handles the mechanical half and stops exactly where the judgment
starts, because deciding what counts as correct is the lesson.

`run_eval.py::load_scorer` imports this file if it exists and looks for one
function:

    judge(question, expects, answer, results) -> bool

Keep that signature. If the live build ends up with a different one, the Run
columns silently stay blank and the room will think the scorer is broken.

The whole implementation is fifteen lines, and the fifteen lines are not the
point. The conversation is: **a substring test is wrong in both directions,**
and students should leave able to say how.

  - False negatives. "half eight" and "20:30" are both correct answers to
    question 1 and neither contains "8:30". The scorer marks them failed.
  - False positives. An answer that says "the pubs do NOT serve until 8:30"
    contains the string and gets marked passed.

Every richer option costs something, and that trade is the design discussion
worth having in the room:

  - a list of accepted phrasings per question — cheap and deterministic, but
    you are now maintaining the list, and you only discover a missing phrasing
    by mis-scoring a run
  - a regex or fuzzy match — catches formatting drift, still blind to negation
  - an LLM judging the answer — handles both problems above, costs a model call
    per question per run, and introduces a scorer that doesn't return the same
    verdict twice

This one is the cheapest thing that is honest about being cheap. It stays
because the run log is read by a person, and the substring verdict is a first
pass that tells that person which answers are worth reading closely.
"""


def judge(question: str, expects: str, answer: str, results) -> bool:
    """
    True when the answer contains the phrase a correct answer has to contain.

    `results` — the retrieved chunks — is in the signature and unused here on
    purpose. It is what you reach for if you want to separate the two questions
    every RAG eval has to answer: was the right thing retrieved, and did the
    model use it? `retrieval_hit` below is that second scorer, and criterion 1
    in criteria.md is scored with it rather than with this function.
    """
    if not expects:
        return False
    return expects.strip().lower() in (answer or "").lower()


def retrieval_hit(expects: str, results) -> bool:
    """
    True when the expected phrase is in at least one RETRIEVED CHUNK.

    This is the criterion-1 scorer, and it is a different measurement from
    `judge`. A question where this is True and `judge` is False is a generation
    failure; one where both are False is a retrieval failure. Splitting them is
    what makes the week 2 diagnosis a lookup rather than a guess.
    """
    if not expects:
        return False
    needle = expects.strip().lower()
    return any(needle in (r.text or "").lower() for r in results)
