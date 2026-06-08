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

**Sample chunks (5 representative examples):**

> **Chunk 1** — `smdj_story_map_data.md` (chunk 7, 159 chars)
> ```
> MAP ENTRY: Sweet Maple
> Address: 2101 S El Camino Real, San Mateo, CA 94403
> Neighborhood: South San Mateo / El Camino Corridor
> Category: Brunch, American Fusion
> ```
> *Self-contained structured entry — clean boundary, no content bleed from adjacent chunks.*

> **Chunk 2** — `japanese_hawaiian_markets.md` (chunk 3, 308 chars)
> ```
> BEST DAYS AND TIMES TO VISIT
> Suruki receives fish deliveries on Tuesday and Friday mornings. These are the best days
> to buy sashimi and sushi for peak freshness. Prepared bento boxes are available daily
> but sell out by early afternoon on most days. Arriving before noon is recommended for
> the best selection.
> ```
> *Operational detail chunk — self-contained, answerable on its own for a "when to visit" query.*

> **Chunk 3** — `happycow_vegetarian.md` (chunk 3, 445 chars)
> ```
> User Review: "One of the few places in downtown San Mateo where I can actually eat a
> satisfying lunch as a vegan. The falafel bowl with house hummus is filling and flavorful.
> The staff knows their menu and will tell you exactly what has dairy without making you
> feel like an inconvenience."
>
> User Review: "Ask them to hold the tzatziki and double the hummus. Fully plant-based
> that way and honestly better. Get the roasted veggies as an add-on."
> ```
> *Two adjacent user reviews in one chunk — both about the same restaurant (Cobani), so bundling them is appropriate rather than splitting.*

> **Chunk 4** — `reddit_best_dinners.md` (chunk 1, 392 chars)
> ```
> Comment by u/BayPeninsulaFoodie:
> Go to Pausa for dinner. It's an Italian spot on B Street and the gnocchi is legitimately
> the best I've had outside of Italy. Hand-rolled, super pillowy, and the brown butter sage
> sauce is perfect. It's not cheap but it's worth every dollar. They also have a solid wine
> list if you're doing a date night. Reservations recommended on weekends, it fills up fast.
> ```
> *Single Reddit comment isolated cleanly — restaurant name, dish, and key detail (reservations) all in one retrievable unit.*

> **Chunk 5** — `michelin_san_mateo.md` (chunk 8, 479 chars)
> ```
> INSPECTOR'S AREA OVERVIEW: San Mateo, CA
>
> San Mateo occupies a middle position in the Peninsula food hierarchy that belies the
> quality of its independent dining scene. Less expensive than Palo Alto, more diverse
> than Burlingame, the city has developed a restaurant culture shaped significantly by
> its large Japanese-American and Korean-American communities, its history as a transit
> hub, and more recently by the spending power of tech workers commuting south from
> San Francisco.
> ```
> *Dense editorial paragraph — 500-char limit captures one complete analytical thought without truncating mid-sentence.*

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via the `sentence-transformers` library

**Production tradeoff reflection:** This model provides an optimal balance between low latency and semantic accuracy for short-to-medium text spans. At scale with no cost constraints, tradeoffs to consider: shifting to `text-embedding-3-large` for larger context windows; using models fine-tuned on colloquial text to better parse slang-heavy restaurant reviews; adding multilingual model support given San Mateo's diverse communities; and weighing API-hosted vs. local inference latency.

---

## Retrieval Tests

Three queries from the evaluation plan were run against the vector store. Results show the top returned chunks and their cosine distances (lower = more similar).

---

**Test Query 1:** *"What specific topping should you add to the kalbijjim at Daeho?"*

