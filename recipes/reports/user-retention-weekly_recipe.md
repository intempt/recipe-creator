---
name: user-retention-weekly
description: |
  Use when a user mentions "user retention weekly", or asks for related help. Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison.
arguments: []
intempt:
  id: user-retention-weekly
  version: 1.0.0
  slashCommand: /user-retention-weekly
  group: Reports
  title: "Weekly user retention"
  shortDescription: "Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which acquisition sources hold up best."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [retention]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_retention_report
  procedure:
    - step: 1
      title: "Track weekly signup cohorts"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Weekly cohorts anchored on signup over 12 weeks, measuring who starts a session in later weeks, split by acquisition source. Benchmarks week 1 at 40%, week 4 at 25% and week 12 at 15%, and flags cohorts down more than 5 points."
      prompt: |
        Create a Retention report called "Weekly User Retention".

        Anchor event: User created
        Return event: Session start
        Cohort granularity: Weekly
        Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
        Breakdown: By UTM source (acquisition source)
        Compare: Previous period (prior 12 weeks of cohorts)
        Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns

        Annotations:
        - Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
        - Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
        - Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
        - Identify whether retention curves are flattening over time (good (natural retention forming a plateau) or continuously decaying (bad) no stable user base forming).

        Surface the source-by-source retention gap at W4: the moment by which most low-quality signups have churned out.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly user retention

Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which acquisition sources hold up best.

## What it does

1. **Track weekly signup cohorts** (`build_retention_report`)

   Weekly cohorts anchored on signup over 12 weeks, measuring who starts a session in later weeks, split by acquisition source. Benchmarks week 1 at 40%, week 4 at 25% and week 12 at 15%, and flags cohorts down more than 5 points.

## What you end up with

- **report** (report): Report produced by this recipe.
