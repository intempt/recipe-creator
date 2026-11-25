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
  - slot: product_margin_data
    kind: attribute
    meaning: Per-product profit margin values available in the product catalog
  steps:
  - id: s1
    builds: experiment
    uses:
    - control_weight_text
    - experiment_window
    - guardrail_max_drop
    - max_results
    - min_searches_per_variant
    - order_placed_event
    - product_margin_data
    - search_query_event
    - search_result_click_event
    - variant_b_weight_popularity
    - variant_b_weight_text
    - variant_c_weight_margin
    - variant_c_weight_text
    - variant_split
    instruction: 'Create a server experiment titled "Search Ranking Optimization" with flag key search_ranking_strategy, for
      users who do {search_query_event}. Split traffic {variant_split}. Control ranks by text relevance: text match weight
      {control_weight_text}, popularity and margin weight 0, ties broken alphabetically. Variant B ranks by popularity: text
      match weight {variant_b_weight_text}, popularity weight {variant_b_weight_popularity}, ties broken by popularity. Variant
      C ranks by margin: text match weight {variant_c_weight_text}, margin weight {variant_c_weight_margin} from {product_margin_data},
      ties broken by margin. Each variant returns at most {max_results} results. Primary metric: revenue per searching user,
      the sum of {order_placed_event.total_price} within 24 hours of a {search_query_event}. Secondary metric: search result
      click rate from {search_result_click_event}. Guardrail: search-to-purchase conversion must not drop by more than {guardrail_max_drop}%.
      Run for {experiment_window} and until each variant has {min_searches_per_variant} searches.'
---

# Search ranking test

Slash command: /search-results-ranking-test

## Step 1: Set up the ranking test

Create a server experiment titled "Search Ranking Optimization" with flag key search_ranking_strategy, for users who do search query event. Split traffic 34 / 33 / 33. Control ranks by text relevance: text match weight 1.0, popularity and margin weight 0, ties broken alphabetically. Variant B ranks by popularity: text match weight 0.6, popularity weight 0.4, ties broken by popularity. Variant C ranks by margin: text match weight 0.7, margin weight 0.3 from product margin data, ties broken by margin. Each variant returns at most 24 results. Primary metric: revenue per searching user, the sum of total price within 24 hours of a search query event. Secondary metric: search result click rate from search result click event. Guardrail: search-to-purchase conversion must not drop by more than 5%. Run for 21 d and until each variant has 5000 searches.