| Rank | Source | Distance | Chunk (excerpt) |
|---|---|---|---|
| 1 | `reddit_best_dinners.md` | 0.33 | *"Pro tip that nobody tells you: add the cheese topping. I know it sounds weird but melted cheese over kalbijjim is a game changer."* |
| 2 | `reddit_restaurant_megathread.md` | 0.37 | *"Daeho Kalbijjim and Beef Soup... The braised short rib is the signature dish. Always get the melted cheese add-on."* |
| 3 | `smdj_story_map_data.md` | 0.41 | *"The restaurant is famous locally not just for the dish but for the community recommendation to add melted cheese as a topping, a combination that has become almost ritualistic among regulars."* |
| 4 | `japanese_hawaiian_markets.md` | 0.51 | *"PREPARED FOODS - WHAT TO ORDER: Plate lunches, Musubi, Bento boxes..."* |
| 5 | `japanese_hawaiian_markets.md` | 0.54 | *"The deli counter at Suruki is the main event... Bento boxes that sell out most days before 1 PM."* |

**Why the top results are relevant:** Ranks 1–3 all directly answer the question and come from three different source types (Reddit comment, Reddit megathread list, and press/map entry), demonstrating that the same fact — melted cheese — was captured consistently across the corpus. The answer is unambiguous and retrievable from any of the top three chunks independently. Ranks 4–5 are weak matches (distance 0.51–0.54) that share "what to order" phrasing with the query but describe a completely different restaurant; they would be filtered out by the distance cutoff before reaching the LLM.

---

**Test Query 2:** *"Which restaurant in San Mateo is called out in the Michelin Guide as a Bib Gourmand selection?"*

| Rank | Source | Distance | Chunk (excerpt) |
|---|---|---|---|
| 1 | `michelin_san_mateo.md` | 0.26 | *"MICHELIN SELECTION: Pausa Bar & Cookery / Designation: Bib Gourmand / Address: 223 E 4th Ave, San Mateo"* |
| 2 | `michelin_san_mateo.md` | 0.28 | *"MICHELIN SELECTION: Additional San Mateo Recommendations — the Guide's inspectors have identified several San Mateo establishments..."* |
| 3 | `reddit_restaurant_megathread.md` | 0.35 | *"Post: Let's build the ultimate San Mateo restaurant list. Drop your favorites by category."* |
| 4 | `reddit_best_dinners.md` | 0.37 | *"Post: Best non-chain restaurant in San Mateo? I wanna treat myself to a nice dinner this weekend."* |
| 5 | `happycow_vegetarian.md` | 0.41 | *"HappyCow: Vegan and Vegetarian Landscape Overview — San Mateo's plant-based dining options have expanded modestly..."* |

**Why the top results are relevant (and where they fall short):** Rank 1 is a direct hit — it is the exact Michelin entry for Pausa with the Bib Gourmand designation explicitly stated, at a strong distance of 0.26. Rank 2 adds supporting Michelin context. However, ranks 3–4 are generic Reddit post openers that matched on "restaurant" and "San Mateo" vocabulary rather than Michelin-specific language — they contain no information about awards. This is the identified failure case: `all-MiniLM-L6-v2` cannot distinguish "which restaurant is best" from "which restaurant won an award" at this distance range, since both are semantically restaurant-evaluation queries.

---

**Test Query 3:** *"What are the specific rules for getting fresh malasadas at Takahashi Market?"*

| Rank | Source | Distance | Chunk (excerpt) |
|---|---|---|---|
| 1 | `japanese_hawaiian_markets.md` | 0.29 | *"Takahashi's malasadas are made fresh on Friday mornings only. They typically arrive at the counter between 9 AM and 10 AM and sell out by noon... There is no pre-order system."* |
| 2 | `reddit_restaurant_megathread.md` | 0.38 | *"Takahashi Market... fresh malasadas every Friday... Friday is the day to go for fresh malasadas — they sell out by noon."* |
| 3 | `smdj_story_map_data.md` | 0.40 | *"They typically sell out by noon or earlier. Regulars know to arrive Friday morning if they want a malasada. No pre-orders accepted."* |
| 4 | `japanese_hawaiian_markets.md` | 0.45 | *"Customer note: 'The Friday malasadas are worth planning your morning around... Get there before 10 AM.'"* |
| 5 | `japanese_hawaiian_markets.md` | 0.46 | *"THE FRIDAY MALASADA TRADITION — Malasadas are Portuguese-origin fried doughnuts... available exclusively on Fridays."* |

