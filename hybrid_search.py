"""
Stretch Feature: Hybrid Search — BM25 + Semantic via Reciprocal Rank Fusion.

BM25 excels at exact keyword matches (proper nouns, specific dish names).
Semantic search excels at conceptual queries where the exact words differ.
RRF combines both rankings: score = sum(1 / (k + rank)) across methods.

Usage:
  python hybrid_search.py "What topping should you add to the kalbijjim at Daeho?"
  python hybrid_search.py --compare "Where can I get food after 10 PM?"
"""

import json
import argparse
import re
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

CHUNKS_FILE = Path(__file__).parent / "chunks.json"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "san_mateo_food_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
RRF_K = 60  # standard RRF constant; higher = less weight on top ranks


def load_chunks():
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def build_bm25(chunks: list[dict]) -> BM25Okapi:
    tokenized = [tokenize(c["text"]) for c in chunks]
    return BM25Okapi(tokenized)


def bm25_retrieve(query: str, bm25: BM25Okapi, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
    return [
        {**chunks[i], "bm25_score": round(float(s), 4), "bm25_rank": rank + 1}
        for rank, (i, s) in enumerate(ranked)
    ]


def semantic_retrieve(query: str, collection, model: SentenceTransformer, k: int = TOP_K) -> list[dict]:
    embedding = model.encode([query])
    results = collection.query(
        query_embeddings=embedding.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for rank, (doc, meta, dist) in enumerate(zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    )):
        hits.append({
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "semantic_distance": round(dist, 4),
            "semantic_rank": rank + 1,
        })
    return hits


def rrf_score(rank: int, k: int = RRF_K) -> float:
    return 1.0 / (k + rank)


def hybrid_retrieve(query: str, bm25: BM25Okapi, chunks: list[dict],
                    collection, model: SentenceTransformer, k: int = TOP_K) -> list[dict]:
    """Combine BM25 and semantic rankings via Reciprocal Rank Fusion."""
    bm25_hits = bm25_retrieve(query, bm25, chunks, k=k * 2)
    sem_hits = semantic_retrieve(query, collection, model, k=k * 2)

    # Build score maps keyed by chunk identity
    scores: dict[str, float] = {}
    chunk_data: dict[str, dict] = {}

    for h in bm25_hits:
        key = f"{h['source']}::{h['chunk_index']}"
        scores[key] = scores.get(key, 0) + rrf_score(h["bm25_rank"])
        chunk_data[key] = {**h}

    for h in sem_hits:
        key = f"{h['source']}::{h['chunk_index']}"
        scores[key] = scores.get(key, 0) + rrf_score(h["semantic_rank"])
        if key not in chunk_data:
            chunk_data[key] = {**h}
        else:
            chunk_data[key]["semantic_distance"] = h.get("semantic_distance")
            chunk_data[key]["semantic_rank"] = h.get("semantic_rank")

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    results = []
    for rank, (key, rrf) in enumerate(ranked):
        entry = chunk_data[key].copy()
        entry["rrf_score"] = round(rrf, 5)
        entry["hybrid_rank"] = rank + 1
        results.append(entry)
    return results


def print_comparison(query: str, bm25_hits, sem_hits, hybrid_hits):
    print(f"\n{'='*65}")
    print(f"QUERY: {query}")
    print(f"{'='*65}")

    print(f"\n--- BM25 (keyword) top {TOP_K} ---")
    for h in bm25_hits:
        print(f"  [{h['bm25_rank']}] score={h['bm25_score']:.3f}  {h['source']}")
        print(f"       {h['text'][:120].strip()}...")

    print(f"\n--- Semantic top {TOP_K} ---")
    for h in sem_hits:
        print(f"  [{h['semantic_rank']}] dist={h['semantic_distance']}  {h['source']}")
        print(f"       {h['text'][:120].strip()}...")

    print(f"\n--- Hybrid (RRF) top {TOP_K} ---")
    for h in hybrid_hits:
        bm25_r = h.get("bm25_rank", "—")
        sem_r = h.get("semantic_rank", "—")
        print(f"  [{h['hybrid_rank']}] rrf={h['rrf_score']}  bm25_rank={bm25_r}  sem_rank={sem_r}  {h['source']}")
        print(f"       {h['text'][:120].strip()}...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", help="Query to run")
    parser.add_argument("--compare", action="store_true", help="Show side-by-side BM25 vs semantic vs hybrid")
    args = parser.parse_args()

    query = args.query or input("Query: ").strip()

    print("Loading chunks and models...")
    chunks = load_chunks()
    bm25 = build_bm25(chunks)
    model = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    if args.compare or True:
        bm25_hits = bm25_retrieve(query, bm25, chunks)
        sem_hits = semantic_retrieve(query, collection, model)
        hybrid_hits = hybrid_retrieve(query, bm25, chunks, collection, model)
        print_comparison(query, bm25_hits, sem_hits, hybrid_hits)
    else:
        hybrid_hits = hybrid_retrieve(query, bm25, chunks, collection, model)
        for h in hybrid_hits:
            print(f"[{h['hybrid_rank']}] {h['source']}  rrf={h['rrf_score']}")
            print(h["text"][:200])
            print()


if __name__ == "__main__":
    main()
