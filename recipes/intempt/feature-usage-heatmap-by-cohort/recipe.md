---
description: Compare feature usage across signup cohorts to see how adoption differs between groups.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Feature usage by signup cohort

Slash command: /feature-usage-heatmap-by-cohort

## Step 1: Heatmap features against cohorts

Create an Insights report called "Feature Usage by Cohort".
Series A: Event "Click on" filtered by target_id (matching a defined feature pattern), aggregation: Count Unique Users
Series B: Computed: Series A / cohort size × 100, unit: %, label: "Adoption Rate within Cohort"
Breakdown: By target_id (feature) AND by cohort month derived from User.First seen (system-set datetime) bucketed to month
Time range: Last 90 days of usage; cohorts from Users with First seen in the last 6 months
Chart type: Heatmap (feature on Y axis, cohort month on X axis), cell value = adoption rate %, color intensity scaled
Annotations:
- Flag features that show "left-side fade" in the heatmap (older cohorts have higher adoption than newer cohorts): likely an onboarding regression where newer users aren't being introduced to the feature.
- Flag features that show "right-side rise" (newer cohorts adopt at higher rates): recent product or onboarding improvements working.
- Highlight rows (features) where adoption is uniformly >30% across all cohorts: universally sticky features.
- Highlight columns (cohorts) where adoption is uniformly low across most features: that cohort's onboarding may have been broken.
Surface which features need to be re-introduced to recent cohorts and which cohort months had degraded onboarding.
Taxonomy notes:
- Users.First seen is a system-set datetime; "signup_cohort_month" is a derived bucketing of First seen, not a stored property.
- Click on.target_id is the canonical feature handle.
