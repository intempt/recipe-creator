---
id: mrr-trend
title: Monthly recurring revenue trend
slash_command: /mrr-trend
group: Reports
owner: intempt
summary: Shows recurring revenue by plan over the last 12 months, with the month on month change and how
  each month compares with the same month last year.
description: >-
  MRR over time by plan with month-over-month growth rate and net-new MRR overlay.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
prerequisites:
  integrations:
    - value: stripe
      severity: blocking
touches:
  reads:
    - Your Stripe connection
  writes:
    - A new report, from step 1 "Chart MRR by plan each month"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Chart MRR by plan each month
    summary: >-
      Monthly recurring revenue summed from completed recurring payments over 12 months, stacked by plan,
      with net new MRR as a second line and a year over year overlay. Flags any month where net new MRR
      turned negative.
    builds: report
    description: |-
      Create an Insights report called "Monthly Recurring Revenue Trend".
      Series A: Event "revenue_completed" where type indicates a recurring payment (or "invoice_paid" if invoice_paid is the canonical recurring revenue marker in this workspace), aggregation: Sum of "amount" property, unit: $, label: "MRR"
       - For revenue_completed, filter by type indicating subscription/recurring revenue.
       - For invoice_paid as fallback, aggregate amount_paid_cents and divide by 100 to get $.
      Series B: Computed: month-over-month MRR delta (current month MRR − previous month MRR), unit: $, label: "Net New MRR"
      Time granularity: Monthly
      Breakdown for Series A: By plan_name: for revenue_completed users, the plan_name comes from their subscription_created event (most recent active subscription). Render as stacked area.
      Time range: Last 12 months
      Compare: Year-over-year (same month previous year, dotted overlay)
      Chart type: Stacked area chart for Series A with Series B as a secondary line
      Annotations:
      - Add the absolute MRR figure for the most recent month as a callout.
      - Add the month-over-month growth rate (%) and the trailing 3-month average growth rate.
      - Flag any month where net new MRR went negative (contraction).
      - Highlight any plan tier whose share of MRR shifted by more than 5 percentage points YoY.
      Taxonomy notes:
      - revenue_completed has amount, customer_id, type, source: use type to filter for recurring revenue.
      - invoice_paid (Stripe) has amount_paid_cents: use as primary if revenue_completed type-discrimination is not configured.
      - plan_name comes from subscription_created: join to user's most-recent active subscription to attribute the MRR.
      - "subscription_payment" as an event does not exist in the canonical taxonomy.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Monthly recurring revenue trend

Shows recurring revenue by plan over the last 12 months, with the month on month change and how each month compares with the same month last year.

## Steps

1. **Chart MRR by plan each month** (builds report)

   Monthly recurring revenue summed from completed recurring payments over 12 months, stacked by plan, with net new MRR as a second line and a year over year overlay. Flags any month where net new MRR turned negative.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Your Stripe connection

Writes:

- A new report, from step 1 "Chart MRR by plan each month"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
