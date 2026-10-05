---
name: onboarding-stalled-users
description: |
  Use when a user mentions "onboarding-stalled users", or asks for related help. Recently signed up but no activation milestone in last 14 days — activation-rescue cohort.
arguments: []
intempt:
  id: onboarding-stalled-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a Users segment named 'Onboarding-Stalled Users' for users first seen 7–30 days ago, no goal_completed_in_journey since first_seen_at, and days_since_last_activity ≤ 14."
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
        Create a segment called "Onboarding-Stalled Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: first_seen_at is between 7 and 30 days ago
        - AND Event: goal_completed_in_journey occurred 0 times since first_seen_at
        - AND Attribute: days_since_last_activity <= 14

        Description: Users who signed up 7-30 days ago, are still occasionally active, but have not completed any activation milestone. The activation-rescue cohort. Trigger guided onboarding outreach (in-app checklist, founder-style email, CSM check-in for high-value accounts).
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Onboarding-Stalled Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Onboarding-Stalled Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: first_seen_at is between 7 and 30 days ago
   - AND Event: goal_completed_in_journey occurred 0 times since first_seen_at
   - AND Attribute: days_since_last_activity <= 14

   Description: Users who signed up 7-30 days ago, are still occasionally active, but have not completed any activation milestone. The activation-rescue cohort. Trigger guided onboarding outreach (in-app checklist, founder-style email, CSM check-in for high-value accounts).
   ```

## Taxonomy notes

- first_seen_at, days_since_last_activity are canonical Users attributes.
- goal_completed_in_journey is canonical V2.1 event with required journey_id property — can optionally filter to a specific activation journey_id.
- The 7-30-day window excludes brand-new signups (still in their first week, given onboarding flows time to fire) AND excludes long-cold accounts that should be in dormant cohorts instead.
- The "still occasionally active" filter (days_since_last_activity <= 14) is the rescue signal — they're showing up but not progressing. Without this filter, the segment includes already-lapsed users who need a different intervention.
- Pendo-cited research: users completing 3 key actions in first 14 days show 65% lower churn — making this cohort the highest-leverage activation target.
