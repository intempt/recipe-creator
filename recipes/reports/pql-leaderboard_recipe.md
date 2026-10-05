---
name: pql-leaderboard
description: |
  Use when a user mentions "pql leaderboard", or asks for related help. Sortable list of free users hitting configurable PQL thresholds — the canonical PLG sales-handoff report.
arguments: []
intempt:
  id: pql-leaderboard
  version: 1.0.0
  slashCommand: /pql-leaderboard
  group: Reports
  shortDescription: "A single Insights report listing free/trial users who hit configurable PQL event thresholds in a 14-day window, sorted by intent score."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "PQL Leaderboard".

        This recipe surfaces the highest-intent free users for sales follow-up — the Product Qualified Lead (PQL) leaderboard.

        PQL definition (configurable; default thresholds):
        A user qualifies as a PQL if ALL of the following are true within a 14-day rolling window:
          1. User is currently on a free or trial plan (subscription_created with trial_end populated, OR no active subscription_created)
          2. User has emitted ≥3 distinct sessions (≥3 session_start events on different days)
          3. User has emitted ≥1 goal_completed_in_journey for the activation journey
          4. User has emitted ≥10 click_on events on core feature targets (configurable target_id pattern)
        Optional ICP filter: user's Users.utm_source matches a high-fit channel (configurable)

        For each PQL, surface:
        - User identity (name, email, primary_account_id from Users object)
        - PQL score = a 0-100 number computed from a weighted blend of: session count × 5 + goal completions × 15 + core-feature clicks × 1 + days_since_first_seen as a recency multiplier (capped at the threshold)
        - Days as PQL (how long they've been over the threshold — long-tenured PQLs need urgent sales attention)
        - Most recent activity timestamp (Users.last_seen_at)
        - The specific behavior that crossed them over the threshold (which condition flipped most recently)

        Series A: Count of users in PQL state, weekly, label: "Active PQLs"
        Series B: Trailing-7-day PQL → subscription_created (paid, non-trial) conversion rate, label: "PQL Conversion Rate"

        Time range: Current snapshot + last 12 weeks for the trend
        Breakdown: By Users.primary_account_id (account-level aggregation — for B2B-leaning SaaS, multiple PQLs at the same account is the strongest signal; this is a "PQA" — Product Qualified Account)
        Chart type: Sortable table (the leaderboard) plus a secondary trend chart showing weekly PQL volume

        Annotations:
        - Add benchmarks: PQL-to-paid conversion rates of 15-30% are healthy; below 10% suggests threshold is too lenient (qualifying too early). Above 35% means the bar may be too high — you might be missing users who'd convert with sales touch.
        - Flag PQLs who have been over-threshold for 7+ days without sales contact (lost-opportunity signal — every hour of delay reduces conversion).
        - Highlight accounts (primary_account_id) with 3+ users currently in PQL state — these are PQAs and warrant priority sales outreach.
        - Surface the dominant "qualifying behavior" pattern (which threshold was hit most recently) — this informs the right opening message for sales.

        Use case: the single most-cited PLG report across the entire research base (Custify, Correlated, OpenView, ProductLed, Klipfolio, Userpilot all describe it as foundational). Routes high-intent free users to sales when the intent is hottest.

        Taxonomy notes:
        - All thresholds use canonical events: session_start, click_on, goal_completed_in_journey, subscription_created.
        - Users.primary_account_id enables account-level PQA aggregation.
        - Users.utm_source enables ICP filtering.
        - PQL scoring is computed by Lovable from these inputs — the recipe defines the formula.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# PQL Leaderboard

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "PQL Leaderboard".

   This recipe surfaces the highest-intent free users for sales follow-up — the Product Qualified Lead (PQL) leaderboard.

   PQL definition (configurable; default thresholds):
   A user qualifies as a PQL if ALL of the following are true within a 14-day rolling window:
     1. User is currently on a free or trial plan (subscription_created with trial_end populated, OR no active subscription_created)
     2. User has emitted ≥3 distinct sessions (≥3 session_start events on different days)
     3. User has emitted ≥1 goal_completed_in_journey for the activation journey
     4. User has emitted ≥10 click_on events on core feature targets (configurable target_id pattern)
   Optional ICP filter: user's Users.utm_source matches a high-fit channel (configurable)

   For each PQL, surface:
   - User identity (name, email, primary_account_id from Users object)
   - PQL score = a 0-100 number computed from a weighted blend of: session count × 5 + goal completions × 15 + core-feature clicks × 1 + days_since_first_seen as a recency multiplier (capped at the threshold)
   - Days as PQL (how long they've been over the threshold — long-tenured PQLs need urgent sales attention)
   - Most recent activity timestamp (Users.last_seen_at)
   - The specific behavior that crossed them over the threshold (which condition flipped most recently)

   Series A: Count of users in PQL state, weekly, label: "Active PQLs"
   Series B: Trailing-7-day PQL → subscription_created (paid, non-trial) conversion rate, label: "PQL Conversion Rate"

   Time range: Current snapshot + last 12 weeks for the trend
   Breakdown: By Users.primary_account_id (account-level aggregation — for B2B-leaning SaaS, multiple PQLs at the same account is the strongest signal; this is a "PQA" — Product Qualified Account)
   Chart type: Sortable table (the leaderboard) plus a secondary trend chart showing weekly PQL volume

   Annotations:
   - Add benchmarks: PQL-to-paid conversion rates of 15-30% are healthy; below 10% suggests threshold is too lenient (qualifying too early). Above 35% means the bar may be too high — you might be missing users who'd convert with sales touch.
   - Flag PQLs who have been over-threshold for 7+ days without sales contact (lost-opportunity signal — every hour of delay reduces conversion).
   - Highlight accounts (primary_account_id) with 3+ users currently in PQL state — these are PQAs and warrant priority sales outreach.
   - Surface the dominant "qualifying behavior" pattern (which threshold was hit most recently) — this informs the right opening message for sales.

   Use case: the single most-cited PLG report across the entire research base (Custify, Correlated, OpenView, ProductLed, Klipfolio, Userpilot all describe it as foundational). Routes high-intent free users to sales when the intent is hottest.

   Taxonomy notes:
   - All thresholds use canonical events: session_start, click_on, goal_completed_in_journey, subscription_created.
   - Users.primary_account_id enables account-level PQA aggregation.
   - Users.utm_source enables ICP filtering.
   - PQL scoring is computed by Lovable from these inputs — the recipe defines the formula.
   ```
