"""
Your test questions.

⚠️ STAFF SOLUTION. Five questions against the `city_guides` corpus, written in
Milestone 2 before any of them had been run.

Two things worth pointing at when you show this to a room:

1. **`expects` is a string a correct answer has to contain, not a summary of
   the answer.** "8:30" works as a scorer target; "the pubs stop serving in
   the evening" does not, because no scorer can check it and two people would
   score it differently.

2. **Question 5 is deliberately one this system is likely to get wrong.** The
   answer to it is not in any single section of any single document — it has to
   be assembled from two. That is the question that makes week 2 worth having,
   and a set of five questions the system obviously handles is a demo script
   rather than a test.
"""

QUESTIONS = [
    {
        "question": "What time do the pubs in Kestrelford stop serving food in the evening?",
        "expects": "8:30",
    },
    {
        "question": "Which year did the railway line north of Brightwater close?",
        "expects": "1963",
    },
    {
        "question": "Where should I eat in Brightwater to avoid riverside prices?",
        "expects": "Corry Lane",
    },
    {
        "question": "How often do the Marchwood trams run on weekdays?",
        "expects": "8 minutes",
    },
    {
        "question": "Which places in the region have no public transport at all?",
        "expects": "Corry Vale",
    },
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
