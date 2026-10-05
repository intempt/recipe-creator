---
name: newly-activated-users
description: |
  Use when a user mentions "newly activated users", or asks for related help. Users who completed activation in the last 7 days — warm and ready to expand.
arguments: []
intempt:
  id: newly-activated-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a Users segment 'Newly Activated Users' where goal_completed_in_journey fired ≥1× in 7 days AND plan_name is not 'free'."
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
        Create a segment called "Newly Activated Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: goal_completed_in_journey where journey_id = <activation journey id> occurred >= 1 time in last 7 days
        - AND Attribute: plan_name is not "free"

        Description: Users who hit the activation milestone in the last 7 days. Warm cohort for expansion outreach, feature-discovery campaigns, and upgrade prompts.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Newly Activated Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Newly Activated Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: goal_completed_in_journey where journey_id = <activation journey id> occurred >= 1 time in last 7 days
   - AND Attribute: plan_name is not "free"

   Description: Users who hit the activation milestone in the last 7 days. Warm cohort for expansion outreach, feature-discovery campaigns, and upgrade prompts.
   ```

## Taxonomy notes

- goal_completed_in_journey is canonical with required properties journey_id, occurred_at, user_id.
- The journey_id MUST be specified — replace <activation journey id> with the actual id of the merchant's activation journey. The recipe is parameterized at this point because each workspace's activation milestone is defined in its own activation journey.
- plan_name is canonical (replaces "plan").
