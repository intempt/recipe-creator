---
name: weekly-business-review-summary
description: |
  Use when a user mentions "weekly business review summary", or asks for related help. Single dashboard with the 6 KPIs every founder/exec wants every Monday — new customers, churn, revenue, MRR/ARR, retention, top engagement.
arguments: []
intempt:
  id: weekly-business-review-summary
  version: 1.0.0
  slashCommand: /weekly-business-review-summary
  group: Reports
  shortDescription: 'Single dashboard with the 6 KPIs every founder/exec wants every Monday: new customers, churn, revenue, MRR/ARR, retention, top engagement.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [all]
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
        Create an Insights report called "Weekly Business Review Summary".

        This recipe is a multi-series KPI dashboard combining the headline numbers a founder or exec wants to see every Monday morning. Render as a multi-metric scorecard.

        Series A: Event "user_created", aggregation: Count Unique Users, weekly, label: "New Signups"
        Series B: Event "subscription_created" where trial_end is null (paid signup) OR for ecommerce mode "order_created" where this is the user's first order, aggregation: Count Unique Users, weekly, label: "New Paying Customers"
        Series C: Event "subscription_cancelled" (saas) OR users whose Users.last_seen_at exceeds 90 days (ecommerce churn proxy), weekly, label: "Churned Customers"
        Series D: Event "revenue_completed" with type indicating recurring revenue (saas) OR Sum of order_created.total_price (ecommerce), aggregation: Sum of amount or total_price, weekly, label: "Revenue"
        Series E: Computed — Net New Customers = Series B − Series C, label: "Net New Customers"
        Series F: Trailing 7-day DAU (count of unique users with session_start), label: "Engagement"

        Time granularity: Weekly
        Time range: Last 12 weeks
        Compare: Previous period (prior 12 weeks) AND year-over-year
        Chart type: Multi-card scorecard layout — each metric gets a card showing: current week value, week-over-week % change, year-over-year % change, 12-week trend sparkline

        Annotations on each card:
        - Highlight the current-week value vs. trailing 4-week average (trend indicator: accelerating / steady / decelerating).
        - Flag any metric that moved >15% week-over-week in either direction (exec-attention threshold).
        - Flag any metric trending wrong-direction for 4+ consecutive weeks (durable trend, not noise).
        - Add a quality-of-growth indicator: Net New Customers (E) growing while Churned Customers (C) is also growing = treadmill (high churn offset by acquisition); Net New growing while Churned is flat or shrinking = compounding growth (best-in-class).

        Use case: the WBR-fill report. Founders, execs, and operators run a weekly cadence on the same 5-6 numbers. This recipe makes that cadence one-click — automatically populated, automatically annotated, ready to present. Replaces the spreadsheet most teams maintain manually for this purpose.

        Taxonomy notes:
        - This recipe operates as an aggregator over multiple canonical events. For mode=saas, prioritize subscription/revenue events. For mode=ecommerce, prioritize order events. For mode=all, render both side-by-side.
        - The "churn" definition for ecommerce uses Users.last_seen_at as a proxy because there's no explicit churn event in DTC ecommerce — adjust the threshold (60/90/180 days) per business model.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Weekly Business Review Summary

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Weekly Business Review Summary".

   This recipe is a multi-series KPI dashboard combining the headline numbers a founder or exec wants to see every Monday morning. Render as a multi-metric scorecard.

   Series A: Event "user_created", aggregation: Count Unique Users, weekly, label: "New Signups"
   Series B: Event "subscription_created" where trial_end is null (paid signup) OR for ecommerce mode "order_created" where this is the user's first order, aggregation: Count Unique Users, weekly, label: "New Paying Customers"
   Series C: Event "subscription_cancelled" (saas) OR users whose Users.last_seen_at exceeds 90 days (ecommerce churn proxy), weekly, label: "Churned Customers"
   Series D: Event "revenue_completed" with type indicating recurring revenue (saas) OR Sum of order_created.total_price (ecommerce), aggregation: Sum of amount or total_price, weekly, label: "Revenue"
   Series E: Computed — Net New Customers = Series B − Series C, label: "Net New Customers"
   Series F: Trailing 7-day DAU (count of unique users with session_start), label: "Engagement"

   Time granularity: Weekly
   Time range: Last 12 weeks
   Compare: Previous period (prior 12 weeks) AND year-over-year
   Chart type: Multi-card scorecard layout — each metric gets a card showing: current week value, week-over-week % change, year-over-year % change, 12-week trend sparkline

   Annotations on each card:
   - Highlight the current-week value vs. trailing 4-week average (trend indicator: accelerating / steady / decelerating).
   - Flag any metric that moved >15% week-over-week in either direction (exec-attention threshold).
   - Flag any metric trending wrong-direction for 4+ consecutive weeks (durable trend, not noise).
   - Add a quality-of-growth indicator: Net New Customers (E) growing while Churned Customers (C) is also growing = treadmill (high churn offset by acquisition); Net New growing while Churned is flat or shrinking = compounding growth (best-in-class).

   Use case: the WBR-fill report. Founders, execs, and operators run a weekly cadence on the same 5-6 numbers. This recipe makes that cadence one-click — automatically populated, automatically annotated, ready to present. Replaces the spreadsheet most teams maintain manually for this purpose.

   Taxonomy notes:
   - This recipe operates as an aggregator over multiple canonical events. For mode=saas, prioritize subscription/revenue events. For mode=ecommerce, prioritize order events. For mode=all, render both side-by-side.
   - The "churn" definition for ecommerce uses Users.last_seen_at as a proxy because there's no explicit churn event in DTC ecommerce — adjust the threshold (60/90/180 days) per business model.
   ```
