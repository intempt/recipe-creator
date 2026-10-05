---
name: compound-funnel-activated-and-paying
description: |
  Use when a user mentions "compound funnel — activated and paying", or asks for related help. PLG funnel where success = activated AND paying, separating real activation from vanity activation.
arguments: []
intempt:
  id: compound-funnel-activated-and-paying
  version: 1.0.0
  slashCommand: /compound-funnel-activated-and-paying
  group: Reports
  shortDescription: "Build a funnel report tracking users from signup and activation journey completion to habitual use and paid subscription."
  availability: coming-soon
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
        Create a Funnel report called "Activated AND Paying".

        Steps:
        1. Event "user_created" — "Signed Up"
        2. Event "goal_completed_in_journey" where journey_id matches the activation journey — "Activated" (uses core feature)
        3. Event "goal_completed_in_journey" with frequency: 3+ occurrences within the same 7-day window for the same user — "Habitual Use"
        4. Compound condition: Step 3 reached AND a subscription_created event exists for the same customer_id where trial_end is null (real paid subscription, not trial) — "Activated AND Paying"

        Conversion window: 30 days
        Breakdown: By Users.utm_source
        Compare: Previous period (prior 30 days)

        For each step, also surface:
        - Median time-to-convert from previous step
        - Per-source conversion rate at each stage

        Annotations:
        - Compare the conversion rate at Step 4 vs. each individual condition alone (Activated alone, Paying alone). The gap reveals how much "activated but free" and "paying but inactive" exist as failure modes.
        - Flag any source where Step 2 → Step 4 is below 25% (activated users not converting to paid — pricing or value-perception issue).
        - Flag any source where Step 4 / Step 1 is below 5% (overall channel-quality issue).
        - Highlight sources where Step 4 conversion exceeds 15%.

        The activation-paywall conversion gap (Activated alone vs. Activated AND Paying) is the difference between vanity activation and real activation.

        Taxonomy notes:
        - "Habituated Use" and "Activated AND Paying" require Lovable to compute compound conditions from event sequences. The canonical events are all real (goal_completed_in_journey, subscription_created); the compounds are derived.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Compound Funnel — Activated AND Paying

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Activated AND Paying".

   Steps:
   1. Event "user_created" — "Signed Up"
   2. Event "goal_completed_in_journey" where journey_id matches the activation journey — "Activated" (uses core feature)
   3. Event "goal_completed_in_journey" with frequency: 3+ occurrences within the same 7-day window for the same user — "Habitual Use"
   4. Compound condition: Step 3 reached AND a subscription_created event exists for the same customer_id where trial_end is null (real paid subscription, not trial) — "Activated AND Paying"

   Conversion window: 30 days
   Breakdown: By Users.utm_source
   Compare: Previous period (prior 30 days)

   For each step, also surface:
   - Median time-to-convert from previous step
   - Per-source conversion rate at each stage

   Annotations:
   - Compare the conversion rate at Step 4 vs. each individual condition alone (Activated alone, Paying alone). The gap reveals how much "activated but free" and "paying but inactive" exist as failure modes.
   - Flag any source where Step 2 → Step 4 is below 25% (activated users not converting to paid — pricing or value-perception issue).
   - Flag any source where Step 4 / Step 1 is below 5% (overall channel-quality issue).
   - Highlight sources where Step 4 conversion exceeds 15%.

   The activation-paywall conversion gap (Activated alone vs. Activated AND Paying) is the difference between vanity activation and real activation.

   Taxonomy notes:
   - "Habituated Use" and "Activated AND Paying" require Lovable to compute compound conditions from event sequences. The canonical events are all real (goal_completed_in_journey, subscription_created); the compounds are derived.
   ```
