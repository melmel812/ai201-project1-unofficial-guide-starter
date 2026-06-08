"""
Milestone 5: Gradio web interface for the San Mateo Food Guide RAG system.

Run:
  python app.py
Then open http://localhost:7860 in your browser.

Requires GROQ_API_KEY in .env. If the key is missing, the interface loads
but returns an error message explaining what to set up.
"""

import os
from dotenv import load_dotenv
import gradio as gr
from groq import Groq
from sentence_transformers import SentenceTransformer
from query_engine import ask, retrieval_only, load_retriever, EMBED_MODEL, LLM_MODEL, TOP_K

load_dotenv()

# Load retriever once at startup so every query reuses the same loaded model
_collection, _model = load_retriever()

# Initialize Groq client if API key is present
_api_key = os.getenv("GROQ_API_KEY", "")
_groq_client = Groq(api_key=_api_key) if _api_key and _api_key != "your_key_here" else None


def handle_query(question: str):
    question = question.strip()
    if not question:
        return "Please enter a question.", ""

    if _groq_client is None:
        # Fallback: show retrieved chunks so the UI is still useful without a key
        result = retrieval_only(question, _collection, _model)
        if not result["hits"]:
            return "No relevant documents found for that query.", ""
        chunks_display = "\n\n".join(
            f"[{i+1}] {h['source']} (distance: {h['distance']})\n{h['text']}"
            for i, h in enumerate(result["hits"])
        )
        answer = (
            "⚠️ GROQ_API_KEY not configured — showing retrieved chunks only.\n"
            "Add your key to .env and restart to get full generated answers.\n\n"
            + chunks_display
        )
        sources = "\n".join(f"• {s}" for s in result["sources"])
        return answer, sources

    try:
        result = ask(question, _collection, _model, _groq_client)
        sources = "\n".join(f"• {s}" for s in result["sources"])
        return result["answer"], sources
    except Exception as e:
        return f"Error: {e}", ""


EXAMPLE_QUESTIONS = [
    "What topping should you add to the kalbijjim at Daeho?",
    "Which San Mateo restaurant has a Michelin Bib Gourmand?",
    "What is Sweet Maple known for and how long is the wait?",
    "Where can I get food after 10 PM in San Mateo?",
    "What should I order at Suruki Market?",
    "When can I get fresh malasadas at Takahashi Market?",
    "What vegan options are available in downtown San Mateo?",
]

with gr.Blocks(title="San Mateo Food Guide", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # San Mateo Unofficial Food Guide
        Ask about local restaurants, hidden gems, hours, dietary options, and neighborhood tips.
        Answers are grounded in community reviews, local press, and curated guides — not general web search.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What should I order at Daeho?",
                lines=2,
            )
            with gr.Row():
                ask_btn = gr.Button("Ask", variant="primary")
                clear_btn = gr.Button("Clear")

        with gr.Column(scale=1):
            gr.Markdown(f"**Model:** `{LLM_MODEL}`\n\n**Sources searched:** 10 documents\n\n**Chunks retrieved:** top {TOP_K}")

    answer_box = gr.Textbox(label="Answer", lines=10, interactive=False)
    sources_box = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    gr.Examples(
        examples=EXAMPLE_QUESTIONS,
        inputs=question_box,
        label="Try these questions",
    )

    ask_btn.click(handle_query, inputs=question_box, outputs=[answer_box, sources_box])
    question_box.submit(handle_query, inputs=question_box, outputs=[answer_box, sources_box])
    clear_btn.click(lambda: ("", "", ""), outputs=[question_box, answer_box, sources_box])

    gr.Markdown(
        """
        ---
        *Answers are generated from retrieved source documents only.
        If sources don't cover a topic, the system will say so rather than guessing.*
        """
    )

if __name__ == "__main__":
    demo.launch()