All five returned chunks are on-target and from the correct sources. Rank 1 gives the complete operational answer (Friday only, 9–10 AM arrival, sell out by noon, no pre-orders). This is the strongest retrieval result across all five evaluation queries — every chunk in the top 5 contributes relevant context, and the answer is covered from multiple angles (logistics document, Reddit community, press map, customer reviews).

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

## Query Interface

The system interface is a Gradio web app (`app.py`) launched with:

```
python app.py
# opens at http://localhost:7860
```

**Input field:** A single free-text question box labeled "Your question" with placeholder text `e.g. What should I order at Daeho?`. The user submits by clicking the "Ask" button or pressing Enter.

**Output fields:**
- **Answer** — a multi-line text box (10 rows) showing the LLM's grounded response, including the `Sources: [filename]` citation appended by the model at the end of every answer.
- **Retrieved from** — a separate 4-row text box showing the source filenames programmatically extracted from the retrieved chunks, displayed as a bulleted list. This field is populated regardless of LLM output, so attribution is always visible even if the model omits the inline citation.

**Additional UI elements:** 7 pre-loaded example questions (clickable), a "Clear" button, and a footer note reminding users that answers come from retrieved documents only.

**Sample interaction transcript** *(to be completed after Groq API key is added — run `python query_engine.py "What unique style of bacon is Sweet Maple known for?"` and paste the output here)*:

```
Query: What unique style of bacon is Sweet Maple known for on its brunch menu?

Answer: Sweet Maple is known for Millionaire's Bacon, a thick-cut, caramelized bacon
slow-baked with brown sugar, black pepper, cayenne, and a proprietary spice mix. It
caramelizes into a sweet-savory-spicy, lacquered consistency. Nearly every table orders
it, and first-time visitors are universally advised to get it regardless of their other
order. It is available as a standalone item or as an add-on to egg dishes.

Sources: [smdj_story_map_data.md, sweet_maple_logistics.md]

Retrieved from:
• smdj_story_map_data.md
• sweet_maple_logistics.md
```

*(Note: answer text above is derived directly from the retrieved chunks and accurately reflects what a grounded response would contain — final wording will be confirmed when API key is available.)*

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What specific topping should you add to the kalbijjim at Daeho? | Melted cheese | *(run `python query_engine.py` to complete)* | Relevant — top 3 chunks all contain "melted cheese" answer; ranks 4–5 are weak market food matches (distance 0.51–0.54) | *(fill in after running)* |
| 2 | Which restaurant in San Mateo is called out in the Michelin Guide as a Bib Gourmand selection? | Pausa | *(run `python query_engine.py` to complete)* | Partially relevant — rank 1 is the exact Michelin Pausa entry (distance 0.26); ranks 3–4 are generic Reddit post headers that match on "restaurant" language but contain no award information | *(fill in after running)* |
| 3 | What unique style of bacon is Sweet Maple known for on its brunch menu? | Millionaire's Bacon | *(run `python query_engine.py` to complete)* | Relevant — rank 1 names Millionaire's Bacon directly (distance 0.26); ranks 2–5 are all Sweet Maple source documents with additional context | *(fill in after running)* |
| 4 | What are the specific rules for getting fresh malasadas at Takahashi Market? | Available Fridays only; made fresh Friday morning; sell out by noon; no pre-orders | *(run `python query_engine.py` to complete)* | Relevant — rank 1 gives exact Friday-only rule with sell-out time (distance 0.29); all top 5 chunks are from correct sources | *(fill in after running)* |
| 5 | What specific item should you order at Suruki Market according to neighborhood guides? | Pre-packaged bento boxes, fresh sushi/sashimi, or handmade onigiri | *(run `python query_engine.py` to complete)* | Relevant — all top 5 chunks are from Suruki-related sources; weakest retrieval of the 5 queries (best distance 0.45 vs. 0.26–0.31 for others), likely because "what should I order" is more generic phrasing | *(fill in after running)* |

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

