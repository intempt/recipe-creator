---
name: winnable-churned-users
description: |
  Use when a user mentions "winnable churned users", or asks for related help. Recently churned users who showed engagement before churn — best win-back candidates.
arguments: []
intempt:
  id: winnable-churned-users
  version: 1.0.0
  slashCommand: /winnable-churned-users
  group: Segments
  shortDescription: 'Recently churned users who showed engagement before churn: best win-back candidates.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
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
        Create a segment called "Winnable Churned Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: subscription_cancelled occurred >= 1 time in last 60 days
        - AND Attribute: lifetime_value > 0
        - AND Attribute: total_events >= 50

        Description: Recently churned users with prior engagement (positive lifetime value, meaningful event volume during their active period). Best candidates for a win-back offer.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Winnable Churned Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Winnable Churned Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: subscription_cancelled occurred >= 1 time in last 60 days
   - AND Attribute: lifetime_value > 0
   - AND Attribute: total_events >= 50

   Description: Recently churned users with prior engagement (positive lifetime value, meaningful event volume during their active period). Best candidates for a win-back offer.
   ```

## Taxonomy notes

- subscription_cancelled is canonical (note: British spelling per V2.1 taxonomy).
- lifetime_value > 0 confirms they had paid usage at some point.
- total_events >= 50 is the canonical proxy for "was previously engaged" (replaces source template's logically impossible "engagement_score WAS >= 50 before churn" — V2.1 segment rules evaluate CURRENT attribute values, never historical values).
- The 50-event threshold is a starting point; merchants typically tune based on the median total_events of their healthy paid cohort.
- For a more sophisticated win-back targeting, layer with a saved Power-Users-At-Time-Of-Cancellation segment (would require historical cohort tagging via user_tags_added at the time of cancellation, which is set up separately).
