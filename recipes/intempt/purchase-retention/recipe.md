---
id: purchase-retention
title: Repeat purchase retention
slash_command: /purchase-retention
group: Reports
owner: intempt
curator: aman
summary: Shows what share of first time buyers come back to buy again, by month and by the category they
  bought first.
description: >-
  Repeat-purchase retention with cohort-level second-purchase rates and time-to-2nd-purchase distribution.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
    - media
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - retention
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Track buyers back for more"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Track buyers back for more
    summary: >-
      Monthly cohorts by month of first order over 12 months, measuring repeat orders at months 1, 3,
      6 and 12, split by first purchase category, plus a distribution of the days between the first and
      second order. Benchmarks the second purchase rate at 27%.
    builds: report
    description: |-
      Create a Retention report called "Purchase Retention".
      Anchor event: order_created (per user, scope: their first order_created to cohort by month of first purchase)
      Return event: order_created (any subsequent order)
      Cohort granularity: Monthly
      Time range: Last 12 months
      Breakdown: By the first-purchase product category: derived from the first order's items.product_id resolved via Products object
      Compare: Previous period (prior 12 months of cohorts)
      Chart type: Retention curve plus cohort table with M1 / M3 / M6 / M12 columns
      Also include a secondary view: "Time from 1st to 2nd purchase" distribution: histogram of days-between, bucketed into 0-7 / 8-30 / 31-90 / 91+ days.
      Annotations:
      - Add benchmarks: 27% of first-time DTC buyers make a 2nd purchase ever; brands at 45%+ are top-quartile.
      - Flag any category where M6 repeat rate is below 15% (one-time-purchase pattern).
      - Flag any cohort where M3 repeat rate dropped >5 percentage points vs. prior cohort (recent acquisition-quality drop).
      - Highlight categories with M3 repeat rate > 30% (high natural-replenishment products: candidates for subscribe-and-save).
      Surface the median time from 1st to 2nd purchase per category: this is the right delay for replenishment journeys.
      Taxonomy notes:
      - "first_order_created" as an event does not exist. "First order" is computed as the earliest order_created per customer_id.
      - "first_purchase_category" is derived from first order's items.product_id to Products.category.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Repeat purchase retention

Shows what share of first time buyers come back to buy again, by month and by the category they bought first.

## Steps

1. **Track buyers back for more** (builds report)

   Monthly cohorts by month of first order over 12 months, measuring repeat orders at months 1, 3, 6 and 12, split by first purchase category, plus a distribution of the days between the first and second order. Benchmarks the second purchase rate at 27%.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Track buyers back for more"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
