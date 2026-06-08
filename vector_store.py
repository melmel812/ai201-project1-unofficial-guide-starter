"""
Milestone 4: Embed chunks and load into ChromaDB, then test retrieval.

Usage:
  python vector_store.py            # build the vector store
  python vector_store.py --test     # build + run evaluation queries
"""

import json
import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path(__file__).parent / "chunks.json"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "san_mateo_food_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


def load_chunks(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_vector_store(chunks: list[dict], model: SentenceTransformer) -> chromadb.Collection:
    """Embed all chunks and persist to ChromaDB. Recreates the collection on each run."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Drop and recreate so re-runs don't accumulate duplicates
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks with {EMBED_MODEL}...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    collection.add(
        ids=[f"{c['source']}::chunk_{c['chunk_index']}" for c in chunks],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )

    print(f"Stored {collection.count()} chunks in ChromaDB at {CHROMA_DIR}")
    return collection


def retrieve(query: str, collection: chromadb.Collection, model: SentenceTransformer, k: int = TOP_K) -> list[dict]:
    """Return top-k chunks for a query with distance scores and source metadata."""
    query_embedding = model.encode([query])
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({"text": doc, "source": meta["source"], "chunk_index": meta["chunk_index"], "distance": round(dist, 4)})
    return hits


def print_retrieval_results(query: str, hits: list[dict]) -> None:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")
    for i, hit in enumerate(hits, 1):
        relevance = "STRONG" if hit["distance"] < 0.3 else ("OK" if hit["distance"] < 0.5 else "WEAK")
        print(f"\n[{i}] source={hit['source']}  chunk={hit['chunk_index']}  distance={hit['distance']}  [{relevance}]")
        print(f"{'-'*40}")
        print(hit["text"])


def run_evaluation_queries(collection: chromadb.Collection, model: SentenceTransformer) -> None:
    """Run the 3 core evaluation queries from planning.md and print results."""
    queries = [
        "What topping should you add to the kalbijjim at Daeho?",
        "Which San Mateo restaurant received a Michelin Bib Gourmand award?",
        "What is Sweet Maple known for on its brunch menu?",
    ]
    for q in queries:
        hits = retrieve(q, collection, model)
        print_retrieval_results(q, hits)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run evaluation queries after building")
    args = parser.parse_args()

    chunks = load_chunks(CHUNKS_FILE)
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)

    collection = build_vector_store(chunks, model)

    if args.test:
        run_evaluation_queries(collection, model)


if __name__ == "__main__":
    main()
