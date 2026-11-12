---
frontmatter_id: retention-lifted-by-feature-adoption
slash_command: /retention-lifted-by-feature-adoption
description: Compares how long users stay when they adopt a given feature in their first week against users who never touch it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows whether adopting a chosen feature in the first week goes with higher user retention than not adopting it,
    with retention gaps flagged at W4 and W12.
  parameters:
  - name: target_id
    type: string
    label: Target feature identifier (Click on target_id) to analyse
    default: most-clicked target_id matching the feature pattern in the last 30 days
    required: false
  - name: adoption_window
    type: duration
    label: Window after User created that counts as early adoption
    default: 7 d
    required: false
  - name: retention_window_weeks
    type: number
    label: Retention weeks reported alongside the curves
    default: 12
    required: false
  - name: strong_lever_gap_pp
    type: number
    label: W4 retention gap (percentage points) above which the feature is flagged as a strong retention lever
    default: 15
    required: false
  - name: weak_gap_pp
    type: number
    label: W12 retention gap (percentage points) below which the feature is flagged as not retention-driving
    default: 5
    required: false
  - name: low_exposure_share
    type: number
    label: Early adopter share of the base (%) below which first-week exposure is flagged as too low
    default: 30
    required: false
  - name: time_range
    type: duration
    label: Signup period analysed
    default: 12 w
    required: false
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a feature element in the product
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked feature element
      optional: false
  - slot: user_created_event
    kind: event
    meaning: A new user account was created
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  steps:
  - id: s1
    builds: report
    uses:
    - feature_click_event
    - user_created_event
    - session_start_event
    - target_id
    - adoption_window
    - retention_window_weeks
    - strong_lever_gap_pp
    - weak_gap_pp
    - low_exposure_share
    - time_range
    instruction: 'Create a Retention report named "Retention Lifted by Feature Adoption" for the feature identified by {feature_click_event.target_id}
      equal to {target_id}; if {target_id} is not given, use the most-clicked target_id matching the feature pattern in the
      last 30 days. Anchor on {user_created_event} and use {session_start_event} as the return event. Build weekly signup
      cohorts over {time_range}. Cohort A: users who emitted {feature_click_event} with the matching target_id within {adoption_window}
      after {user_created_event} (early adopters). Cohort B: users who did not emit {feature_click_event} with the matching
      target_id within {adoption_window} after {user_created_event} (non-adopters). Chart both retention curves overlaid in
      different colors, plus a delta line showing the absolute retention gap (A minus B) at each week. For weeks W1, W2, W4,
      W8 and W12 (up to {retention_window_weeks} weeks), show Cohort A retention rate, Cohort B retention rate, the absolute
      gap in percentage points, and the cohort sizes. Annotate: flag the week with the largest gap as the magic moment; flag
      if the W4 gap exceeds {strong_lever_gap_pp} percentage points as a strong retention lever; flag if the W12 gap is below
      {weak_gap_pp} percentage points as not retention-driving; and highlight early adopter cohort size if it is below {low_exposure_share}
      percent of the base as insufficient first-week exposure. State whether the target feature is retention-correlated.'
---

# Retention lift from a feature

Slash command: /retention-lifted-by-feature-adoption

## Step 1: Compare adopters and non adopters

Create a Retention report called "Retention Lifted by Feature Adoption".
Configuration: this recipe runs for a configurable target feature, identified by Click on.target_id (default: the most-clicked target_id matching the feature pattern in the last 30 days; user can specify).
Cohort definitions:
- Cohort A: users who emitted a Click on event with the target_id within their first 7 days after User created ("early adopters")
- Cohort B: users who did NOT emit a Click on with the target_id within their first 7 days ("non-adopters")
Anchor event: User created
Return event: Session start
Cohort granularity: Weekly (signup cohorts based on User created)
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
Taxonomy notes:
- Click on.target_id is the canonical feature handle. User created and Session start are canonical.
- Cohort A/B split is computed from the existence of a Click on event with the matching target_id within 7 days of User created.
