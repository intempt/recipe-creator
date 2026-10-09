---
name: trial-to-paid-conversion-rate
description: |
  Use when a user mentions "trial-to-paid conversion rate", or asks for related help. Weekly trial-to-paid conversion using trial start and end dates with an 18% benchmark.
arguments: []
intempt:
  id: trial-to-paid-conversion-rate
  version: 1.0.0
  slashCommand: /trial-to-paid-conversion-rate
  group: Reports
  title: "Trial to paid conversion rate"
  shortDescription: "Shows what share of trials turn into paying customers each week, by signup source, against the 18% industry median."
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
      title: "Track trial conversion weekly"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Weekly cohorts of trial starts over the last 12 weeks where the trial window has fully elapsed, measuring how many went on to pay, split by signup source. Draws benchmark lines at 18% for the median and 25% for top quartile."
      prompt: |
        Create an Insights report called "Trial-to-Paid Conversion Rate".

        Series A: Event Subscription started where the trial end date is not null AND the trial start date is not null, aggregation: Count Unique Users
           this is the trial-start cohort
        Series B: Event Subscription started filtered to users in Series A whose subsequent subscription transitioned out of trial state: operationally: count users in Series A who have a follow-on Revenue completed event or an Invoice paid event after the trial end date
        Formula: (B / A) × 100, unit: %, label: "Trial-to-Paid Conversion"
        Time granularity: Weekly (cohort by trial-start week, allow the trial window to fully elapse before counting)
        Time range: Last 12 weeks (where the trial window has fully elapsed)
        Breakdown: By UTM source (signup source)
        Compare: Previous period (previous 12 weeks)
        Chart type: Line chart with previous-period overlay

        Annotations:
        - Add a horizontal benchmark line at 18% (median for B2B SaaS with self-serve trials).
        - Add a horizontal benchmark line at 25% (top-quartile threshold).
        - Highlight any week where the conversion rate dropped >3 percentage points vs. previous period.

        Identify which signup source has the highest conversion AND volume: that's where to double down on acquisition spend.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Trial to paid conversion rate

Shows what share of trials turn into paying customers each week, by signup source, against the 18% industry median.

## Before you run it

- Connect stripe

## What it does

1. **Track trial conversion weekly** (`build_insights_report`)

   Weekly cohorts of trial starts over the last 12 weeks where the trial window has fully elapsed, measuring how many went on to pay, split by signup source. Draws benchmark lines at 18% for the median and 25% for top quartile.

## What you end up with

- **report** (report): Report produced by this recipe.
