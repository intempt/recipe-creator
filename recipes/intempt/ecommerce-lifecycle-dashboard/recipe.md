---
id: ecommerce-lifecycle-dashboard
title: Ecommerce lifecycle and retention
slash_command: /ecommerce-lifecycle-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Shows lifecycle distribution, when shoppers reorder, and whether discount codes add revenue or eat into it.
description: >-
  CRM / retention dashboard: lifecycle distribution, replenishment timing, and discount cannibalization.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the lifecycle board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the lifecycle board
    summary: >-
      Lifecycle stage distribution and movement over 90 days, days between first and second order, the
      effect of discount codes on order value, and what customers do right after buying.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Ecommerce Lifecycle".
      Persona: CRM Lead, Retention Marketer, or Loyalty/Lifecycle Manager. Question answered: "How are customers progressing through their lifecycle, and where do I intervene?"
      Distinct from Customer 360: Customer 360 is the "who are my customers" overview; Lifecycle is the "how do I move them" operational view (migration, replenishment timing, discount mechanics, post-purchase touchpoints).
      Board-level configuration:
      - defaultDateRange: last_90_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: lifecycle_score (canonical 6-stage enum)
      Layout: 4 rows.
      Row 1: Lifecycle health KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in Champions"
      - Card 2: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "% in At Risk"
      - Card 3: Insights metric to source recipe: customer-lifecycle-distribution, vizType: metric, titleOverride: "Largest Migration Last 30d"
      - Card 4: Insights metric to source recipe: discount-impact-on-aov-and-margin, vizType: metric, titleOverride: "Net Revenue Impact of Discounts"
      Row 2: Lifecycle distribution + migration (heightPx: 480, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (stacked bar + migration flow side panel: the centerpiece)
      Row 3: Operational levers: timing and discount mechanics (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram: informs replenishment journey timing)
      - Card 2: Insights to source recipe: discount-impact-on-aov-and-margin, displayMode: chart, vizType: bar (per-discount-code AOV impact and net revenue effect)
      Row 4: Post-purchase journey (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Path to source recipe: post-conversion-onboarding-paths, displayMode: chart (what newly-converted customers do)
      - Card 2: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort repeat-purchase by first-order category)
      Annotations:
      - Row 2 (lifecycle distribution + migration, full-width) is the strategic centerpiece.
      - Row 3 turns insight into operational levers.
      - Row 4 closes the loop: post-conversion paths + retention by category.
      Taxonomy notes:
      - Users.lifecycle_score is the canonical 6-stage enum.
      - All source recipes use canonical events: order_created, discount_applied, page_viewed, session_start, subscription_created.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Ecommerce lifecycle and retention

Shows lifecycle distribution, when shoppers reorder, and whether discount codes add revenue or eat into it.

## Steps

1. **Build the lifecycle board** (builds dashboard)

   Lifecycle stage distribution and movement over 90 days, days between first and second order, the effect of discount codes on order value, and what customers do right after buying.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the lifecycle board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
