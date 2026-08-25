"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ STAFF SOLUTION. In the starter, `split_documents` just calls
`fallback_split` and the docstring tells students to replace it. This is one
worked answer to Milestone 3, written against the `city_guides` corpus.

It is deliberately *a* solution and not *the* solution. A student who splits
`campus_life` one-post-per-chunk and defends it has done the milestone just as
well. What makes this one worth showing is that the strategy comes from
something observable in the documents rather than from a round number:

  - `city_guides` is 14 markdown files averaging ~2,070 characters, each cut
    into labelled `##` sections — getting there, getting around, where to eat,
    when to go.
  - The starter's fixed 800-character window turns them into 51 chunks and
    pays no attention to those headings, so a chunk routinely ends halfway
    through "Where to eat" and starts halfway through "What to see".
  - Worse, a chunk that starts mid-section carries no sign of which *town* it
    is about. "Four pubs, two cafés, and a bakery that sells out by 11am" is
    useless to a reader who can't tell it's Kestrelford.

So: one chunk per `##` section, with the document title and the section
heading prepended so every chunk says what it is about. Sections longer than
`config.CHUNK_SIZE` are packed on paragraph boundaries rather than cut mid-
sentence, and the heading goes back on the front of each piece.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in week 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# ─── The Milestone 3 answer ──────────────────────────────────────────────────


def _split_into_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Break one markdown document into (title, [(heading, body), ...]).

    A line starting with `# ` is the document title. A line starting with `## `
    opens a section. Anything before the first `##` becomes an intro section
    with an empty heading, which is where the one-paragraph scene-setter at the
    top of each guide ends up.
    """
    title = ""
    sections: list[tuple[str, str]] = []
    heading = ""
    body: list[str] = []

    for line in text.split("\n"):
        if line.startswith("## "):
            sections.append((heading, "\n".join(body).strip()))
            heading = line[3:].strip()
            body = []
        elif line.startswith("# ") and not title:
            title = line[2:].strip()
        else:
            body.append(line)

    sections.append((heading, "\n".join(body).strip()))
    return title, [(h, b) for h, b in sections if b]


def _pack_paragraphs(body: str, limit: int, overlap: int) -> list[str]:
    """
    Fit a long section into pieces no bigger than `limit`, cutting only at
    blank lines.

    The last paragraph of a piece is repeated at the front of the next one when
    it fits inside `overlap`. That is the overlap doing something useful — a
    whole thought carried across — rather than an arbitrary number of trailing
    characters.
    """
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    pieces: list[str] = []
    current: list[str] = []

    for paragraph in paragraphs:
        candidate = current + [paragraph]
        if current and sum(len(p) + 2 for p in candidate) > limit:
            pieces.append("\n\n".join(current))
            tail = current[-1]
            current = [tail, paragraph] if len(tail) <= overlap else [paragraph]
        else:
            current = candidate

    if current:
        pieces.append("\n\n".join(current))
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks, one per labelled section.

    Every chunk opens with `Title — Heading` so it can be read on its own. That
    line is not decoration: these guides describe nine different towns in the
    same vocabulary, and a chunk about opening hours that doesn't say which
    town it belongs to will match every question about opening hours equally
    badly.

    Documents with no `##` headings — which is what `campus_life` and most of
    `advice_threads` look like — fall through to paragraph packing, so this
    behaves sensibly on the other corpora rather than only on the one it was
    written for.
    """
    limit = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    chunks: list[Chunk] = []
    for doc in documents:
        title, sections = _split_into_sections(doc.text)
        index = 0

        for heading, body in sections:
            label = " — ".join(part for part in (title, heading) if part)

            for piece in _pack_paragraphs(body, limit, overlap):
                text = f"{label}\n\n{piece}" if label else piece
                chunks.append(
                    Chunk(
                        text=text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
