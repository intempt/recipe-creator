---
name: discount-only-buyers
description: |
  Use when a user mentions "discount-only buyers", or asks for related help. Customers who only purchase when a discount is applied — suppression cohort for full-price campaigns.
arguments: []
intempt:
  id: discount-only-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Customers who only purchase when a discount is applied — suppression cohort for full-price campaigns."
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
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
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
        Create a segment called "Discount-Only Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created where discount_codes is not empty occurred >= 2 times (all time)
        - AND Event: order_created where discount_codes is empty occurred 0 times (all time)

        Description: Customers whose every order has a discount code applied. Margin-protective suppression cohort — exclude from full-price campaigns and reserve for sale-only outreach. Pricing them at full price typically results in zero conversion; the bargain-hunting behavior is the buying signal.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Discount-Only Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Discount-Only Buyers".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created where discount_codes is not empty occurred >= 2 times (all time)
   - AND Event: order_created where discount_codes is empty occurred 0 times (all time)

   Description: Customers whose every order has a discount code applied. Margin-protective suppression cohort — exclude from full-price campaigns and reserve for sale-only outreach. Pricing them at full price typically results in zero conversion; the bargain-hunting behavior is the buying signal.
   ```

## Taxonomy notes

- order_created is canonical V2.1 event with discount_codes property (array of applied discount codes).
- The "discount_codes is not empty" filter requires that the array contains at least one code; "is empty" means no codes were applied.
- This is a SUPPRESSION segment — its job is to be excluded from full-price campaigns, not directly targeted. Pair with: "exclude from welcome flow > 10% off"; "suppress from new-arrival full-price launches"; "include in seasonal-sale and clearance campaigns only."
- Counter-pattern segment: "Full-Price Buyers" (order_created where discount_codes is empty >= 2 times) — these are your healthiest-margin customers and should be protected from over-discounting. Build that segment by inverting this one.
- This segment requires the merchant's checkout to populate discount_codes consistently. Stripe-native discounts populate this; some custom discount logic may not. Verify a sample order_created event before relying on this segment.
