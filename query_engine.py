"""
Milestone 5: Grounded generation engine.

Loads the ChromaDB vector store, retrieves top-k chunks for a query,
then calls the Groq LLM with a grounding-enforcing system prompt.

Usage:
  python query_engine.py "What topping should you add to the kalbijjim at Daeho?"
  python query_engine.py --no-llm "What topping should you add to the kalbijjim at Daeho?"
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "san_mateo_food_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5
DISTANCE_CUTOFF = 0.55  # drop chunks with distance above this threshold

SYSTEM_PROMPT = """You are a local food guide assistant for San Mateo, CA.

Answer the user's question using ONLY the information provided in the DOCUMENTS section below.
Do not use any knowledge from your training data. Do not guess or infer details not present in the documents.

If the documents do not contain enough information to answer the question fully, say:
"I don't have enough information in my sources to answer that."

After your answer, list the source document(s) you drew from, like this:
Sources: [filename1, filename2]

DOCUMENTS:
{context}"""


def load_retriever():
    """Load the ChromaDB collection and embedding model."""
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"Vector store not found at {CHROMA_DIR}. Run `python vector_store.py` first."
        )
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer(EMBED_MODEL)
    return collection, model


def retrieve(query: str, collection, model, k: int = TOP_K) -> list[dict]:
    """Return top-k chunks filtered by distance cutoff."""
    embedding = model.encode([query])
    results = collection.query(
        query_embeddings=embedding.tolist(),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if dist <= DISTANCE_CUTOFF:
            hits.append({
                "text": doc,
                "source": meta["source"],
                "chunk_index": meta["chunk_index"],
                "distance": round(dist, 4),
            })
    return hits


def build_context(hits: list[dict]) -> str:
    """Format retrieved chunks into the context block injected into the system prompt."""
    if not hits:
        return "(No relevant documents found.)"
    parts = []
    for i, hit in enumerate(hits, 1):
        parts.append(f"[Document {i} — {hit['source']}]\n{hit['text']}")
    return "\n\n".join(parts)


def generate(query: str, hits: list[dict], client: Groq) -> str:
    """Call the Groq LLM with grounded context and return the response text."""
    context = build_context(hits)
    filled_prompt = SYSTEM_PROMPT.format(context=context)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": filled_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.2,  # low temp for factual, document-grounded answers
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()


def ask(query: str, collection=None, model=None, groq_client=None) -> dict:
    """
    Full RAG pipeline: retrieve → ground → generate.
    Returns {"answer": str, "sources": list[str], "hits": list[dict]}.
    Callers can pass pre-loaded collection/model/client to avoid reloading.
    """
    if collection is None or model is None:
        collection, model = load_retriever()

    hits = retrieve(query, collection, model)
    sources = sorted(set(h["source"] for h in hits))

    if groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise EnvironmentError(
                "GROQ_API_KEY not set. Copy .env.example to .env and add your key."
            )
        groq_client = Groq(api_key=api_key)

    answer = generate(query, hits, groq_client)
    return {"answer": answer, "sources": sources, "hits": hits}


def retrieval_only(query: str, collection=None, model=None) -> dict:
    """Return retrieved chunks without calling the LLM — useful when no API key is available."""
    if collection is None or model is None:
        collection, model = load_retriever()
    hits = retrieve(query, collection, model)
    sources = sorted(set(h["source"] for h in hits))
    context = build_context(hits)
    return {"hits": hits, "sources": sources, "context": context}


def main():
    parser = argparse.ArgumentParser(description="Query the San Mateo food guide RAG system.")
    parser.add_argument("query", nargs="?", help="Question to ask")
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip LLM generation and print retrieved chunks only (no API key needed)",
    )
    args = parser.parse_args()

    query = args.query or input("Ask a question: ").strip()
    if not query:
        print("No query provided.")
        sys.exit(1)

    print(f"\nQuery: {query}")

    collection, model = load_retriever()

    if args.no_llm:
        result = retrieval_only(query, collection, model)
        print(f"\n--- Retrieved chunks (top {TOP_K}, cutoff={DISTANCE_CUTOFF}) ---")
        for i, hit in enumerate(result["hits"], 1):
            print(f"\n[{i}] {hit['source']}  distance={hit['distance']}")
            print(hit["text"])
        print(f"\nSources: {result['sources']}")
    else:
        result = ask(query, collection, model)
        print(f"\n--- Answer ---\n{result['answer']}")
        print(f"\nSources: {result['sources']}")


if __name__ == "__main__":
    main()
