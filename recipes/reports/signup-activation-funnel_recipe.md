---
name: signup-activation-funnel
description: |
  Use when a user mentions "signup → activation funnel", or asks for related help. Signup-to-activation funnel using user_created and goal_completed_in_journey with per-step time-to-convert.
arguments: []
intempt:
  id: signup-activation-funnel
  version: 1.0.0
  slashCommand: /signup-activation-funnel
  group: Reports
  shortDescription: "Signup-to-activation funnel using user_created and goal_completed_in_journey with per-step time-to-convert."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Signup to Activation".

        Steps:
        1. Event "user_created" — "Signed Up"
        2. Event "session_start" within 24 hours of user_created — "Returned After Signup" (proxy for engagement after creation)
        3. Event "goal_completed_in_journey" where journey_id matches the onboarding/activation journey — "Used Core Feature"
        4. Event "goal_completed_in_journey" where journey_id matches the activation journey AND occurred_at - signup_at <= 14 days — "Activated"

        Conversion window: 14 days
        Breakdown: By Users.utm_source (signup source — top 6 channels: organic, paid_search, paid_social, content, referral, direct)
        Compare: Previous period (prior 14 days)

        For each step, also surface:
        - Median and 75th-percentile time-to-convert from previous step
        - Per-source conversion rate at each stage

        Annotations:
        - Add benchmark: activation rate (Step 4 / Step 1) of 30% is typical PLG SaaS.
        - Flag any source with activation rate <15% (poor lead quality or onboarding mismatch).
        - Flag any step where median time-to-convert exceeds 24 hours for "Returned After Signup" or 7 days for "Used Core Feature".
        - Highlight sources with activation rate >40%.

        Identify which signup source produces the highest-activating users at sufficient volume.

        Taxonomy notes:
        - user_created and goal_completed_in_journey are canonical. goal_completed_in_journey carries journey_id, occurred_at, user_id.
        - "signup_completed", "onboarding_started" as standalone events do not exist; the activation journey itself emits goal_completed_in_journey when the user hits the activation goal.
        - Users.utm_source is the canonical first-touch source attribute.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Signup → Activation Funnel

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Signup to Activation".

   Steps:
   1. Event "user_created" — "Signed Up"
   2. Event "session_start" within 24 hours of user_created — "Returned After Signup" (proxy for engagement after creation)
   3. Event "goal_completed_in_journey" where journey_id matches the onboarding/activation journey — "Used Core Feature"
   4. Event "goal_completed_in_journey" where journey_id matches the activation journey AND occurred_at - signup_at <= 14 days — "Activated"

   Conversion window: 14 days
   Breakdown: By Users.utm_source (signup source — top 6 channels: organic, paid_search, paid_social, content, referral, direct)
   Compare: Previous period (prior 14 days)

   For each step, also surface:
   - Median and 75th-percentile time-to-convert from previous step
   - Per-source conversion rate at each stage

   Annotations:
   - Add benchmark: activation rate (Step 4 / Step 1) of 30% is typical PLG SaaS.
   - Flag any source with activation rate <15% (poor lead quality or onboarding mismatch).
   - Flag any step where median time-to-convert exceeds 24 hours for "Returned After Signup" or 7 days for "Used Core Feature".
   - Highlight sources with activation rate >40%.

   Identify which signup source produces the highest-activating users at sufficient volume.

   Taxonomy notes:
   - user_created and goal_completed_in_journey are canonical. goal_completed_in_journey carries journey_id, occurred_at, user_id.
   - "signup_completed", "onboarding_started" as standalone events do not exist; the activation journey itself emits goal_completed_in_journey when the user hits the activation goal.
   - Users.utm_source is the canonical first-touch source attribute.
   ```
