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
  shortDescription: "Produce a Retention report comparing week-1 feature adopters vs non-adopters with side-by-side retention curves."
  availability: coming-soon
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
        Create a Retention report called "Retention Lifted by Feature Adoption".

        Configuration: this recipe runs for a configurable target feature, identified by click_on.target_id (default: the most-clicked target_id matching the feature pattern in the last 30 days; user can specify).

        Cohort definitions:
        - Cohort A: users who emitted a click_on event with the target_id within their first 7 days after user_created ("early adopters")
        - Cohort B: users who did NOT emit a click_on with the target_id within their first 7 days ("non-adopters")

        Anchor event: user_created
        Return event: session_start
        Cohort granularity: Weekly (signup cohorts based on user_created)
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
        - Highlight the cohort size of "early adopters" — if it's <30% of the base, the feature isn't getting enough first-week exposure.

        Surface whether the target feature is genuinely retention-correlated. This is the canonical "magic moment" / "north-star action" analysis.

        Taxonomy notes:
        - click_on.target_id is the canonical feature handle. user_created and session_start are canonical.
        - Cohort A/B split is computed from the existence of a click_on event with the matching target_id within 7 days of user_created.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Retention Lifted by Feature Adoption

## Procedure

1. **Build Retention Report** [`build_retention_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Retention report called "Retention Lifted by Feature Adoption".

   Configuration: this recipe runs for a configurable target feature, identified by click_on.target_id (default: the most-clicked target_id matching the feature pattern in the last 30 days; user can specify).

   Cohort definitions:
   - Cohort A: users who emitted a click_on event with the target_id within their first 7 days after user_created ("early adopters")
   - Cohort B: users who did NOT emit a click_on with the target_id within their first 7 days ("non-adopters")

   Anchor event: user_created
   Return event: session_start
   Cohort granularity: Weekly (signup cohorts based on user_created)
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
   - Highlight the cohort size of "early adopters" — if it's <30% of the base, the feature isn't getting enough first-week exposure.

   Surface whether the target feature is genuinely retention-correlated. This is the canonical "magic moment" / "north-star action" analysis.

   Taxonomy notes:
   - click_on.target_id is the canonical feature handle. user_created and session_start are canonical.
   - Cohort A/B split is computed from the existence of a click_on event with the matching target_id within 7 days of user_created.
   ```
