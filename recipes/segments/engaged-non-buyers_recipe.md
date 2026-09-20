---
name: engaged-non-buyers
description: |
  Use when a user mentions "engaged non-buyers", or asks for related help. Highly engaged visitors who have never made a purchase — first-purchase targeting cohort.
arguments: []
intempt:
  id: engaged-non-buyers
  version: 1.0.0
  slashCommand: /engaged-non-buyers
  group: Segments
  shortDescription: 'Highly engaged visitors who have never made a purchase: first-purchase targeting cohort.'
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
        Create a segment called "Engaged Non-Buyers".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: total_events >= 10
        - AND Event: order_created occurred 0 times (all time)
        - AND Attribute: days_since_last_activity <= 7
        - AND Attribute: email is not empty

        Description: Identified users who engage frequently but have never purchased. First-purchase incentive cohort — typically responds well to a first-order discount or product-discovery campaign.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Engaged Non-Buyers

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Engaged Non-Buyers".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: total_events >= 10
   - AND Event: order_created occurred 0 times (all time)
   - AND Attribute: days_since_last_activity <= 7
   - AND Attribute: email is not empty

   Description: Identified users who engage frequently but have never purchased. First-purchase incentive cohort — typically responds well to a first-order discount or product-discovery campaign.
   ```

## Taxonomy notes

- total_events, days_since_last_activity, email are canonical Users attributes.
- order_created is canonical.
- The "email is not empty" filter ensures the segment is reachable via email; for an ad-retargeting variant, drop that filter and pair with high-intent-anonymous-visitors.
