---
name: repeat-buyers
description: |
  Use when a user mentions "repeat buyers", or asks for related help. Customers who have made 3+ purchases in the last 90 days with meaningful spend.
arguments: []
intempt:
  id: repeat-buyers
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Customers who have made 3+ purchases in the last 90 days with meaningful spend."
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
        Create a segment called "Repeat Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred >= 3 times in last 90 days
        - AND Attribute: lifetime_value >= 100

        Description: Repeat customers with meaningful spend. Priority for loyalty rewards, replenishment campaigns, and review requests.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Repeat Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Repeat Buyers".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created occurred >= 3 times in last 90 days
   - AND Attribute: lifetime_value >= 100

   Description: Repeat customers with meaningful spend. Priority for loyalty rewards, replenishment campaigns, and review requests.
   ```

## Taxonomy notes

- order_created is canonical.
- lifetime_value is canonical Users attribute (replaces source template's "total_order_value" which is not canonical).
- The $100 threshold is a starting point; merchants typically tune to their P50/P75 order value benchmark.
