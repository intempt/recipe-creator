---
id: first-purchase-cohort-ltv-curve
title: First purchase LTV curve
slash_command: /first-purchase-cohort-ltv-curve
group: Reports
owner: intempt
summary: Shows cumulative revenue per customer for each monthly cohort as it ages, so you can see which
  acquisition months and channels pay back.
description: >-
  Cumulative revenue per cohort member by cohort age: the textbook DTC LTV view.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: quick
  executionMode: live
  tags:
    - insights
steps:
  - id: s1
    title: Plot revenue per cohort by age
    summary: >-
      Cumulative revenue per cohort member for each of the last 12 monthly cohorts, grouped by the month
      of a customer's first order and split by acquisition source. Marks cohorts that are still incomplete
      and flags any whose curve flattens by month 3 to 6.
    builds: report
    description: |-
      Create an Insights report called "First-Purchase Cohort LTV Curve".
      Series A: Event "order_created", aggregation: Sum of "total_price", scoped per user, cumulative from each user's first order_created
      Series B: Computed: Series A / cohort size, unit: $, label: "Cumulative Revenue per Cohort Member"
      Cohort: Monthly cohort defined by month of first order_created (each user's first order_created event determines their cohort)
      Time range: Last 12 months of cohorts (allow some cohorts to have shorter LTV tails: surface "incomplete cohort" labels for the most recent ones)
      Breakdown: By Users.utm_source (the user's first-touch acquisition channel, from the Users object)
      Chart type: Multi-line chart: each line is a cohort, X axis is cohort age in months (0, 1, 2, ..., 12), Y axis is cumulative revenue per cohort member
      Annotations:
      - Highlight the highest-LTV cohort and lowest-LTV cohort at month 6 and month 12.
      - Flag any cohort where LTV growth flattens prematurely (LTV-curve "going horizontal" by month 3-6 indicates a one-time-buyer cohort).
      - Highlight channels where cohort LTV is increasing across recent cohorts (acquisition quality improving).
      Taxonomy notes:
      - "First purchase" is determined per-user by the earliest order_created event for that customer_id.
      - Users.utm_source is a real first-touch attribution attribute on the Users object.
      - LTV is cumulative sum of order_created.total_price per user from first purchase onward.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# First purchase LTV curve

Shows cumulative revenue per customer for each monthly cohort as it ages, so you can see which acquisition months and channels pay back.

## Steps

1. **Plot revenue per cohort by age** (builds report)

   Cumulative revenue per cohort member for each of the last 12 monthly cohorts, grouped by the month of a customer's first order and split by acquisition source. Marks cohorts that are still incomplete and flags any whose curve flattens by month 3 to 6.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
