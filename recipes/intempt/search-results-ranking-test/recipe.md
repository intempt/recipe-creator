---
frontmatter_id: search-results-ranking-test
slash_command: /search-results-ranking-test
description: Compares ranking search results by text relevance, by sales velocity, or by profit margin, scored on revenue after a search.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - marketplaces
portable:
  summary: Tests three search ranking strategies (text relevance, sales popularity, profit margin) and reports which one drives
    the most revenue after a search.
  parameters:
  - name: experiment_window
    type: duration
    label: Experiment run length
    default: 21 d
    required: false
  - name: min_searches_per_variant
    type: number
    label: Minimum searches per variant
    default: 5000
    required: false
  - name: control_weight_text
    type: number
    label: 'Control: text match weight'
    default: 1.0
    required: false
  - name: variant_b_weight_text
    type: number
    label: 'Variant B: text match weight'
    default: 0.6
    required: false
  - name: variant_b_weight_popularity
    type: number
    label: 'Variant B: popularity weight'
    default: 0.4
    required: false
  - name: variant_c_weight_text
    type: number
    label: 'Variant C: text match weight'
    default: 0.7
    required: false
  - name: variant_c_weight_margin
    type: number
    label: 'Variant C: margin weight'
    default: 0.3
    required: false
  - name: max_results
    type: number
    label: Maximum search results shown
    default: 24
    required: false
  - name: guardrail_max_drop
    type: number
    label: Maximum allowed search-to-purchase conversion drop (%)
    default: 5
    required: false
  - name: variant_split
    type: text
    label: Traffic split across Control, Variant B, Variant C (percent)
    default: 34 / 33 / 33
    required: false
  requirements:
  - slot: search_ranking_experiment
    kind: integration
    meaning: A server-side experiment platform that serves a feature flag per user and tracks goal conversions per experience
    channel: email
  - slot: search_query_event
    kind: event
    meaning: A customer ran a product search
    properties:
    - name: query
      type: text
      meaning: The search text entered by the customer
      optional: false
  - slot: search_result_click_event
    kind: event
    meaning: A customer clicked a product in search results
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked result, such as search-result-3 for position 3
      optional: false
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total price of the placed order
      optional: false
  - slot: search_to_purchase_metric
    kind: segment
    meaning: An existing aggregate metric of search-to-purchase conversion used as a guardrail
  - slot: product_margin_data
    kind: attribute
    meaning: Per-product profit margin values available in the product catalog
  - slot: search_backend
    kind: integration
    meaning: The application search service that ranks results using text relevance, sales velocity and margin weights
    channel: email
  steps:
  - id: s1
    builds: experiment
    uses:
    - search_ranking_experiment
    - search_backend
    - search_query_event
    - control_weight_text
    - variant_b_weight_text
    - variant_b_weight_popularity
    - variant_c_weight_text
    - variant_c_weight_margin
    - max_results
    - variant_split
    instruction: 'Create a server experiment titled "Search Ranking Optimization" with flag key search_ranking_strategy. Serve
      three variants: Control (34%) uses relevance-based ranking with text match weight {control_weight_text}, popularity
      weight 0 and margin weight 0; Variant B (33%) uses popularity-weighted ranking with text match weight {variant_b_weight_text}
      and popularity weight {variant_b_weight_popularity}; Variant C (33%) uses margin-weighted ranking with text match weight
      {variant_c_weight_text} and margin weight {variant_c_weight_margin}. Split traffic {variant_split}. Each variant returns
      max results {max_results}, and tie breakers are alphabetical for Control, popularity for Variant B and margin for Variant
      C.'
---

# Search ranking test

Slash command: /search-results-ranking-test

## Step 1: Set up the ranking test

Create a SERVER EXPERIMENT on /experiences titled "Search Ranking Optimization".
═══ PATH 1: Top-level configuration ═══
Experience type: server_experiment
Flag Key: search_ranking_strategy
Variants:
- Control (34%): relevance-based (text match score only)
- Variant B (33%): popularity-weighted (relevance × sales velocity)
- Variant C (33%): margin-weighted (relevance × profit margin)
Targeting:
- Pages: any page where the search backend is called: typically search results pages (page URL contains "/search") and inline search-as-you-type widgets in the header
- Devices: any (server-side search is device-agnostic; the ranking algorithm runs in the search backend regardless of client device)
- Audience: users performing product searches (search query string is non-empty, OR Submit on the search form)
- Display frequency: always (every search query call invokes getFlag and applies the assigned variant's ranking)
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Placed order within session of a search)
Secondary metrics:
- Click on on search results (search-to-click conversion)
- Average click position (which rank (1, 2, 3) got clicked)
- Revenue per search (sum of Placed order.total_price / count of distinct searches)
- Zero-result rate (searches where no Click on followed within 30 seconds)
Guardrail: search-to-purchase conversion (the existing aggregate metric) must not drop >5% in any variant. Note: variant C (margin-weighted) is a known accuracy/profit tradeoff: guardrails catch it if the accuracy drop is too steep.
Schedule: 21 days, 5,000 searches per variant minimum
═══ PATH 2: Variant JSON payload ═══
Variant: Control (relevance)
 {
 "ranking_strategy": "relevance",
 "weights": {
 "text_match_score": 1.0,
 "popularity": 0.0,
 "margin": 0.0
 },
 "max_results": 24,
 "tie_breaker": "alphabetical"
 }
Variant: B (popularity-weighted)
 {
 "ranking_strategy": "popularity_weighted",
 "weights": {
 "text_match_score": 0.6,
 "popularity": 0.4,
 "margin": 0.0
 },
 "max_results": 24,
 "tie_breaker": "popularity"
 }
Variant: C (margin-weighted)
 {
 "ranking_strategy": "margin_weighted",
 "weights": {
 "text_match_score": 0.7,
 "popularity": 0.0,
 "margin": 0.3
 },
 "max_results": 24,
 "tie_breaker": "margin"
 }
SDK integration:
 const ranking = await intempt.getFlag('search_ranking_strategy', userId);
 const results = await search.query(query, { weights: ranking.weights, max: ranking.max_results });
Each rendered search result should have target_id = "search-result-{position}" so Click on per-position metrics roll up consistently.
Taxonomy notes:
- The search backend (search.query) is application-side and not part of canonical taxonomy.
- "Click position" is the rank of the clicked result: typically captured as target_id ("search-result-3" to position 3) or as a property on Click on.
- "Margin" data is required for variant C; if your product catalog doesn't track per-product margin, variant C cannot run faithfully.
- "Display frequency: always": every search query for a given userId returns the same variant (sticky assignment) for the experiment's duration. The variant is computed once on first search and cached.
