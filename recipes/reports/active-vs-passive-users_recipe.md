---
name: active-vs-passive-users
description: |
  Use when a user mentions "active vs. passive users", or asks for related help. Three-way split: producers (frequent click_on), consumers (only page_viewed/session_start), and inactive — the hidden segment most teams miss.
arguments: []
intempt:
  id: active-vs-passive-users
  version: 1.0.0
  slashCommand: /active-vs-passive-users
  group: Reports
  shortDescription: "Creates a trailing-30-day Insights report classifying each user as Producer, Consumer, Lurker, or Inactive by event thresholds."
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
        Create an Insights report called "Active vs. Passive Users".

        Per-user classification computed from the trailing 30-day window:
          - Producer: emitted ≥10 click_on events AND ≥1 submit_on (taking actions, creating, configuring)
          - Consumer: emitted ≥3 session_start AND ≥10 page_viewed BUT <5 click_on (browsing, reading, but not creating)
          - Lurker: emitted ≥1 session_start in the last 30 days BUT below both thresholds above (logging in but barely engaging)
          - Inactive: zero session_start in the last 30 days

        Series A: Count Unique Users per classification bucket, time granularity: Weekly
        Series B: Computed — share of total active users (excluding Inactive) per bucket, unit: %
        Series C: Sum of subscription_created.amount or revenue_completed.amount per bucket — surfaces revenue concentration

        Time granularity: Weekly snapshot
        Time range: Last 12 weeks
        Breakdown: By plan_name (resolved from each user's most-recent active subscription_created)
        Compare: Previous period (prior 12 weeks)
        Chart type: Stacked area chart for the weekly distribution, with a secondary view showing revenue concentration per bucket

        Annotations:
        - Add the classic distribution: in healthy products, Producers should be 20-40% of active users, Consumers 40-60%, Lurkers 10-20%. If Producers are <15%, the product is "leaning consumer" — engagement risk.
        - Flag if the Producer share is shrinking week-over-week (engagement erosion — leading indicator of churn before retention metrics catch it).
        - Highlight Consumer-to-Producer migration rate: of users classified as Consumer last week, what % became Producers this week? This is the latent activation rate.
        - Surface revenue concentration: in many SaaS products, Producers generate disproportionate revenue. If Producers are <20% of users but >70% of revenue, you have a "power user" risk — losing one Producer hurts more than losing 10 Lurkers.
        - Flag any plan tier where Producer share is materially lower than other tiers (the plan is acquiring lurkers — pricing/positioning issue).

        Use case: most engagement reports just count "active users." This recipe surfaces the hidden segment of "active but passive" — users who log in regularly but never DO anything. They look retained but are pre-churn. Catching them before they go inactive is high-leverage.

        Taxonomy notes:
        - click_on, submit_on, page_viewed, session_start are all canonical. submit_on is specifically the "user took an action" canonical event (form submissions, etc.).
        - The classification thresholds are configurable per workspace.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Active vs. Passive Users

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Active vs. Passive Users".

   Per-user classification computed from the trailing 30-day window:
     - Producer: emitted ≥10 click_on events AND ≥1 submit_on (taking actions, creating, configuring)
     - Consumer: emitted ≥3 session_start AND ≥10 page_viewed BUT <5 click_on (browsing, reading, but not creating)
     - Lurker: emitted ≥1 session_start in the last 30 days BUT below both thresholds above (logging in but barely engaging)
     - Inactive: zero session_start in the last 30 days

   Series A: Count Unique Users per classification bucket, time granularity: Weekly
   Series B: Computed — share of total active users (excluding Inactive) per bucket, unit: %
   Series C: Sum of subscription_created.amount or revenue_completed.amount per bucket — surfaces revenue concentration

   Time granularity: Weekly snapshot
   Time range: Last 12 weeks
   Breakdown: By plan_name (resolved from each user's most-recent active subscription_created)
   Compare: Previous period (prior 12 weeks)
   Chart type: Stacked area chart for the weekly distribution, with a secondary view showing revenue concentration per bucket

   Annotations:
   - Add the classic distribution: in healthy products, Producers should be 20-40% of active users, Consumers 40-60%, Lurkers 10-20%. If Producers are <15%, the product is "leaning consumer" — engagement risk.
   - Flag if the Producer share is shrinking week-over-week (engagement erosion — leading indicator of churn before retention metrics catch it).
   - Highlight Consumer-to-Producer migration rate: of users classified as Consumer last week, what % became Producers this week? This is the latent activation rate.
   - Surface revenue concentration: in many SaaS products, Producers generate disproportionate revenue. If Producers are <20% of users but >70% of revenue, you have a "power user" risk — losing one Producer hurts more than losing 10 Lurkers.
   - Flag any plan tier where Producer share is materially lower than other tiers (the plan is acquiring lurkers — pricing/positioning issue).

   Use case: most engagement reports just count "active users." This recipe surfaces the hidden segment of "active but passive" — users who log in regularly but never DO anything. They look retained but are pre-churn. Catching them before they go inactive is high-leverage.

   Taxonomy notes:
   - click_on, submit_on, page_viewed, session_start are all canonical. submit_on is specifically the "user took an action" canonical event (form submissions, etc.).
   - The classification thresholds are configurable per workspace.
   ```
