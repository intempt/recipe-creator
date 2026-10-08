---
id: cohort-acquisition-ltv-dashboard
title: Cohort LTV by acquisition channel
slash_command: /cohort-acquisition-ltv-dashboard
group: Dashboards
owner: intempt
curator: sid
summary: >-
  Monitor acquisition performance with line plots of selected metrics over calendar time. Use the trends to
  see how measures such as revenue or repeat purchases change over time.
description: >-
  A dashboard for tracking acquisition-related metrics over calendar time with Insights line plots. It shows
  trends, not cumulative revenue by cohort age.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
    - finance
  vertical: []
  complexity: standard
  executionMode: live
  tags:
    - dashboard
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new dashboard, from step 1 "Build the cohort LTV board"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the cohort LTV board
    summary: >-
      Cumulative revenue per customer by first-purchase month over 12 months, split by acquisition channel,
      alongside repeat-purchase rate and days to second order.
    builds: dashboard
    description: |-
      Create a Dash board (12-column composition canvas) titled "Cohort Acquisition LTV".
      Persona: Performance Marketer running paid acquisition, or DTC Founder evaluating channel quality. Question answered: "Which acquisition cohorts produce LTV worth keeping? Where should I scale spend? Which channels acquire customers who retain vs. one-and-done?"
      This dashboard is universally cited as the #1 dashboard for $20M+ DTC brands across Common Thread Collective, Conjura, Lifetimely, and Peel. Distinct from Customer 360 (overall customer-base observational) and Ecommerce Revenue (top-line): Cohort LTV is acquisition-month-cohort × revenue curve, with channel decomposition that ties acquisition cost back to long-term value.
      Board-level configuration:
      - defaultDateRange: last_12_months (LTV is inherently long-term; shorter ranges miss the cohort tail)
      - exclusionPeriod: incomplete_periods (recent cohorts haven't had time to mature)
      - visibility: project
      - boardFilters: none by default
      - boardBreakdowns: utm_source: pushed down throughout (the canonical acquisition-channel dimension)
      Layout: 4 rows.
      Row 1: Cohort headline KPIs (heightPx: 200, four metric cards at widthUnits: 3):
      - Card 1: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M6)"
      - Card 2: Insights metric to source recipe: first-purchase-cohort-ltv-curve, vizType: metric, titleOverride: "Average LTV (M12)"
      - Card 3: Retention metric to source recipe: purchase-retention, vizType: metric, titleOverride: "M3 Repeat Purchase Rate"
      - Card 4: Insights metric to source recipe: post-purchase-second-order-velocity, vizType: metric, titleOverride: "Median Days to 2nd Order"
      Row 2: Cohort LTV curves by channel (heightPx: 480, full-width single card at widthUnits: 12):
      - Card 1: Insights to source recipe: first-purchase-cohort-ltv-curve, displayMode: chart, vizType: line (multi-line: each line = a cohort, X-axis = months since first purchase, Y-axis = cumulative revenue per cohort member, broken down by acquisition channel via utm_source). The strategic centerpiece: answers "which channels acquire customers worth keeping."
      Row 3: Repeat-purchase mechanics (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Retention to source recipe: purchase-retention, displayMode: chart, vizType: retention_curve (cohort by first-purchase month: repeat-purchase % over time, by first-order category)
      - Card 2: Insights to source recipe: post-purchase-second-order-velocity, displayMode: chart (histogram of days from 1st to 2nd order: informs replenishment journey timing per category)
      Row 4: Channel revenue and lifecycle context (heightPx: 440, two cards at widthUnits: 6):
      - Card 1: Insights to source recipe: revenue-by-channel, displayMode: chart, vizType: bar (current revenue split per channel: context for the LTV view)
      - Card 2: Insights to source recipe: customer-lifecycle-distribution, displayMode: chart (per-channel customer-lifecycle distribution: answers "which channels acquire Champions vs. At Risk customers")
      Annotations:
      - Row 1's two LTV KPIs (M6 + M12) are the canonical DTC scaling metrics. M6 LTV ≥ 1.5× CAC = healthy unit economics; M12 LTV ≥ 3× CAC = top-quartile. Without ad-spend integration in canonical taxonomy, this dashboard surfaces LTV; CAC must be computed externally and combined.
      - Row 2 (Cohort LTV curves, full-width) is the strategic centerpiece. Reading it: each line is a cohort defined by first-purchase month; the line's slope tells you how fast each cohort accumulates revenue. Channels with steep curves (rapid cumulative revenue) acquire quality customers; channels with flat curves (low cumulative revenue) acquire one-and-done buyers.
      - Row 3 surfaces operational levers:
       - Card 1 (retention curve) shows replenishment patterns by category: categories with steep retention curves (>30% M3 repeat) are candidates for subscribe-and-save or autoship; flat curves (<10% M3) are one-time-purchase categories
       - Card 2 (second-order velocity histogram) tells you the right delay for replenishment journey triggers per category: generic 30-day or 60-day delays often miss the actual median.
      - Row 4 ties it together: which channels are currently producing revenue (Card 1), and what customer types are they acquiring (Card 2). A channel with high current revenue but acquiring mostly At Risk segments is a leading indicator of revenue erosion.
      - Recommended cadence: read this dashboard monthly. Cohort LTV is slow-moving: weekly views over-rotate on noise.
      Taxonomy notes:
      - All source recipes use canonical events: order_created (with items, total_price, customer_id), session_start, page_viewed.
      - Users.utm_source is the canonical first-touch acquisition channel.
      - Users.lifecycle_score is the canonical 6-stage lifecycle enum (At risk / Needs attention / New customers / Promising / Regulars / Champions).
      - This dashboard does NOT include CAC or ROAS metrics because ad-spend events are not in canonical taxonomy V2.1. It surfaces LTV cohort quality; CAC must be computed externally and combined for full unit economics analysis.
outputs:
  - key: dashboard
    producedByStep: s1
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cohort LTV by acquisition channel

Monitor acquisition performance with line plots of selected metrics over calendar time. Use the trends to see how measures such as revenue or repeat purchases change over time.

## Steps

1. **Build the cohort LTV board** (builds dashboard)

   Cumulative revenue per customer by first-purchase month over 12 months, split by acquisition channel, alongside repeat-purchase rate and days to second order.

## What you end up with

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new dashboard, from step 1 "Build the cohort LTV board"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard.
