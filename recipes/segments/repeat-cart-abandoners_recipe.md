---
name: repeat-cart-abandoners
description: |
  Use when a user mentions "repeat cart abandoners", or asks for related help. Users who have abandoned checkout 2+ times in the last 30 days without purchasing.
arguments: []
intempt:
  id: repeat-cart-abandoners
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a user segment identifying visitors who abandoned checkout at least twice in the past 30 days without completing an order."
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
        Create a segment called "Repeat Cart Abandoners".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: abandoned_checkout occurred >= 2 times in last 30 days
        - AND Event: order_created occurred 0 times in last 30 days

        Description: Users who repeatedly abandon checkout — likely friction or price sensitivity. Trigger differentiated recovery offers (different from first-time abandoners).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Repeat Cart Abandoners

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Repeat Cart Abandoners".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: abandoned_checkout occurred >= 2 times in last 30 days
   - AND Event: order_created occurred 0 times in last 30 days

   Description: Users who repeatedly abandon checkout — likely friction or price sensitivity. Trigger differentiated recovery offers (different from first-time abandoners).
   ```

## Taxonomy notes

- abandoned_checkout is canonical V2.1 event with properties abandoned_at, checkout_id, email, items, masterID, recovery_url.
- order_created is canonical.
- For broader cart abandonment (carts that never reached checkout), use cart_abandoned (also canonical) instead. abandoned_checkout fires only when checkout was started; cart_abandoned fires when items were added but not converted.
