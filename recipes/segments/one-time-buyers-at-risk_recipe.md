---
name: one-time-buyers-at-risk
description: |
  Use when a user mentions "one-time buyers at risk", or asks for related help. Customers who made one purchase but have not returned in 60+ days.
arguments: []
intempt:
  id: one-time-buyers-at-risk
  version: 1.0.0
  slashCommand: /one-time-buyers-at-risk
  group: Segments
  shortDescription: "Customers who made one purchase but have not returned in 60+ days."
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
        Create a segment called "One-Time Buyers At Risk".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: order_created occurred = 1 time (all time)
        - AND Attribute: days_since_last_activity >= 60
        - AND Attribute: lifecycle_score is not in ["Regulars", "Promising"]

        Description: Single-purchase customers who haven't returned in over 60 days and aren't on a healthy lifecycle trajectory. Re-engagement opportunity — second-purchase incentive recommended.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# One-Time Buyers At Risk

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "One-Time Buyers At Risk".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: order_created occurred = 1 time (all time)
   - AND Attribute: days_since_last_activity >= 60
   - AND Attribute: lifecycle_score is not in ["Regulars", "Promising"]

   Description: Single-purchase customers who haven't returned in over 60 days and aren't on a healthy lifecycle trajectory. Re-engagement opportunity — second-purchase incentive recommended.
   ```

## Taxonomy notes

- order_created is canonical.
- days_since_last_activity is canonical Users attribute (numeric, no scoring constraint applies).
- lifecycle_score uses the canonical 6-stage enum: At risk, Needs attention, New customers, Promising, Regulars, Champions. "Regulars" and "Promising" are valid canonical values.
