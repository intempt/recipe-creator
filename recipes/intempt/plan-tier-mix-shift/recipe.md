---
id: plan-tier-mix-shift
title: Plan tier mix shift
slash_command: /plan-tier-mix-shift
group: Reports
owner: intempt
summary: Shows how revenue and customer count are spread across plans over time, and whether the business
  is drifting up market or down.
description: >-
  % of revenue and % of customers per plan over time, surfacing up-market vs down-market drift.
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
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Compare revenue and customer mix"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Compare revenue and customer mix
    summary: >-
      Monthly share of recurring revenue and share of active customers per plan over 12 months, drawn
      as two stacked areas side by side with a year over year comparison. Flags any plan whose revenue
      share moved more than 5 points.
    builds: report
    description: |-
      Create an Insights report called "Plan-Tier Mix Shift".
      Series A: Event "revenue_completed" filtered to recurring revenue type (or invoice_paid as fallback), aggregation: Sum of "amount", unit: $
      Series B: Count of users with an active subscription at month-end (active = has subscription_created with status in active states, no subsequent subscription_cancelled or subscription_expired before the month-end)
      Series C: Computed: Series A by plan / total Series A × 100, unit: %, label: "% of Revenue by Plan"
      Series D: Computed: Series B by plan / total Series B × 100, unit: %, label: "% of Customers by Plan"
      Time granularity: Monthly
      Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)
      Time range: Last 12 months
      Compare: Year-over-year
      Chart type: Two stacked area charts side-by-side: Series C (revenue mix) and Series D (customer mix)
      Annotations:
      - For each plan, label start-of-period and end-of-period share with the change in percentage points.
      - Flag any plan whose share of revenue shifted by >5 percentage points YoY.
      - Highlight any divergence between revenue mix and customer mix (e.g., higher tier growing as % of revenue but flat as % of customers = ARPA going up = pricing/positioning working).
      - Flag the opposite divergence (customer mix shifting up-market but revenue mix flat = discounting eroding the up-market thesis).
      This is one of the most consequential questions for SaaS pricing/positioning teams.
      Taxonomy notes:
      - plan_name is on subscription_created. Active subscription status is determined by absence of a later subscription_cancelled / subscription_expired for the same subscription_id.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Plan tier mix shift

Shows how revenue and customer count are spread across plans over time, and whether the business is drifting up market or down.

## Steps

1. **Compare revenue and customer mix** (builds report)

   Monthly share of recurring revenue and share of active customers per plan over 12 months, drawn as two stacked areas side by side with a year over year comparison. Flags any plan whose revenue share moved more than 5 points.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Compare revenue and customer mix"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
