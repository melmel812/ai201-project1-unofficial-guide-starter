# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

The diverse culinary landscape of San Mateo, CA, emphasizing independent, culturally authentic neighborhood staples, regional fusion hubs, and local logistics (such as lines, wait times, and dietary accessibility).

**Why it's hard to find otherwise:** Traditional search engines surface standard star ratings and sponsored review lists, but fail to capture nuanced community consensus about which spots are chains versus authentic mom-and-pop operations. Aggregate platforms also obscure hyper-local operational realities — like knowing exactly when a bakery sells out of sourdough, or which back-alley food hall stands are cash-only/takeout-exclusive.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit r/SanMateo — Best Non-Chain Restaurant Dinners | Community forum | https://www.reddit.com/r/SanMateo/comments/1kusnwt/best_non_chain_restaurant_in_san_mateo_i_wanna/ |
| 2 | Reddit r/SanMateo — Ultimate Restaurant Recommendation Megathread | Community forum | https://www.reddit.com/r/SanMateo/comments/1ad3cl9/best_restaurants/ |
| 3 | Reddit r/SanMateo — Favorite Neighborhood Spots (Any Cuisine) | Community forum | https://www.reddit.com/r/SanMateo/comments/1lyrvba/favorite_neighborhood_spots_any_cuisine/ |
| 4 | San Mateo Daily Journal — Local Food & Lifestyle Features | Regional press | https://www.smdailyjournal.com/lifestyle/food/ |
| 5 | San Mateo Daily Journal — Interactive Food Story Map | Regional press / map | https://sm-dj.com/foodmap/ |
| 6 | The MICHELIN Guide — San Mateo Dining Selections | Expert curation | https://guide.michelin.com/us/en/california/san-mateo/restaurants |
| 7 | Yelp — Top-Rated Late Night Eats in San Mateo | Niche directory | https://www.yelp.com/search?find_desc=Late+Night+Food&find_loc=San+Mateo%2C+CA (`docs/yelp_late_night.md`) |
| 8 | HappyCow — Vegan and Vegetarian San Mateo | Dietary directory | https://www.happycow.net/north_america/usa/california/san_mateo/ (`docs/happycow_vegetarian.md`) |
| 9 | Sweet Maple San Mateo — Brunch Operations & Menu | Restaurant site | https://www.sweetmaplesf.com/ |
| 10 | Suruki Market & Takahashi Market — Prepared Foods/Deli Guides | Market guides | https://www.yelp.com/search?find_desc=Japanese+Grocery&find_loc=San+Mateo%2C+CA (`docs/japanese_hawaiian_markets.md`) |

**Source format notes:**
- Reddit threads: highly fragmented casual prose; single-sentence recommendations buried in long personal anecdotes.
- Daily Journal & Michelin: structured paragraph-dense blocks with context, history, and address data woven together.
- Yelp/HappyCow directories: structured metadata (price points, hours, tags) alongside short repetitive user reviews.

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** The corpus is a hybrid of highly fragmented conversational prose (Reddit) and dense structured paragraphs (journalism, Michelin). A 500-character chunk isolates individual Reddit recommendations cleanly while preserving enough sentence structure for the editorial articles. The 100-character overlap ensures that restaurant names and their associated details aren't split across chunk boundaries, keeping retrieval context intact.

**Final chunk count:** 114 chunks across 10 documents (8–19 chunks per document)

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via the `sentence-transformers` library

**Production tradeoff reflection:** This model provides an optimal balance between low latency and semantic accuracy for short-to-medium text spans. At scale with no cost constraints, tradeoffs to consider: shifting to `text-embedding-3-large` for larger context windows; using models fine-tuned on colloquial text to better parse slang-heavy restaurant reviews; adding multilingual model support given San Mateo's diverse communities; and weighing API-hosted vs. local inference latency.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt explicitly prohibits the model from using training knowledge. The exact instruction injected before every query:

```
You are a local food guide assistant for San Mateo, CA.

Answer the user's question using ONLY the information provided in the DOCUMENTS section below.
Do not use any knowledge from your training data. Do not guess or infer details not present in the documents.

If the documents do not contain enough information to answer the question fully, say:
"I don't have enough information in my sources to answer that."

After your answer, list the source document(s) you drew from, like this:
Sources: [filename1, filename2]

DOCUMENTS:
{retrieved chunks injected here}
```

Two additional structural mechanisms reinforce grounding:
1. **Distance cutoff filter** (`DISTANCE_CUTOFF = 0.55`): chunks with a cosine distance above 0.55 are dropped before being passed to the LLM, so loosely-related content never reaches the prompt.
2. **Low temperature** (`temperature=0.2`): reduces the model's tendency to interpolate or generate beyond the provided context.

**How source attribution is surfaced in the response:**

Attribution is enforced at two levels. The system prompt instructs the model to append `Sources: [filename1, filename2]` at the end of every answer. Additionally, `query_engine.py` programmatically extracts the `source` field from every retrieved chunk and returns it as a separate `sources` list — so even if the LLM omits the citation, the Gradio interface always displays which documents were retrieved in a dedicated "Retrieved from" field.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "Which San Mateo restaurant received a Michelin Bib Gourmand award?"

**What the system returned:** The correct answer (Pausa) appeared at rank 1 with distance 0.34. However, rank 3 returned the Reddit megathread post header — `"Let's build the ultimate San Mateo restaurant list. Drop your favorites by category."` — with a distance of 0.42, and rank 5 returned another generic Reddit post opener about finding a nice dinner. Neither chunk contains information about Michelin awards.

**Root cause (tied to a specific pipeline stage):** The failure is in the **embedding/retrieval stage**. Generic "restaurant recommendation" language in the Reddit post headers shares enough semantic space with the query about restaurant awards that `all-MiniLM-L6-v2` assigned them moderate similarity scores. The model embeds both "which restaurant is the best" and "which restaurant got an award" into nearby regions of the vector space because both are restaurant-evaluation queries — the model has no mechanism to distinguish award-specific vocabulary from general recommendation vocabulary at this distance.

**What you would change to fix it:** Two options. First, add a **distance cutoff filter** in the retrieval step: any chunk with distance above 0.40 gets dropped from the context before being passed to the LLM, which would have excluded both off-target Reddit chunks. Second, improve chunk content by **prepending document-type labels** to each chunk at ingestion time (e.g., `[SOURCE: Michelin Guide]` or `[SOURCE: Reddit community thread]`), so the embedding carries the source type as part of its semantic signal rather than relying purely on content similarity.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
