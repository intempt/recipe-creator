---
name: activation-funnel-with-velocity
description: |
  Use when a user mentions "activation funnel with time-to-convert per step", or asks for related help. Activation funnel with median + p75 step velocity — surfaces where users stall, not just where they drop.
arguments: []
intempt:
  id: activation-funnel-with-velocity
  version: 1.0.0
  slashCommand: /activation-funnel-with-velocity
  group: Reports
  shortDescription: 'Activation funnel with median + p75 step velocity: surfaces where users stall, not just where they drop.'
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
        Create a Funnel report called "Activation with Step Velocity".

        Steps:
        1. Event "user_created" — "Signed Up"
        2. Event "session_start" within 24h of user_created — "First Return"
        3. Event "goal_completed_in_journey" where journey_id matches the setup journey — "Completed Setup"
        4. Event "goal_completed_in_journey" where journey_id matches the core-feature journey — "Used Core Feature"
        5. Event "goal_completed_in_journey" where journey_id matches the activation journey, with frequency: occurred_at appears 3+ times in the 7 days following step 4 — "Activated (Habituated)"

        Conversion window: 14 days
        Breakdown: By Users.utm_source
        Compare: Previous period (prior 14 days)

        For each step, in addition to conversion rate, surface:
        - Median time-to-convert from previous step
        - 75th-percentile time-to-convert
        - Stall rate: % of users at this step who have NOT advanced after 24h, after 72h, after 7 days

        Annotations:
        - Add benchmarks: median signup → setup-complete ≤ 24 hours is the activation gold standard.
        - Flag any step where p75 time-to-convert exceeds 7 days (long tail of stalled users).
        - Flag any step where the stall-rate-at-72h is above 60%.
        - Highlight the step where reducing time-to-convert by 50% would have the biggest downstream activation lift.

        Velocity is the activation lever — drop-off tells you where users die, velocity tells you where they're stuck.

        Taxonomy notes:
        - "Habituated" Step 5 requires Lovable to compute the "3+ goal completions in 7 days" rule from goal_completed_in_journey timestamps grouped by user.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Activation Funnel with Time-to-Convert per Step

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Activation with Step Velocity".

   Steps:
   1. Event "user_created" — "Signed Up"
   2. Event "session_start" within 24h of user_created — "First Return"
   3. Event "goal_completed_in_journey" where journey_id matches the setup journey — "Completed Setup"
   4. Event "goal_completed_in_journey" where journey_id matches the core-feature journey — "Used Core Feature"
   5. Event "goal_completed_in_journey" where journey_id matches the activation journey, with frequency: occurred_at appears 3+ times in the 7 days following step 4 — "Activated (Habituated)"

   Conversion window: 14 days
   Breakdown: By Users.utm_source
   Compare: Previous period (prior 14 days)

   For each step, in addition to conversion rate, surface:
   - Median time-to-convert from previous step
   - 75th-percentile time-to-convert
   - Stall rate: % of users at this step who have NOT advanced after 24h, after 72h, after 7 days

   Annotations:
   - Add benchmarks: median signup → setup-complete ≤ 24 hours is the activation gold standard.
   - Flag any step where p75 time-to-convert exceeds 7 days (long tail of stalled users).
   - Flag any step where the stall-rate-at-72h is above 60%.
   - Highlight the step where reducing time-to-convert by 50% would have the biggest downstream activation lift.

   Velocity is the activation lever — drop-off tells you where users die, velocity tells you where they're stuck.

   Taxonomy notes:
   - "Habituated" Step 5 requires Lovable to compute the "3+ goal completions in 7 days" rule from goal_completed_in_journey timestamps grouped by user.
   ```
