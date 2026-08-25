# Staff notes — Project 1

**Staff only. This file does not exist in the starter repo. Do not share the
repository URL with students.**

This repo is the starter with the project completed. It does two jobs: it drives
the week 1 and week 2 follow-alongs, and it is the exemplar of what a strong
submission looks like.

---

## What's different from the starter

| File | What changed |
|---|---|
| `config.py` | `CORPUS` → `city_guides`; `CHUNK_SIZE` 800 → 1200; `CHUNK_OVERLAP` 120 → 200; `THRESHOLD` 0.6 → 0.70, measured |
| `chunker.py` | `split_documents` rewritten — one chunk per `##` section, title and heading prepended. `fallback_split` untouched |
| `questions.py` | Five questions filled in with `expects` phrases |
| `criteria.md` | Five criteria written, with reasons, plus a week 2 revision on criterion 4 |
| `generate.py` | `GROUNDING_INSTRUCTION` — two rules added. **This is the week 2 improvement** |
| `scorer.py` | **New.** The file built live in the week 2 follow-along |
| `README.md` | The submission, both weeks |
| `results/` | Real before and after run logs |
| `SOLUTION_NOTES.md` | This file |

Everything else — `app.py`, `store.py`, `ingest.py`, `gate.py`, `serve.py`,
`run_eval.py`, `RUNNING.md` — is byte-identical to the starter, and should stay
that way. If you change one of them here, change it there too.

---

## Using it in week 1

The follow-along is a **chunker swap on the `practice` corpus in a scratch
clone of the starter** — not in this repo. Instructor guide, segment 3.

What this repo gives you for week 1:

- **The "before" state, still runnable.** `chunker.fallback_split` is intact.
  `python app.py --corpus practice index` after temporarily pointing
  `split_documents` at it reproduces exactly what students see.
- **A worked Milestone 3 to compare against**, if the room wants to see one
  after they've written their own. Show it *after*, never before — the
  strategy is supposed to come from the corpus they picked, and this one is
  written for a corpus most of them won't have.
- **The Milestone 4 distance table**, in `README.md` under Sample Answer. This
  is the single most useful thing to put on screen in week 1: two groups of
  numbers, a visible gap, and a cutoff in the gap.

Reproduce the numbers with:

```bash
python app.py index
python app.py chunks -n 5
python run_eval.py --label before
```

---

## Using it in week 2

`scorer.py` is the artifact built live in segment 3. **Read it before you
teach** — the docstring is the design conversation, and it's longer than the
code on purpose.

The contract that matters: `run_eval.py::load_scorer` imports `scorer` and
looks for

```python
judge(question, expects, answer, results) -> bool
```

If the scorer you build live ends up with a different name or signature,
`run_eval.py` silently runs unscored and the room will think it's broken. Say
the signature out loud before anyone types.

**The deliberately mediocre system the pre-session checklist asks for is already
here.** Criterion 5 misses, reproducibly, on all three runs — the model answers
"Kestrelford and Corry Vale have no public transport" when the source says
Kestrelford has no transport *within the town*. To show the miss live:

```bash
git stash            # or revert the two added rules in GROUNDING_INSTRUCTION
python run_eval.py --label demo
```

Two things in that failure are worth the room's time:

1. **It's a generation failure with clean retrieval**, which is the segment 3
   teaching hook made concrete — the right chunks came back and the answer is
   still wrong, so fixing the chunker would feel productive and change nothing.
2. **The substring scorer marks it PASS.** `expects` is "Corry Vale", the wrong
   answer contains "Corry Vale". This is the best available argument for why
   some criteria stay manual, and it costs nothing to show.

`criteria.md` criterion 4 carries a worked **legitimate revision** for segment 4
— the original line left in place, the revision underneath, the reason naming a
measurement problem rather than a missed number. Use it against the
illegitimate example rather than inventing one.

---

## Deliberate choices, so nobody "fixes" them

- **Criterion 5 misses.** Do not tune this repo into a clean sweep. A staff
  exemplar that passes everything contradicts the thing every guide in the pair
  says out loud.
- **The improvement is a prompt change, not hybrid search.** It's the boring
  option and it's the one the diagnosis pointed at. The README says so
  explicitly, including that hybrid search was the first instinct and was wrong.
  That paragraph is the whole point of criterion 9.
- **Criterion 1 passes 5/5 in both logs and the README says that's a fault.**
  A criterion that can't move isn't measuring the system. "What I'd Do
  Differently" names the tighter version.
- **`rank-bm25` is still unused.** It ships for students who pick hybrid search.

---

## Before each term

- Re-run everything end to end on a clean machine. `results/` is checked in and
  the README quotes exact distances — if the embedding model or `chromadb`
  moves, those numbers move and both files need updating together.
- Confirm `config.MODEL` is still a current model id.
- Confirm `REQUESTS_PER_MINUTE` in `config.py` against the AI Studio rate-limit
  dashboard for a real student account. Google no longer publishes free-tier
  limits, so the shipped value is an assumption, and the starter carries it too.
- Delete any local `chroma_db/` before testing. It's gitignored, so students
  never see yours — but a database written by a newer `chromadb` than
  `requirements.txt` pins fails on read with `KeyError: '_type'`, which reads
  as a code bug and isn't one.
