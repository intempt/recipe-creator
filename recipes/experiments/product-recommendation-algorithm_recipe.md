---
name: product-recommendation-algorithm
description: |
  Use when a user mentions "product recommendation algorithm test", or asks for related help. Test which recommendation engine drives more cross-sell revenue: collaborative filtering vs. session-based vs. popularity. Server experiment with JSON payload.
arguments: []
intempt:
  id: product-recommendation-algorithm
  version: 1.0.1
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Test which recommendation engine drives more cross-sell revenue: collaborative filtering vs. session-based vs. popularity. Server experiment with JSON payload."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [experiment, server]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a SERVER EXPERIMENT on /experiences titled "Recommendation Algorithm Test".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: server_experiment

        Flag Key: recommendation_algorithm

        Variants:
        - Control (33%): collaborative filtering — "Customers also bought"
        - Variant B (33%): session-based — "Recently viewed by you"
        - Variant C (34%): popularity-based — "Trending now"

        Targeting:
        - Pages: any page that renders the recommendation block (typically PDPs and category pages — page URL contains "/products/" OR "/category/")
        - Devices: any (server experiments are device-agnostic; the recommendation API is called server-side regardless of client device)
        - Audience: visitors with >1 page_viewed in the current session (excludes one-and-done bouncers — recommendations are most useful for engaged shoppers)
        - Display frequency: always (every page render that includes the recommendation block calls getFlag and serves a variant)

        Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from order_created where the order's items include a clicked recommendation)
        Secondary metrics:
        - click_on where target_id starts with "rec-" (recommendation click-through rate)
        - order_created.total_price for orders following a recommendation click (revenue from recommended products)
        - Recommendation click position (which slot — 1, 2, 3, etc. — the user clicked)
        - Add-to-cart-from-rec rate: cart_created where the added product_id matches a recently-clicked recommendation

        Guardrail: PDP page_viewed → cart_created conversion rate must not drop >5% (avoid recommendations distracting from primary purchase decision)

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

        Each rendered recommendation should have target_id = "rec-{position}" (e.g., "rec-1", "rec-2") so click_on per-position aggregation works.

        Taxonomy notes:
        - The recommendation endpoints (/api/recs/*) are application-side and not part of the canonical taxonomy; this recipe assumes the merchant has these implemented.
        - Attributing order_created revenue to a recommendation requires the order to record which items came from a clicked recommendation — typically via session tracking joining click_on (target_id starts with "rec-") to subsequent order_created.items.
        - "Display frequency: always" for server experiments means every getFlag call returns the same variant for the same userId (sticky assignment); the variant is computed once and cached for that user for the experiment's duration.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Product Recommendation Algorithm Test

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a SERVER EXPERIMENT on /experiences titled "Recommendation Algorithm Test".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: server_experiment

   Flag Key: recommendation_algorithm

   Variants:
   - Control (33%): collaborative filtering — "Customers also bought"
   - Variant B (33%): session-based — "Recently viewed by you"
   - Variant C (34%): popularity-based — "Trending now"

   Targeting:
   - Pages: any page that renders the recommendation block (typically PDPs and category pages — page URL contains "/products/" OR "/category/")
   - Devices: any (server experiments are device-agnostic; the recommendation API is called server-side regardless of client device)
   - Audience: visitors with >1 page_viewed in the current session (excludes one-and-done bouncers — recommendations are most useful for engaged shoppers)
   - Display frequency: always (every page render that includes the recommendation block calls getFlag and serves a variant)

   Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from order_created where the order's items include a clicked recommendation)
   Secondary metrics:
   - click_on where target_id starts with "rec-" (recommendation click-through rate)
   - order_created.total_price for orders following a recommendation click (revenue from recommended products)
   - Recommendation click position (which slot — 1, 2, 3, etc. — the user clicked)
   - Add-to-cart-from-rec rate: cart_created where the added product_id matches a recently-clicked recommendation

   Guardrail: PDP page_viewed → cart_created conversion rate must not drop >5% (avoid recommendations distracting from primary purchase decision)

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

   Each rendered recommendation should have target_id = "rec-{position}" (e.g., "rec-1", "rec-2") so click_on per-position aggregation works.

   Taxonomy notes:
   - The recommendation endpoints (/api/recs/*) are application-side and not part of the canonical taxonomy; this recipe assumes the merchant has these implemented.
   - Attributing order_created revenue to a recommendation requires the order to record which items came from a clicked recommendation — typically via session tracking joining click_on (target_id starts with "rec-") to subsequent order_created.items.
   - "Display frequency: always" for server experiments means every getFlag call returns the same variant for the same userId (sticky assignment); the variant is computed once and cached for that user for the experiment's duration.
   ```