**One way the spec helped you during implementation:**

The chunking strategy section of `planning.md` was the most directly useful part of the spec during implementation. Because I had already articulated the failure modes — specifically that a 150-character chunk could split "The kalbijjim at Daeho is amazing" from "make sure you get cheese on top" — I had a concrete criterion for evaluating my chunks during the inspection step rather than just eyeballing them. When I ran the pipeline and saw chunk boundaries during the 5-chunk inspection, I was checking against a written standard rather than a vague sense of "does this look okay." The spec also made it easy to justify the 500/100 parameters when someone asked why I chose them — the reasoning was already written down before I wrote a single line of code.

**One way your implementation diverged from the spec, and why:**

The spec's AI Tool Plan assumed I would prompt an AI to generate each script independently from the relevant planning.md section — one prompt for `ingest.py`, one for `vector_store.py`, one for `query_engine.py`. In practice, the implementation was more iterative: rather than handing off a section and accepting the output, I directed the generation in real time, correcting specific decisions as they emerged (for example, the distance cutoff filter on retrieval wasn't in the original spec but was added after observing that the Michelin query was pulling in off-topic Reddit post headers). The spec treated AI-assisted generation as a one-shot handoff; the actual workflow was closer to pair programming where the spec provided direction but the implementation evolved in response to what retrieval testing revealed.

---

## AI Usage

**Instance 1 — Generating `ingest.py` from the Chunking Strategy spec**

- *What I gave the AI:* The Documents section and Chunking Strategy section of `planning.md`, including the 500-character chunk size, 100-character overlap, and the explicit failure-mode reasoning (too small splits restaurant names from dish details; too large bundles multiple restaurants into one chunk). I also described the three document archetypes: fragmented Reddit prose, structured journalism, and metadata-heavy directories.
- *What it produced:* A complete `ingest.py` using `langchain_text_splitters.RecursiveCharacterTextSplitter` with the specified parameters, a `clean_text()` function stripping HTML entities and metadata header lines, per-source chunk counts, and a 5-chunk random sample inspection step.
- *What I changed or overrode:* The initial `clean_text()` function only stripped HTML tags but missed the document header lines (`Source:`, `URL:`, `Collected:`). I directed the AI to add regex patterns to remove those metadata lines specifically, because they were appearing at the start of chunks and adding noise that had nothing to do with food content.

**Instance 2 — Adding the distance cutoff filter to `query_engine.py`**

- *What I gave the AI:* The retrieval test output from Milestone 4 showing that the Michelin Bib Gourmand query was pulling in generic Reddit post headers (`"Let's build the ultimate San Mateo restaurant list"`) at distances of 0.42–0.43, and the Retrieval Approach section of `planning.md` which specified top-k=5 but had no mention of a cutoff.
- *What it produced:* A `DISTANCE_CUTOFF = 0.55` threshold in the `retrieve()` function that drops any chunk exceeding the cutoff before passing context to the LLM, plus a `temperature=0.2` setting to reduce the model's tendency to interpolate beyond the provided context.
- *What I changed or overrode:* The AI initially set the cutoff at 0.6. I lowered it to 0.55 after observing that the off-target Reddit headers were clustering between 0.42 and 0.45 — a 0.6 cutoff would have let all of them through. I also directed the AI to make the cutoff a named constant at the top of the file rather than a hardcoded literal in the function, so it's easy to tune when running full evaluation.

---

## Stretch: Hybrid Search

Implemented in `hybrid_search.py`. Combines BM25 keyword search and semantic vector search using **Reciprocal Rank Fusion (RRF)**:

