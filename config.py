"""
Settings for The Unofficial Guide.

⚠️ STAFF SOLUTION. The starter ships CORPUS="campus_life", CHUNK_SIZE=800,
CHUNK_OVERLAP=120 and THRESHOLD=0.6. Every one of those four numbers has been
changed here, and each change is defended in README.md — which is the actual
deliverable. A student who changes them without being able to say why has done
the typing and not the milestone.

Anything you set in your .env file wins over the defaults here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")


# ─── The corpus you're working with ──────────────────────────────────────────
# Change this to switch corpora, or pass --corpus on the command line.
# Options are the folder names inside corpora/. See corpora/README.md.

CORPUS = os.getenv("AI201_CORPUS", "city_guides")


# ─── Chunking (Milestone 3) ──────────────────────────────────────────────────
# These are no longer a chunk size in the starter's sense. chunker.py cuts on
# `##` section headings, so CHUNK_SIZE is the point at which a section is too
# long to stay in one piece and gets packed onto paragraph boundaries instead.
#
# 1200 because the longest section in city_guides is a shade under 1100
# characters: at this ceiling every section survives whole and the packing path
# only fires on the handful that genuinely need it. 800 would have split about
# a third of them for no reason.
#
# 200 because the overlap here carries a whole trailing PARAGRAPH into the next
# piece rather than a fixed number of characters, and 200 is roughly one
# paragraph in this corpus. Anything longer just duplicated text.

CHUNK_SIZE = 1200       # longest a section may be before it is packed
CHUNK_OVERLAP = 200     # longest trailing paragraph carried into the next piece


# ─── Retrieval (Milestone 4) ─────────────────────────────────────────────────

TOP_K = 5               # how many chunks to pull back per question

# The relevance gate. If the best chunk is further away than this, the system
# refuses to answer instead of handing the model thin material.
#
# LOWER IS BETTER: 0.3 is a close match, 0.9 is unrelated.
#
# Measured in Milestone 4, not guessed. The five in-corpus questions landed
# between 0.165 and 0.591; the three out-of-scope ones between 0.808 and 0.982.
# That is a gap of 0.217 with nothing in it, so the cutoff goes in the middle.
# The table is in README.md.
#
# Note this is well above the starter's 0.6, and 0.6 would have refused
# question 5 (0.591 is close, but the margin is one bad run wide). Reading the
# distances is the milestone; keeping the shipped number is not.
THRESHOLD = 0.70


# ─── Models ──────────────────────────────────────────────────────────────────
# Embeddings run on your own machine and cost no API quota.
# Only generation calls out to a service.

# This is the model Chroma bundles, and leaving it alone is the fast path: it
# downloads about 80 MB from Chroma's own CDN and needs nothing else installed.
#
# Setting it to any other name — week 2's "try a second embedding model"
# stretch option — switches to loading that model from Hugging Face instead,
# which needs `pip install 'sentence-transformers>=3.4,<3.5'` first. store.py
# says so with a real error message rather than a stack trace if you forget.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL = os.getenv("AI201_MODEL", "gemini-3.5-flash-lite")


# ─── Rate limiting and quota guards ──────────────────────────────────────────
# You should not need to touch these. They exist so that a runaway loop costs
# you a warning instead of your whole day's allowance.

REQUESTS_PER_MINUTE = 30       # outgoing calls the limiter will allow per minute
SESSION_REQUEST_BUDGET = 300   # stop and warn rather than draining the daily quota
MAX_RETRIES = 4                # on 429 / resource-exhausted, with backoff

CACHE_ENABLED = os.getenv("AI201_CACHE", "1") != "0"
CACHE_DIR = ROOT / ".cache"


# ─── Paths ───────────────────────────────────────────────────────────────────

CORPORA_DIR = ROOT / "corpora"
CHROMA_DIR = ROOT / "chroma_db"
RESULTS_DIR = ROOT / "results"


def corpus_path(name: str | None = None) -> Path:
    """Folder holding the documents for a corpus."""
    return CORPORA_DIR / (name or CORPUS) / "documents"


def collection_name(name: str | None = None, variant: str = "default") -> str:
    """
    Name of the vector-store collection for a corpus.

    `variant` lets you index the same corpus two different ways and query both
    without deleting anything — you'll want that in week 2 when you compare
    chunking strategies.

    Chroma is fussy about collection names: 3 to 63 characters, starting and
    ending with a letter or digit, and nothing but letters, digits, underscores
    and hyphens in between. If you bring your own corpus and name the folder
    something Chroma won't accept, this cleans it up rather than failing.
    """
    import re

    raw = f"{name or CORPUS}__{variant}"
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "-", raw)
    cleaned = cleaned.strip("_-")          # must start and end alphanumeric
    if not cleaned or not cleaned[0].isalnum():
        cleaned = f"c{cleaned}"
    if not cleaned[-1].isalnum():
        cleaned = f"{cleaned}0"
    return cleaned[:63].rstrip("_-") or "collection"
