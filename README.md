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

**Final chunk count:** *(to be filled after ingestion runs)*

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via the `sentence-transformers` library

**Production tradeoff reflection:** This model provides an optimal balance between low latency and semantic accuracy for short-to-medium text spans. At scale with no cost constraints, tradeoffs to consider: shifting to `text-embedding-3-large` for larger context windows; using models fine-tuned on colloquial text to better parse slang-heavy restaurant reviews; adding multilingual model support given San Mateo's diverse communities; and weighing API-hosted vs. local inference latency.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

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

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

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
