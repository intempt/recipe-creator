---
name: recently-churned-users
description: |
  Use when a user mentions "recently churned users (30 days)", or asks for related help. Users who cancelled their subscription in the last 30 days — fast win-back cohort.
arguments: []
intempt:
  id: recently-churned-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a Users segment named 'Recently Churned Users' where subscription_cancelled occurred in the last 30 days and lifetime_value > 0."
  availability: available
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
        Create a segment called "Recently Churned Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: subscription_cancelled occurred >= 1 time in last 30 days
        - AND Attribute: lifetime_value > 0

        Description: Users who cancelled in the last 30 days with prior paid history. Fast win-back cohort — easier to recover than older churned users while feedback is still fresh.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Recently Churned Users (30 Days)

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Recently Churned Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: subscription_cancelled occurred >= 1 time in last 30 days
   - AND Attribute: lifetime_value > 0

   Description: Users who cancelled in the last 30 days with prior paid history. Fast win-back cohort — easier to recover than older churned users while feedback is still fresh.
   ```

## Taxonomy notes

- subscription_cancelled is canonical V2.1 event (British spelling).
- lifetime_value > 0 confirms they had paid status before churning (filters out canceled-trial-without-conversion edge cases).
- Distinct from "winnable-churned-users" (60-day window with engagement filter) — this is the broader, fresher cohort that responds best to immediate win-back outreach (within the first 30 days when memory is freshest).
