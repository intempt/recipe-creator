---
name: retention-lifted-by-feature-adoption
description: |
  Use when a user mentions "retention lifted by feature adoption", or asks for related help. Side-by-side cohort retention curves for users who adopted a target feature in week 1 vs those who didn't.
arguments: []
intempt:
  id: retention-lifted-by-feature-adoption
  version: 1.0.0
  slashCommand: /retention-lifted-by-feature-adoption
  group: Reports
  title: "Retention lift from a feature"
  shortDescription: "Compares how long users stay when they adopt a given feature in their first week against users who never touch it."
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
      title: "Compare adopters and non adopters"
      command: build_retention_report
      produces: report
      bindsAs: report
      description: "Two weekly retention curves over 12 weeks: users who clicked the target feature within 7 days of signing up, and users who did not. Shows the gap in percentage points at weeks 1, 4, 8 and 12 and flags a week 4 gap above 15 points."
      prompt: |
        Create a Retention report called "Retention Lifted by Feature Adoption".

        Configuration: this recipe runs for a configurable target feature (default: the most-clicked feature in the last 30 days; user can specify).

        Cohort definitions:
        - Cohort A: users who clicked the target feature within their first 7 days after they were created ("early adopters")
        - Cohort B: users who did NOT click the target feature within their first 7 days ("non-adopters")

        Anchor event: User created
        Return event: Session start
        Cohort granularity: Weekly (signup cohorts based on when the user was created)
        Time range: Last 12 weeks
        Chart type: Two retention curves overlaid (Cohort A in one color, Cohort B in another) plus delta line showing absolute retention gap at each week

        For each week (W1, W2, W4, W8, W12), surface:
        - Cohort A retention rate
        - Cohort B retention rate
        - Absolute retention gap (A − B) in percentage points
        - Cohort sizes

        Annotations:
        - Flag the week where the retention gap is largest (the "magic moment").
        - Flag if W4 retention gap is >15 percentage points (the feature is a strong retention lever).
        - Flag if W12 retention gap is <5 percentage points (feature isn't actually retention-driving).
        - Highlight the cohort size of "early adopters": if it's <30% of the base, the feature isn't getting enough first-week exposure.

        Surface whether the target feature is genuinely retention-correlated. This is the canonical "magic moment" / "north-star action" analysis.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Retention lift from a feature

Compares how long users stay when they adopt a given feature in their first week against users who never touch it.

## What it does

1. **Compare adopters and non adopters** (`build_retention_report`)

   Two weekly retention curves over 12 weeks: users who clicked the target feature within 7 days of signing up, and users who did not. Shows the gap in percentage points at weeks 1, 4, 8 and 12 and flags a week 4 gap above 15 points.

## What you end up with

- **report** (report): Report produced by this recipe.
