---
id: return-rate-by-category
title: Return rate by category
slash_command: /return-rate-by-category
group: Reports
owner: intempt
summary: Shows which product categories get returned most, and which ones have got worse since last quarter.
description: >-
  Return rate by product category with previous-period comparison and rising-rate flagging.
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
    title: Rank categories by returns
    summary: >-
      Return requests as a percentage of fulfilled orders by product category over the last 90 days, compared
      with the prior 90. Flags any category up more than 5 points and lists the top 5 by volume and the
      top 5 by rate.
    builds: report
    description: |-
      Create an Insights report called "Return Rate by Category".
      Series A: Event "order_fulfilled", aggregation: Count
      Series B: Event "return_requested", aggregation: Count
      Formula: (B / A) × 100, unit: %, label: "Return Rate"
      Breakdown: By product category: derive from return_requested.items joined to Products to find category, OR from the source order's items (return_requested carries order_id relation).
      Time range: Last 90 days
      Compare: Previous period (prior 90 days)
      Chart type: Bar chart sorted by total return rate descending
      Annotations:
      - Flag any category where return rate jumped >5 percentage points vs. prior period.
      - Surface top 5 categories by absolute return volume and top 5 by return rate (the lists are usually different and both matter).
      Taxonomy notes:
      - return_requested has items, order_id (relation), return_id, status. Items resolve to categories through the Products record object.
      - Note: there is no canonical "return_reason" property on return_requested. Reason analysis would require joining with order_refunded (which has a reason text field) when the return is monetized.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Return rate by category

Shows which product categories get returned most, and which ones have got worse since last quarter.

## Steps

1. **Rank categories by returns** (builds report)

   Return requests as a percentage of fulfilled orders by product category over the last 90 days, compared with the prior 90. Flags any category up more than 5 points and lists the top 5 by volume and the top 5 by rate.

## What you end up with

- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build report.
