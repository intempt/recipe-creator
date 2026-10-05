---
name: replenishment-ready
description: |
  Use when a user mentions "replenishment-ready customers", or asks for related help. Customers approaching their typical re-order cycle. 8-15% conversion on replenishment reminders vs 1-3% on general promos.
arguments: []
intempt:
  id: replenishment-ready
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Creates a Users segment named 'Replenishment-Ready' for users with order_created 30-60 days ago and no order_created in the last 30 days."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [ecommerce]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: "Configure Segment Rule"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Open the segment authoring surface, name the segment, and apply the rule below."
      prompt: |
        Create a segment called "Replenishment-Ready".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 1 time (all time)
        - AND Event: order_created occurred 0 times in last 30 days
        - AND Event: order_created occurred >= 1 time between 30 and 60 days ago

        Description: Customers whose last purchase was 30-60 days ago and who are due for re-purchase based on typical consumption cycles. Trigger replenishment reminder ("Running low?") timed to product depletion. Replenishment messaging consistently outperforms generic promotion by 5-10x.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Replenishment-Ready Customers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Replenishment-Ready".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created occurred >= 1 time (all time)
   - AND Event: order_created occurred 0 times in last 30 days
   - AND Event: order_created occurred >= 1 time between 30 and 60 days ago

   Description: Customers whose last purchase was 30-60 days ago and who are due for re-purchase based on typical consumption cycles. Trigger replenishment reminder ("Running low?") timed to product depletion. Replenishment messaging consistently outperforms generic promotion by 5-10x.
   ```

## Taxonomy notes

- order_created is canonical V2.1 event.
- The 30-60 day window is a STARTER for typical consumables; merchants should tune per category:
    - Coffee, supplements, FMCG: last order 21-35 days ago
    - Skincare: last order 45-75 days ago
    - Cosmetics, makeup: last order 60-90 days ago
    - Pet food, household supplies: last order 30-45 days ago
    - Vitamins: last order 25-35 days ago
- The rule structure (last 30 days = 0 orders AND 30-60 days ago = 1+ orders) finds the "due for refill" sweet spot — recent enough to remember, old enough to be running out.
- Distinct from one-time-buyers-at-risk (60+ days, broader lapsed signal) and at-risk-vips (recency decay among proven high-value). Replenishment-ready is the SCHEDULED-NEED cohort.
- For more precision, the rule can be tightened to specific product_id filters via order_created.items.product_id (e.g., only target users who bought a specific consumable SKU). That product-specific variant is a refinement merchants build on top of this base recipe.
