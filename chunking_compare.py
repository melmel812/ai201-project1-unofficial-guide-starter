"""
Stretch Feature: Chunking Strategy Comparison.

Compares Strategy A (500 chars / 100 overlap) vs Strategy B (300 chars / 50 overlap)
on the same query set using two separate ChromaDB collections.

Usage:
  python chunking_compare.py          # build both collections and run comparison
  python chunking_compare.py --build  # rebuild collections only
"""

import json
import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingest import load_documents, clean_text

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

STRATEGIES = {
    "A_500_100": {"chunk_size": 500, "chunk_overlap": 100, "collection": "san_mateo_food_guide"},
    "B_300_50":  {"chunk_size": 300, "chunk_overlap": 50,  "collection": "san_mateo_food_guide_300_50"},
}

COMPARISON_QUERIES = [
    "What topping should you add to the kalbijjim at Daeho?",
    "Where can I get food after 10 PM in San Mateo?",
    "What should I order at Suruki Market?",
]


def build_chunks(chunk_size: int, chunk_overlap: int) -> list[dict]:
    documents = load_documents(DOCS_DIR)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for doc in documents:
        cleaned = clean_text(doc["raw_text"])
        for i, text in enumerate(splitter.split_text(cleaned)):
            text = text.strip()
            if text:
                chunks.append({"source": doc["source"], "chunk_index": i, "text": text})
    return chunks


def load_or_build_collection(client, strategy_name: str, config: dict,
                              model: SentenceTransformer, rebuild: bool = False) -> chromadb.Collection:
    col_name = config["collection"]
    existing = [c.name for c in client.list_collections()]

    if col_name in existing and not rebuild:
        print(f"  Using existing collection: {col_name}")
        return client.get_collection(col_name)

    if col_name in existing:
        client.delete_collection(col_name)

    chunks = build_chunks(config["chunk_size"], config["chunk_overlap"])
    print(f"  Strategy {strategy_name}: {len(chunks)} chunks  "
          f"(size={config['chunk_size']}, overlap={config['chunk_overlap']})")

    collection = client.create_collection(col_name, metadata={"hnsw:space": "cosine"})
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=False, batch_size=32)
    collection.add(
        ids=[f"{c['source']}::chunk_{c['chunk_index']}" for c in chunks],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    return collection


def retrieve_top(query: str, collection, model: SentenceTransformer, k: int = 3) -> list[dict]:
    emb = model.encode([query])
    results = collection.query(
        query_embeddings=emb.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": doc, "source": meta["source"], "distance": round(dist, 4)}
        for doc, meta, dist in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )
    ]


def run_comparison(collections: dict, model: SentenceTransformer):
    results = {}
    for query in COMPARISON_QUERIES:
        results[query] = {}
        for name, col in collections.items():
            results[query][name] = retrieve_top(query, col, model)
    return results


def print_comparison(results: dict):
    strategy_names = list(next(iter(results.values())).keys())
    for query, strategies in results.items():
        print(f"\n{'='*65}")
        print(f"QUERY: {query}")
        print(f"{'='*65}")
        for sname in strategy_names:
            cfg = STRATEGIES[sname]
            print(f"\n  [{sname}]  chunk_size={cfg['chunk_size']}  overlap={cfg['chunk_overlap']}")
            for i, hit in enumerate(strategies[sname], 1):
                print(f"    [{i}] dist={hit['distance']}  {hit['source']}")
                print(f"         {hit['text'][:130].strip()}...")


def save_results(results: dict, path: Path):
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true", help="Force rebuild both collections")
    args = parser.parse_args()

    print(f"Loading embedding model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    print("\nBuilding / loading collections...")
    collections = {}
    for name, config in STRATEGIES.items():
        collections[name] = load_or_build_collection(client, name, config, model, rebuild=args.build)

    print("\nRunning comparison queries...")
    results = run_comparison(collections, model)
    print_comparison(results)
    save_results(results, Path(__file__).parent / "chunking_comparison_results.json")


if __name__ == "__main__":
    main()
