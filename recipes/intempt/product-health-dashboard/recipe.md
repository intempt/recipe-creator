---
id: product-health-dashboard
title: Product engagement and adoption
slash_command: /product-health-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Answers whether the product is getting more or less engaging, which features users return to, and how users
  say they feel. The cohort heatmap output is in Retention, not Insights.
description: >-
  PM view: stickiness, feature adoption depth, retention by feature, NPS, and the active vs passive user
  split. Cohort heatmap is available under Retention.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the product health board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the product health board
    summary: >-
      Stickiness and feature adoption depth, retention split by which feature was used, NPS, and the split
      between active and passive users.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Product Health".
      Persona: Product Manager / Product Lead. Question answered: "Is the product getting more or less engaging? Which features matter? How do users feel about it?"
      Board-level configuration:
      - defaultDateRange: last_30_days
      - exclusionPeriod: incomplete_periods
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: plan_name (resolved from each user's most-recent active subscription): pushed down to all cards as a secondary breakdown
      Layout: 4 rows.
      Row 1: Engagement headline (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: stickiness-ratios-dau-wau-mau, vizType: metric, titleOverride: "DAU/MAU Stickiness"
      - Card 2: Insights metric to source recipe: weekly-active-users-trend, vizType: metric, titleOverride: "WAU"
      - Card 3: Insights metric to source recipe: active-vs-passive-users, vizType: metric, titleOverride: "Producer Share %"
      - Card 4: Insights metric to source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"
      Row 2: Feature engagement depth (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
      - Card 2: Funnel to source recipe: feature-discovery-adoption, displayMode: chart, vizType: funnel_steps
      Row 3: Retention drivers (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Retention to source recipe: retention-lifted-by-feature-adoption, displayMode: chart (the side-by-side curve comparison)
      - Card 2: Insights to source recipe: feature-usage-heatmap-by-cohort, displayMode: chart, vizType: heatmap
      Row 4: Engagement segmentation and support pulse (heightPx: 400, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: active-vs-passive-users, displayMode: chart, vizType: stacked_area
      - Card 2: Insights to source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line (dual-axis)
      Annotations:
      - Row 1's four KPIs together answer: are users active (WAU), are they sticky (DAU/MAU), are they actively producing (Producer Share %), and how do they feel (NPS). Each is a different lens; reading them together is the key.
      - The board's value comes from reading the four rows together: Row 1 reports headline state, Row 2 reports feature engagement depth, Row 3 reports retention drivers, Row 4 reports segmentation and support pulse.
      Taxonomy notes:
      - All 8 source recipes are taxonomy-grounded.
      - nps-tracking depends on feedback_submitted events with survey_type = "nps": see that recipe's notes.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product engagement and adoption

Answers whether the product is getting more or less engaging, which features users return to, and how users say they feel. The cohort heatmap output is in Retention, not Insights.

## Steps

1. **Build the product health board** (builds dashboard)

   Stickiness and feature adoption depth, retention split by which feature was used, NPS, and the split between active and passive users.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the product health board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
