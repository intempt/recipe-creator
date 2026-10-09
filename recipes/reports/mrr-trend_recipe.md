---
name: mrr-trend
description: |
  Use when a user mentions "mrr trend", or asks for related help. MRR over time by plan with month-over-month growth rate and net-new MRR overlay.
arguments: []
intempt:
  id: mrr-trend
  version: 1.0.0
  slashCommand: /mrr-trend
  group: Reports
  title: "Monthly recurring revenue trend"
  shortDescription: "Shows recurring revenue by plan over the last 12 months, with the month on month change and how each month compares with the same month last year."
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
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Chart MRR by plan each month"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Monthly recurring revenue summed from completed recurring payments over 12 months, stacked by plan, with net new MRR as a second line and a year over year overlay. Flags any month where net new MRR turned negative."
      prompt: |
        Create an Insights report called "Monthly Recurring Revenue Trend".

        Series A: Revenue completed events where the revenue type indicates a recurring payment (or Invoice paid if that is the recurring revenue marker in this workspace), aggregation: Sum of the payment amount, unit: $, label: "MRR"
          - For Revenue completed, filter by the revenue type indicating subscription/recurring revenue.
          - For Invoice paid as fallback, aggregate the amount paid in cents and divide by 100 to get $.
        Series B: Computed: month-over-month MRR delta (current month MRR − previous month MRR), unit: $, label: "Net New MRR"
        Time granularity: Monthly
        Breakdown for Series A: By Plan: for users with recurring revenue, the plan comes from their Subscription started event (most recent active subscription). Render as stacked area.
        Time range: Last 12 months
        Compare: Year-over-year (same month previous year, dotted overlay)
        Chart type: Stacked area chart for Series A with Series B as a secondary line

        Annotations:
        - Add the absolute MRR figure for the most recent month as a callout.
        - Add the month-over-month growth rate (%) and the trailing 3-month average growth rate.
        - Flag any month where net new MRR went negative (contraction).
        - Highlight any plan tier whose share of MRR shifted by more than 5 percentage points YoY.

        Attributing revenue:
        - Use the revenue type to filter Revenue completed down to recurring revenue; if your workspace does not discriminate revenue type, use Invoice paid as the primary recurring marker instead.
        - Attribute each customer's MRR to the Plan on their most-recent active subscription.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Monthly recurring revenue trend

Shows recurring revenue by plan over the last 12 months, with the month on month change and how each month compares with the same month last year.

## Before you run it

- Connect stripe

## What it does

1. **Chart MRR by plan each month** (`build_insights_report`)

   Monthly recurring revenue summed from completed recurring payments over 12 months, stacked by plan, with net new MRR as a second line and a year over year overlay. Flags any month where net new MRR turned negative.

## What you end up with

- **report** (report): Report produced by this recipe.
