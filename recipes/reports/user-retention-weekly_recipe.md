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
  shortDescription: "Weekly cohort retention with W1/W4/W12 benchmarks and acquisition-source comparison."
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
      title: "Build Retention Report"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Retention report called "Weekly User Retention".

        Anchor event: user_created
        Return event: session_start
        Cohort granularity: Weekly
        Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
        Breakdown: By Users.utm_source (acquisition source)
        Compare: Previous period (prior 12 weeks of cohorts)
        Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns

        Annotations:
        - Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
        - Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
        - Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
        - Identify whether retention curves are flattening over time (good — natural retention forming a plateau) or continuously decaying (bad — no stable user base forming).

        Surface the source-by-source retention gap at W4 — the moment by which most low-quality signups have churned out.

        Taxonomy notes:
        - user_created and session_start are canonical. Users.utm_source is the canonical first-touch attribute.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# User Retention Weekly

## Procedure

1. **Build Retention Report** [`build_retention_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Retention report called "Weekly User Retention".

   Anchor event: user_created
   Return event: session_start
   Cohort granularity: Weekly
   Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
   Breakdown: By Users.utm_source (acquisition source)
   Compare: Previous period (prior 12 weeks of cohorts)
   Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns

   Annotations:
   - Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
   - Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
   - Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
   - Identify whether retention curves are flattening over time (good — natural retention forming a plateau) or continuously decaying (bad — no stable user base forming).

   Surface the source-by-source retention gap at W4 — the moment by which most low-quality signups have churned out.

   Taxonomy notes:
   - user_created and session_start are canonical. Users.utm_source is the canonical first-touch attribute.
   ```
