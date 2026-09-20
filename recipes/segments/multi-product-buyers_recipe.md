---
name: multi-product-buyers
description: |
  Use when a user mentions "multi-product buyers", or asks for related help. Customers who have purchased across multiple distinct products — cross-sell-ready cohort.
arguments: []
intempt:
  id: multi-product-buyers
  version: 1.0.0
  slashCommand: /multi-product-buyers
  group: Segments
  shortDescription: 'Customers who have purchased across multiple distinct products: cross-sell-ready cohort.'
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
        Create a segment called "Multi-Product Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 2 times in last 180 days
        - AND Attribute: lifetime_value >= 200

        Description: Customers with multiple orders and meaningful spend. Cross-sell-ready cohort — broader product affinity than single-category buyers.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Multi-Product Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Multi-Product Buyers".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created occurred >= 2 times in last 180 days
   - AND Attribute: lifetime_value >= 200

   Description: Customers with multiple orders and meaningful spend. Cross-sell-ready cohort — broader product affinity than single-category buyers.
   ```

## Taxonomy notes

- order_created is canonical.
- lifetime_value is canonical Users numeric attribute.
- For true distinct-product-count filtering, the workspace would need a custom attribute distinct_products_purchased populated by an aggregation job — V2.1 segment rules don't natively count distinct values within a property of an event. This recipe approximates with order count + LTV, which captures the practical signal without requiring custom attribution.
- Tune the lifetime_value threshold to your AOV — for stores with $50 AOV, $200 ≈ 4 orders; for stores with $200 AOV, raise to $500+.
