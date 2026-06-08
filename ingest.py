"""
Milestone 3: Document ingestion and chunking pipeline.
Loads all .md files from docs/, cleans them, and splits into chunks
using RecursiveCharacterTextSplitter (500 chars, 100 overlap).
"""

import os
import re
import json
import random
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCS_DIR = Path(__file__).parent / "docs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_documents(docs_dir: Path) -> list[dict]:
    """Load all .md files from docs_dir, returning list of {source, text} dicts."""
    documents = []
    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        documents.append({"source": path.name, "raw_text": text})
    return documents


def clean_text(text: str) -> str:
    """
    Remove document boilerplate while preserving substantive content.
    Strips: HTML tags, header metadata lines (Source:/URL:/Collected:),
    horizontal rules, excess blank lines, and HTML entities.
    """
    # Strip any stray HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'")
    text = text.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")

    # Remove metadata header lines (Source:, URL:, Collected:, File path:)
    text = re.sub(r"^(Source|URL|Collected|File path):.*$", "", text, flags=re.MULTILINE)

    # Remove markdown horizontal rules
    text = re.sub(r"^---+$", "", text, flags=re.MULTILINE)

    # Remove lines that are only dashes/equals (section dividers)
    text = re.sub(r"^[=\-]{3,}$", "", text, flags=re.MULTILINE)

    # Collapse 3+ consecutive blank lines into a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Split cleaned documents into chunks; attach source metadata to each chunk."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        cleaned = clean_text(doc["raw_text"])
        splits = splitter.split_text(cleaned)
        for i, text in enumerate(splits):
            text = text.strip()
            if len(text) == 0:
                continue
            chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": text,
                "char_count": len(text),
            })
    return chunks


def inspect_chunks(chunks: list[dict], n: int = 5) -> None:
    """Print n random chunks for manual review."""
    sample = random.sample(chunks, min(n, len(chunks)))
    print(f"\n{'='*60}")
    print(f"CHUNK INSPECTION: {n} random samples")
    print(f"{'='*60}")
    for i, chunk in enumerate(sample, 1):
        print(f"\n[Chunk {i}] source={chunk['source']}  index={chunk['chunk_index']}  chars={chunk['char_count']}")
        print(f"{'-'*40}")
        print(chunk["text"])
    print(f"\n{'='*60}\n")


def save_chunks(chunks: list[dict], output_path: Path) -> None:
    """Persist chunks to JSON for use in the embedding stage."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def main():
    print(f"Loading documents from: {DOCS_DIR}")
    documents = load_documents(DOCS_DIR)

    if not documents:
        print("ERROR: No .md files found in docs/. Add source documents before running.")
        return

    print(f"Loaded {len(documents)} documents:")
    for doc in documents:
        print(f"  - {doc['source']}  ({len(doc['raw_text'])} chars raw)")

    chunks = chunk_documents(documents)

    # Checkpoint: verify no empty chunks slipped through
    empty = [c for c in chunks if len(c["text"].strip()) == 0]
    if empty:
        print(f"WARNING: {len(empty)} empty chunks detected and will be excluded.")
        chunks = [c for c in chunks if len(c["text"].strip()) > 0]

    print(f"\nChunking complete.")
    print(f"  Chunk size:    {CHUNK_SIZE} chars")
    print(f"  Overlap:       {CHUNK_OVERLAP} chars")
    print(f"  Total chunks:  {len(chunks)}")

    # Per-source breakdown
    print("\nChunks per source:")
    from collections import Counter
    counts = Counter(c["source"] for c in chunks)
    for source, count in sorted(counts.items()):
        print(f"  {source}: {count} chunks")

    inspect_chunks(chunks, n=5)

    output_path = Path(__file__).parent / "chunks.json"
    save_chunks(chunks, output_path)
    print(f"Chunks saved to: {output_path}")


if __name__ == "__main__":
    main()
