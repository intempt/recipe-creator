---
name: high-cart-value-abandoners
description: |
  Use when a user mentions "high-cart-value abandoners", or asks for related help. Cart abandoners with high cart value — priority recovery cohort distinct from frequency-based abandoners.
arguments: []
intempt:
  id: high-cart-value-abandoners
  version: 1.0.0
  slashCommand: /high-cart-value-abandoners
  group: Segments
  shortDescription: 'Cart abandoners with high cart value: priority recovery cohort distinct from frequency-based abandoners.'
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
        Create a segment called "High-Cart-Value Abandoners".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: cart_abandoned where total_amount >= 200 occurred >= 1 time in last 7 days
        - AND Event: order_created occurred 0 times in last 7 days

        Description: Cart abandoners whose abandoned cart value is high — priority recovery cohort. Worth more attention (and a potentially higher-effort intervention like a personal email or SMS) than low-cart-value abandoners. Distinct from repeat-cart-abandoners (which targets by frequency, not value).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# High-Cart-Value Abandoners

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "High-Cart-Value Abandoners".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: cart_abandoned where total_amount >= 200 occurred >= 1 time in last 7 days
   - AND Event: order_created occurred 0 times in last 7 days

   Description: Cart abandoners whose abandoned cart value is high — priority recovery cohort. Worth more attention (and a potentially higher-effort intervention like a personal email or SMS) than low-cart-value abandoners. Distinct from repeat-cart-abandoners (which targets by frequency, not value).
   ```

## Taxonomy notes

- cart_abandoned is canonical V2.1 event with property total_amount (currency).
- order_created is canonical.
- The $200 threshold is a STARTER; tune to your store's AOV — for stores with $80 AOV use $150, for stores with $500 AOV use $400-600. The principle is "carts notably above your typical AOV deserve more recovery effort."
- The 7-day window aligns with the standard cart_abandoned recovery flow timing.
- This segment is most valuable when paired with a higher-effort recovery intervention than the standard abandoned-cart email sequence — for example, a personal SMS, a call from a sales rep (for high-AOV stores), or a higher-tier discount than the default recovery flow uses.
- Merchants running a basic abandoned-cart email flow can use this segment to OVERRIDE the standard flow with a higher-touch intervention for the top 10-20% of carts by value.
