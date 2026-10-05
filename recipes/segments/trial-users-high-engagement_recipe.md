---
name: trial-users-high-engagement
description: |
  Use when a user mentions "trial users — high engagement", or asks for related help. Trial users with strong usage signals who are likely to convert. Engagement bucketed enum.
arguments: []
intempt:
  id: trial-users-high-engagement
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Creates the /segments segment 'Trial Users — High Engagement' for trial-plan users with end_date within 14 days, engagement_score High, and at least 3 goal_completed_in_journey events in the last 14 days."
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
        Create a segment called "Trial Users — High Engagement".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: plan_name = "trial"
        - AND Attribute: end_date is within next 14 days
        - AND Attribute: engagement_score = "High"
        - AND Event: goal_completed_in_journey occurred >= 3 times in last 14 days

        Description: Trial users with strong usage signals — most likely to convert. Trigger high-touch sales outreach or premium-feature unlock.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Trial Users — High Engagement

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Trial Users — High Engagement".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: plan_name = "trial"
   - AND Attribute: end_date is within next 14 days
   - AND Attribute: engagement_score = "High"
   - AND Event: goal_completed_in_journey occurred >= 3 times in last 14 days

   Description: Trial users with strong usage signals — most likely to convert. Trigger high-touch sales outreach or premium-feature unlock.
   ```

## Taxonomy notes

- plan_name and end_date are canonical Users attributes.
- engagement_score uses the canonical enum Low | Medium | High (per platform scoring rules — no numeric thresholds on score attributes). Source template used numeric ">= 60" which violates the scoring constraint.
- goal_completed_in_journey is canonical.
- For more precision, the goal_completed_in_journey rule can be filtered to a specific journey_id.
