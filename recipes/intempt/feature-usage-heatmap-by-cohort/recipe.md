---
frontmatter_id: feature-usage-heatmap-by-cohort
slash_command: /feature-usage-heatmap-by-cohort
description: Compare feature usage across signup cohorts to see how adoption differs between groups.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how feature adoption differs across signup cohort months with a heatmap, flagging features needing re-introduction
    and cohorts with weak onboarding.
  parameters:
  - name: usage_window
    type: duration
    label: Usage time range
    default: 90 d
    required: false
  - name: cohort_window
    type: duration
    label: Signup cohort window
    default: 6 mo
    required: false
  - name: sticky_threshold
    type: number
    label: Universally sticky adoption threshold (%)
    default: 30
    required: false
  - name: feature_pattern
    type: text
    label: Feature target_id pattern
    default: <UNKNOWN>
    required: true
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a feature control in the product
    properties:
    - name: target_id
      type: text
      meaning: Identifier of the clicked feature
      optional: false
  - slot: user_first_seen
    kind: attribute
    meaning: The date and time a user first appeared in the product (first seen)
  steps:
  - id: s1
    builds: report
    uses:
    - feature_click_event
    - user_first_seen
    - usage_window
    - cohort_window
    - feature_pattern
    - sticky_threshold
    instruction: 'Create an Insights report named "Feature Usage by Cohort". Series A: count unique users of {feature_click_event}
      where {feature_click_event.target_id} matches {feature_pattern}, over {usage_window}. Series B: computed as Series A
      divided by the cohort size times 100, unit %, labeled "Adoption Rate within Cohort". Break down by {feature_click_event.target_id}
      and by the signup cohort month derived from {user_first_seen} bucketed to month. Limit users to those whose {user_first_seen}
      falls within {cohort_window}. Display as a heatmap with features on the Y axis, cohort month on the X axis, cell value
      as adoption rate %, and color intensity scaled. Annotate features showing a left-side fade (older cohorts adopt more
      than newer cohorts) as a likely onboarding regression. Annotate features showing a right-side rise (newer cohorts adopt
      more) as recent improvements. Highlight feature rows where adoption is uniformly above {sticky_threshold}% across all
      cohorts as universally sticky. Highlight cohort columns where adoption is uniformly low across most features as possibly
      broken onboarding. Summarize which features need re-introduction to recent cohorts and which cohort months had degraded
      onboarding.'
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