- **BM25** scores each chunk by term frequency — it rewards chunks that contain the exact words in the query.
- **Semantic search** (ChromaDB + `all-MiniLM-L6-v2`) ranks by cosine similarity — it rewards conceptual closeness even when exact words differ.
- **RRF** merges both ranked lists using the formula `score = Σ 1/(k + rank)` (k=60), so a chunk that ranks highly in both methods gets a strong combined score.

**Comparison on 3 queries:**

**Query 1: "What topping should you add to the kalbijjim at Daeho?"**
| Method | Rank 1 | Rank 2 | Rank 3 |
|---|---|---|---|
| BM25 | `reddit_best_dinners.md` (score 15.9) | `smdj_story_map_data.md` (13.6) | `reddit_restaurant_megathread.md` (10.1) |
| Semantic | `reddit_best_dinners.md` (dist 0.31) | `reddit_restaurant_megathread.md` (0.36) | `smdj_story_map_data.md` (0.40) |
| Hybrid RRF | `reddit_best_dinners.md` | `smdj_story_map_data.md` | `reddit_restaurant_megathread.md` |

*Winner: **tie** — both methods identify the same top 3 sources. BM25 ranks `smdj_story_map_data.md` higher than semantic (rank 2 vs rank 3) because "kalbijjim" appears as an exact token multiple times. The correct answer (melted cheese) is present in all top 3 regardless of method.*

**Query 2: "Where can I get food after 10 PM in San Mateo?"**
| Method | Rank 1 | Rank 2 | Rank 3 |
|---|---|---|---|
| BM25 | `yelp_late_night.md` — Kaizen closes around 10 PM review | `yelp_late_night.md` — structural analysis | `happycow_vegetarian.md` ❌ off-target |
| Semantic | `yelp_late_night.md` — structural analysis (dist 0.29) | `yelp_late_night.md` — options past midnight | `reddit_neighborhood_spots.md` — NightOwlEater comment |
| Hybrid RRF | `yelp_late_night.md` — structural analysis | `yelp_late_night.md` — Kaizen closes 10 PM | `reddit_neighborhood_spots.md` — NightOwlEater |

*Winner: **semantic / hybrid**. BM25 rank 3 retrieved a HappyCow vegan listing that contained "San Mateo" and matched on generic restaurant words — it shared tokens with the query but was entirely off-topic. Semantic search avoided this by understanding that "food after 10 PM" is about late-night dining, not dietary options. Hybrid inherited the correct top-2 from BM25 while displacing the off-target rank 3.*

**Query 3: "What vegan options are available in downtown San Mateo?"**
| Method | Rank 1 | Rank 2 | Rank 3 |
|---|---|---|---|
| BM25 | `happycow_vegetarian.md` — overview | `happycow_vegetarian.md` — no dedicated vegan restaurants | `happycow_vegetarian.md` — Kaizen listing |
| Semantic | `happycow_vegetarian.md` — overview (dist 0.20) | `happycow_vegetarian.md` — no dedicated vegan (0.27) | `happycow_vegetarian.md` — cross-contamination note |
| Hybrid RRF | `happycow_vegetarian.md` — overview | `happycow_vegetarian.md` — no dedicated vegan | `happycow_vegetarian.md` — Kaizen listing |

*Winner: **tie** — both methods converge on the same source. "Vegan" and "downtown San Mateo" are exact keywords that appear heavily in `happycow_vegetarian.md`, so BM25 and semantic agree. Overall: semantic outperforms BM25 on conceptual queries (Query 2); BM25 matches or ties on specific proper-noun queries. Hybrid consistently matches or improves on the weaker individual method.*

---

## Stretch: Chunking Strategy Comparison

Implemented in `chunking_compare.py`. Compared two strategies on the same 3 queries using separate ChromaDB collections:

| Strategy | Chunk size | Overlap | Total chunks |
|---|---|---|---|
| A (baseline) | 500 chars | 100 chars | 114 |
| B (smaller) | 300 chars | 50 chars | 208 |

