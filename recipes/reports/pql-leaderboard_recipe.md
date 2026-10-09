---
name: pql-leaderboard
description: |
  Use when a user mentions "pql leaderboard", or asks for related help. Sortable list of free users hitting configurable PQL thresholds: the canonical PLG sales-handoff report.
arguments: []
intempt:
  id: pql-leaderboard
  version: 1.0.0
  slashCommand: /pql-leaderboard
  group: Reports
  title: "Product qualified lead leaderboard"
  shortDescription: "Ranks the free users showing the strongest buying signals, with a score and contact details, so sales knows who to call first."
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
      title: "Rank free users by buying signal"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Free and trial users who, in a rolling 14 day window, had 3 or more sessions on separate days, completed an activation goal and made 10 or more clicks on core features. Each gets a 0 to 100 score, contact details and the number of days they have qualified."
      prompt: |
        Create an Insights report called "PQL Leaderboard".

        This recipe surfaces the highest-intent free users for sales follow-up: the Product Qualified Lead (PQL) leaderboard.

        PQL definition (configurable; default thresholds):
        A user qualifies as a PQL if ALL of the following are true within a 14-day rolling window:
          1. User is currently on a free or trial plan (Subscription started with a trial end date, OR no active subscription)
          2. User has emitted ≥3 distinct sessions (≥3 Session start events on different days)
          3. User has emitted ≥1 completed journey goal for the activation journey
          4. User has emitted ≥10 Click on events on core feature targets (configurable feature target)
        Optional ICP filter: user's UTM source matches a high-fit channel (configurable)

        For each PQL, surface:
        - User identity (name, email, the account the user belongs to)
        - PQL score = a 0-100 number computed from a weighted blend of: session count × 5 + goal completions × 15 + core-feature clicks × 1 + days since first seen as a recency multiplier (capped at the threshold)
        - Days as PQL (how long they've been over the threshold: long-tenured PQLs need urgent sales attention)
        - Most recent activity timestamp (Last seen)
        - The specific behavior that crossed them over the threshold (which condition flipped most recently)

        Series A: Count of users in PQL state, weekly, label: "Active PQLs"
        Series B: Trailing-7-day PQL to paid (non-trial) subscription conversion rate, label: "PQL Conversion Rate"

        Time range: Current snapshot + last 12 weeks for the trend
        Breakdown: By the account each user belongs to (account-level aggregation (for B2B-leaning SaaS, multiple PQLs at the same account is the strongest signal; this is a "PQA") Product Qualified Account)
        Chart type: Sortable table (the leaderboard) plus a secondary trend chart showing weekly PQL volume

        Annotations:
        - Add benchmarks: PQL-to-paid conversion rates of 15-30% are healthy; below 10% suggests threshold is too lenient (qualifying too early). Above 35% means the bar may be too high: you might be missing users who'd convert with sales touch.
        - Flag PQLs who have been over-threshold for 7+ days without sales contact (lost-opportunity signal: every hour of delay reduces conversion).
        - Highlight accounts with 3+ users currently in PQL state: these are PQAs and warrant priority sales outreach.
        - Surface the dominant "qualifying behavior" pattern (which threshold was hit most recently): this informs the right opening message for sales.

        Use case: the single most-cited PLG report across the entire research base (Custify, Correlated, OpenView, ProductLed, Klipfolio, Userpilot all describe it as foundational). Routes high-intent free users to sales when the intent is hottest.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product qualified lead leaderboard

Ranks the free users showing the strongest buying signals, with a score and contact details, so sales knows who to call first.

## What it does

1. **Rank free users by buying signal** (`build_insights_report`)

   Free and trial users who, in a rolling 14 day window, had 3 or more sessions on separate days, completed an activation goal and made 10 or more clicks on core features. Each gets a 0 to 100 score, contact details and the number of days they have qualified.

## What you end up with

- **report** (report): Report produced by this recipe.
