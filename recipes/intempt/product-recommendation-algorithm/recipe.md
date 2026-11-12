---
frontmatter_id: product-recommendation-algorithm
slash_command: /product-recommendation-algorithm
description: Compares three ways of picking recommended products (also bought, recently viewed, trending) on cross-sell revenue.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Runs a server-side test of three recommendation methods (also bought, recently viewed, trending) to find which
    drives the most cross-sell revenue.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Recommendation Algorithm Test
    required: false
  - name: flag_key
    type: string
    label: Feature flag key
    default: recommendation_algorithm
    required: false
  - name: control_weight
    type: number
    label: Control traffic share (%)
    default: 33
    required: false
  - name: variant_b_weight
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variant_c_weight
    type: number
    label: Variant C traffic share (%)
    default: 34
    required: false
  - name: min_page_views
    type: number
    label: Minimum page views in session before eligible
    default: 1
    required: false
  - name: max_items
    type: number
    label: Recommendations shown per block
    default: 4
    required: false
  - name: schedule_duration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: guardrail_max_drop_pct
    type: number
    label: Maximum allowed drop in PDP-to-cart conversion (%)
    default: 5
    required: false
  requirements:
  - slot: recommendation_click
    kind: event
    meaning: A customer clicked a recommended product in a recommendation block
    properties:
    - name: target_id
      type: string
      meaning: Recommendation slot identifier starting with 'rec-' followed by position
      optional: false
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Total order value
      optional: false
    - name: items
      type: text
      meaning: Products included in the order
      optional: false
  - slot: cart_created
    kind: event
    meaning: A customer created a cart containing a product
    properties:
    - name: product_id
      type: string
      meaning: Identifier of the product added to cart
      optional: false
  - slot: product_page_view
    kind: event
    meaning: A customer viewed a product detail page
  - slot: page_view
    kind: event
    meaning: A customer viewed a page on the site
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
  - slot: recommendation_experiment
    kind: integration
    meaning: An experimentation tool that assigns visitors to flag variants and tracks goal completions
    channel: email
  steps:
  - id: s1
    builds: experiment
    uses:
    - recommendation_experiment
    - recommendation_click
    - order_placed
    - cart_created
    - product_page_view
    - page_view
    - experiment_title
    - flag_key
    - control_weight
    - variant_b_weight
    - variant_c_weight
    - min_page_views
    - max_items
    - schedule_duration
    - guardrail_max_drop_pct
    instruction: 'Create a server-side experiment titled "{experiment_title}" with flag key {flag_key} and three variants:
      Control at {control_weight}% using collaborative filtering (endpoint /api/recs/collaborative, header "Customers also
      bought"), Variant B at {variant_b_weight}% using session-based recommendations (endpoint /api/recs/session, header "Recently
      viewed by you"), and Variant C at {variant_c_weight}% using popularity-based recommendations (endpoint /api/recs/trending,
      header "Trending now"). Each variant payload sets max_items to {max_items}; Control and Variant B fall back to popularity,
      Variant C has no fallback. Target pages whose URL contains "/products/" or "/category/" and that render the recommendation
      block. Target visitors with more than {min_page_views} page view in the current session. Serve on every page render
      (sticky per user). Run for {schedule_duration}. Primary metric: revenue from Placed order where the order items include
      a clicked recommendation (goal completed in experience with value above 0). Secondary metrics: recommendation click-through
      rate (clicks on target_id starting with "rec-"), revenue from orders following a recommendation click, click position
      by rec- slot, and add-to-cart rate for recently clicked recommended products. Guardrail: PDP view to cart created conversion
      must not drop more than {guardrail_max_drop_pct}%. Each rendered recommendation uses target_id "rec-position".'
---

# Recommendation algorithm test

Slash command: /product-recommendation-algorithm

## Step 1: Set up the algorithm test

Create a SERVER EXPERIMENT on /experiences titled "Recommendation Algorithm Test".
═══ PATH 1: Top-level configuration ═══
Experience type: server_experiment
Flag Key: recommendation_algorithm
Variants:
- Control (33%): collaborative filtering: "Customers also bought"
- Variant B (33%): session-based: "Recently viewed by you"
- Variant C (34%): popularity-based: "Trending now"
Targeting:
- Pages: any page that renders the recommendation block (typically PDPs and category pages: page URL contains "/products/" OR "/category/")
- Devices: any (server experiments are device-agnostic; the recommendation API is called server-side regardless of client device)
- Audience: visitors with >1 View page in the current session (excludes one-and-done bouncers: recommendations are most useful for engaged shoppers)
- Display frequency: always (every page render that includes the recommendation block calls getFlag and serves a variant)
Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from Placed order where the order's items include a clicked recommendation)
Secondary metrics:
- Click on where target_id starts with "rec-" (recommendation click-through rate)
- Placed order.total_price for orders following a recommendation click (revenue from recommended products)
- Recommendation click position (which slot (1, 2, 3, etc.) the user clicked)
- Add-to-cart-from-rec rate: Cart created where the added product_id matches a recently-clicked recommendation
Guardrail: PDP View page to Cart created conversion rate must not drop >5% (avoid recommendations distracting from primary purchase decision)
Schedule: 14 days
═══ PATH 2: Variant JSON payload ═══
Variant: Control (collaborative filtering)
 JSON payload:
 {
 "algorithm": "collaborative_filtering",
 "endpoint": "/api/recs/collaborative",
 "header_text": "Customers also bought",
 "max_items": 4,
 "fallback_algorithm": "popularity"
 }
Variant: B (session-based)
 {
 "algorithm": "session_based",
 "endpoint": "/api/recs/session",
 "header_text": "Recently viewed by you",
 "max_items": 4,
 "fallback_algorithm": "popularity"
 }
Variant: C (popularity-based)
 {
 "algorithm": "popularity",
 "endpoint": "/api/recs/trending",
 "header_text": "Trending now",
 "max_items": 4,
 "fallback_algorithm": null
 }
SDK integration:
 const recsConfig = await intempt.getFlag('recommendation_algorithm', userId);
 const recs = await fetch(recsConfig.endpoint + '?productId=' + currentProductId);
 // render recs.items in the PDP recommendation block, using recsConfig.header_text
Each rendered recommendation should have target_id = "rec-{position}" (e.g., "rec-1", "rec-2") so Click on per-position aggregation works.
Taxonomy notes:
- The recommendation endpoints (/api/recs/*) are application-side and not part of the canonical taxonomy; this recipe assumes the merchant has these implemented.
- Attributing Placed order revenue to a recommendation requires the order to record which items came from a clicked recommendation: typically via session tracking joining Click on (target_id starts with "rec-") to subsequent Placed order.items.
- "Display frequency: always" for server experiments means every getFlag call returns the same variant for the same userId (sticky assignment); the variant is computed once and cached for that user for the experiment's duration.
