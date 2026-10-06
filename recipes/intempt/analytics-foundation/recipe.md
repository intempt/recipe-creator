---
id: analytics-foundation
title: Analytics foundation
slash_command: /analytics-foundation
group: Reports
owner: intempt
curator: aman
summary: >-
  Set up core analytics from your events: Insights, Funnels, and Retention reports, plus an executive
  dashboard for headline numbers.
description: >-
  Map events, build Insights, Funnels, and Retention reports, then compose an executive dashboard.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - finance
    - media
  vertical: []
  complexity: standard
  executionMode: scheduled
  tags:
    - analytics-foundation
prerequisites:
  events:
    - value: session_start
      severity: blocking
    - value: page_viewed
      severity: blocking
    - value: click_on
      severity: recommended
touches:
  reads:
    - The session_start event in your project
    - The page_viewed event in your project
    - The click_on event in your project
  writes:
    - A new report, from step 1 "Build the core report set"
    - A new dashboard, from step 2 "Compose the exec dashboard"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the core report set
    summary: >-
      Creates the four reports every team starts with: key metrics, conversion funnels, cohort retention
      and user flows.
    builds: report
    description: >-
      Build the core report set: Insights (key metrics), Funnels (conversion paths), Retention (cohort
      analysis), Paths (user flows).
  - id: s2
    title: Compose the exec dashboard
    summary: >-
      Pulls the headline numbers onto one dashboard, each with a period comparison and a trend.
    builds: dashboard
    description: >-
      Compose an executive dashboard surfacing headline metrics with comparisons and trends. Use the result
      of "Build the core report set".
    dependsOn:
      - s1
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
  - key: dashboard
    producedByStep: s2
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Analytics foundation

Set up core analytics from your events: Insights, Funnels, and Retention reports, plus an executive dashboard for headline numbers.

## Steps

1. **Build the core report set** (builds report)

   Creates the four reports every team starts with: key metrics, conversion funnels, cohort retention and user flows.

2. **Compose the exec dashboard** (builds dashboard)

   Pulls the headline numbers onto one dashboard, each with a period comparison and a trend.

## What you end up with

- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The session_start event in your project
- The page_viewed event in your project
- The click_on event in your project

Writes:

- A new report, from step 1 "Build the core report set"
- A new dashboard, from step 2 "Compose the exec dashboard"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, report.
