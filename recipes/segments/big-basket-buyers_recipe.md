---
name: big-basket-buyers
description: |
  Use when a user mentions "big-basket buyers", or asks for related help. Customers with high average order value — premium-bundle and upsell-targeting cohort.
arguments: []
intempt:
  id: big-basket-buyers
  version: 1.0.0
  slashCommand: /big-basket-buyers
  group: Segments
  shortDescription: 'Customers with high average order value: premium-bundle and upsell-targeting cohort.'
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
        Create a segment called "Big-Basket Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: avg_order_value >= 150
        - AND Event: order_created occurred >= 2 times (all time)
        - AND Attribute: lifetime_value >= 300

        Description: Customers who buy at higher AOV per order. Distinct from VIPs (which is by lifetime spend). Big-basket buyers may have fewer orders but consistently spend big on each — the right cohort for premium product launches, bundle offers, and "spend more, save more" tier promotions.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Big-Basket Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Big-Basket Buyers".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: avg_order_value >= 150
   - AND Event: order_created occurred >= 2 times (all time)
   - AND Attribute: lifetime_value >= 300

   Description: Customers who buy at higher AOV per order. Distinct from VIPs (which is by lifetime spend). Big-basket buyers may have fewer orders but consistently spend big on each — the right cohort for premium product launches, bundle offers, and "spend more, save more" tier promotions.
   ```

## Taxonomy notes

- avg_order_value, lifetime_value are canonical Users numeric attributes.
- order_created is canonical event.
- The composite (avg_order_value >= 150 AND >= 2 orders AND lifetime_value >= 300) prevents single-order outliers from inflating the segment — a customer who placed one $200 order isn't a "big-basket buyer," they're a one-off.
- Tune avg_order_value threshold to ~1.5x your typical AOV. For stores with $80 typical AOV, use $120; for stores with $200 typical AOV, use $300.
- Distinct from vip-customers-high-ltv (which is cumulative spend, may be many small orders) — big-basket-buyers is per-order intensity. The two cohorts overlap but capture different shopping patterns.
