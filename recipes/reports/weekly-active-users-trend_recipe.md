---
name: weekly-active-users-trend
description: |
  Use when a user mentions "weekly active users trend", or asks for related help. WAU trend with WAU/MAU stickiness ratio — the standard PLG engagement view.
arguments: []
intempt:
  id: weekly-active-users-trend
  version: 1.0.0
  slashCommand: /weekly-active-users-trend
  group: Reports
  shortDescription: "Build an Insights report tracking weekly active users and WAU/MAU stickiness ratio over time."
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
        Create an Insights report called "Weekly Active Users Trend".

        Series A: Event "session_start", aggregation: Count Unique Users, time granularity: Weekly, label: "WAU"
          (alternative: use "identify" if the workspace uses identify as the active-user signal)
        Series B: Event "session_start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
        Series C: Computed — Series A (WAU) / Series B (MAU) × 100, unit: %, label: "Stickiness (WAU/MAU)"
        Time granularity: Weekly
        Time range: Last 12 weeks
        Breakdown: By plan_name — derive from each user's most-recent active subscription_created.plan_name
        Compare: Previous period (prior 12 weeks)
        Chart type: Dual-axis — left axis user counts (WAU/MAU as lines), right axis stickiness % (line)

        Annotations:
        - Add a horizontal benchmark line at 20% stickiness (industry "good" for B2B SaaS).
        - Add a horizontal benchmark at 50% (top-quartile, near-daily-use products).
        - Highlight any plan where stickiness dropped >3 points vs. previous period.
        - Flag any plan where WAU is growing but stickiness is falling (acquiring users but losing engagement).

        Stickiness is the leading indicator of retention; raw WAU growth without stickiness growth is a vanity metric.

        Taxonomy notes:
        - session_start is canonical and carries device_type, country, utm_source. "user_active" as an event does not exist; session_start (or identify) is the active-user signal.
        - plan_tier as a property does not exist; plan_name on subscription_created is the canonical plan attribute.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Weekly Active Users Trend

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Weekly Active Users Trend".

   Series A: Event "session_start", aggregation: Count Unique Users, time granularity: Weekly, label: "WAU"
     (alternative: use "identify" if the workspace uses identify as the active-user signal)
   Series B: Event "session_start", aggregation: Count Unique Users, rolling 28-day window, label: "MAU"
   Series C: Computed — Series A (WAU) / Series B (MAU) × 100, unit: %, label: "Stickiness (WAU/MAU)"
   Time granularity: Weekly
   Time range: Last 12 weeks
   Breakdown: By plan_name — derive from each user's most-recent active subscription_created.plan_name
   Compare: Previous period (prior 12 weeks)
   Chart type: Dual-axis — left axis user counts (WAU/MAU as lines), right axis stickiness % (line)

   Annotations:
   - Add a horizontal benchmark line at 20% stickiness (industry "good" for B2B SaaS).
   - Add a horizontal benchmark at 50% (top-quartile, near-daily-use products).
   - Highlight any plan where stickiness dropped >3 points vs. previous period.
   - Flag any plan where WAU is growing but stickiness is falling (acquiring users but losing engagement).

   Stickiness is the leading indicator of retention; raw WAU growth without stickiness growth is a vanity metric.

   Taxonomy notes:
   - session_start is canonical and carries device_type, country, utm_source. "user_active" as an event does not exist; session_start (or identify) is the active-user signal.
   - plan_tier as a property does not exist; plan_name on subscription_created is the canonical plan attribute.
   ```
