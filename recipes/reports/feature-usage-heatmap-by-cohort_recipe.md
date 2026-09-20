---
name: feature-usage-heatmap-by-cohort
description: |
  Use when a user mentions "feature usage heatmap by cohort", or asks for related help. Feature usage by signup cohort with sticky-feature identification and cohort-onboarding regression detection.
arguments: []
intempt:
  id: feature-usage-heatmap-by-cohort
  version: 1.0.0
  slashCommand: /feature-usage-heatmap-by-cohort
  group: Reports
  title: "Feature usage by signup cohort"
  shortDescription: "Shows whether newer signups adopt each feature as well as older ones did, which is how you catch an onboarding change that quietly broke something."
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
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Heatmap features against cohorts"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Adoption rate per feature for each monthly signup cohort from the last 6 months, measured over 90 days of usage. Flags features where older cohorts adopt more than newer ones, and cohorts that adopt little across the board."
      prompt: |
        Create an Insights report called "Feature Usage by Cohort".

        Series A: Event "click_on" filtered by target_id (matching a defined feature pattern), aggregation: Count Unique Users
        Series B: Computed: Series A / cohort size × 100, unit: %, label: "Adoption Rate within Cohort"
        Breakdown: By target_id (feature) AND by cohort month derived from User.first_seen_at (system-set datetime) bucketed to month
        Time range: Last 90 days of usage; cohorts from Users with first_seen_at in the last 6 months
        Chart type: Heatmap (feature on Y axis, cohort month on X axis), cell value = adoption rate %, color intensity scaled

        Annotations:
        - Flag features that show "left-side fade" in the heatmap (older cohorts have higher adoption than newer cohorts): likely an onboarding regression where newer users aren't being introduced to the feature.
        - Flag features that show "right-side rise" (newer cohorts adopt at higher rates): recent product or onboarding improvements working.
        - Highlight rows (features) where adoption is uniformly >30% across all cohorts: universally sticky features.
        - Highlight columns (cohorts) where adoption is uniformly low across most features: that cohort's onboarding may have been broken.

        Surface which features need to be re-introduced to recent cohorts and which cohort months had degraded onboarding.

        Taxonomy notes:
        - Users.first_seen_at is a system-set datetime; "signup_cohort_month" is a derived bucketing of first_seen_at, not a stored property.
        - click_on.target_id is the canonical feature handle.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Feature usage by signup cohort

Shows whether newer signups adopt each feature as well as older ones did, which is how you catch an onboarding change that quietly broke something.

## What it does

1. **Heatmap features against cohorts** (`build_insights_report`)

   Adoption rate per feature for each monthly signup cohort from the last 6 months, measured over 90 days of usage. Flags features where older cohorts adopt more than newer ones, and cohorts that adopt little across the board.

## What you end up with

- **report** (report): Report produced by this recipe.