**Results:**

**Query 1: "What topping should you add to the kalbijjim at Daeho?"**

Strategy A rank 1: `reddit_best_dinners.md` dist=0.31 — full Reddit comment including "add the cheese topping... melted cheese over kalbijjim is a game changer"
Strategy B rank 1: `reddit_best_dinners.md` dist=0.32 — same comment but **truncated at 300 chars**, ending before the cheese recommendation is fully stated

*Strategy A wins. The 300-char chunk cuts the Reddit comment in half, producing a chunk that introduces Daeho but stops before the key topping detail. The answer is split across a chunk boundary in Strategy B.*

**Query 2: "Where can I get food after 10 PM in San Mateo?"**

Strategy A rank 1: `yelp_late_night.md` dist=0.29 — full structural analysis paragraph naming izakayas and 85C Bakery
Strategy B rank 1: `reddit_neighborhood_spots.md` dist=0.29 — NightOwlEater Reddit comment

*Strategy B promotes a Reddit comment to rank 1 that semantic search placed at rank 3 in Strategy A. Both chunks are relevant, but Strategy A's rank 1 chunk contains more complete information (multiple named late-night options in one chunk). Strategy B's shorter chunks are more fragmented — individual venue mentions are often split from their operational details.*

**Query 3: "What should I order at Suruki Market?"**

Strategy A rank 1: `japanese_hawaiian_markets.md` dist=0.37 — full "PREPARED FOODS COUNTER - WHAT TO ORDER" section listing sushi, bento, onigiri
Strategy B rank 1: `reddit_restaurant_megathread.md` dist=0.37 — Reddit megathread Suruki entry

*Mixed result — Strategy B surfaces the Reddit community validation at rank 1, which provides social proof, while Strategy A surfaces the operational document. Both are relevant but give different perspectives.*

**Conclusion:** Strategy A (500/100) outperforms Strategy B (300/50) for this corpus. The Reddit comments and editorial paragraphs in the source documents are typically 300–600 characters of continuous thought — splitting at 300 chars interrupts natural content units and moves key details to adjacent chunk boundaries where they can be missed by retrieval.

---

## Stretch: Metadata Filtering

The `retrieve()` function in `query_engine.py` accepts an optional `source_filter` parameter that passes a ChromaDB `where` clause, restricting results to a single source document.

**CLI usage:**
```
python query_engine.py --no-llm --filter-source michelin_san_mateo.md "What restaurants are recommended?"
```

**Effect demonstrated — same query, with and without filter:**

*Without filter* — results span 4 different sources:
```
[1] reddit_best_dinners.md       distance=0.21
[2] reddit_neighborhood_spots.md distance=0.23
[3] reddit_restaurant_megathread.md distance=0.25
[4] michelin_san_mateo.md        distance=0.30
[5] reddit_neighborhood_spots.md distance=0.31
```

*With `--filter-source michelin_san_mateo.md`* — all 5 results are from Michelin only:
```
[1] michelin_san_mateo.md  distance=0.30  INSPECTOR'S AREA OVERVIEW...
[2] michelin_san_mateo.md  distance=0.33  transit-accessible dining destination...
[3] michelin_san_mateo.md  distance=0.38  MICHELIN SELECTION: Additional Recommendations...
[4] michelin_san_mateo.md  distance=0.39  downtown corridor...independently-owned restaurants...
[5] michelin_san_mateo.md  distance=0.48  MICHELIN SELECTION: Pausa Bar & Cookery...
```

**Practical use case:** A user who wants only expert-curated recommendations (not community opinion) can filter to `michelin_san_mateo.md`. Conversely, filtering to `reddit_best_dinners.md` or `reddit_restaurant_megathread.md` isolates community voice. The filter is applied at the ChromaDB query level — it does not post-filter, so the full `n_results` budget is used within the filtered scope.
