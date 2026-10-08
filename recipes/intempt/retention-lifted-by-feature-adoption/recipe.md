---
description: Compares how long users stay when they adopt a given feature in their first week against users who never touch it.
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
  - media
---

# Retention lift from a feature

Slash command: /retention-lifted-by-feature-adoption

## Step 1: Compare adopters and non adopters

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
- Highlight the cohort size of "early adopters": if it's <30% of the base, the feature isn't getting enough first-week exposure.
Surface whether the target feature is genuinely retention-correlated. This is the canonical "magic moment" / "north-star action" analysis.
Taxonomy notes:
- click_on.target_id is the canonical feature handle. user_created and session_start are canonical.
- Cohort A/B split is computed from the existence of a click_on event with the matching target_id within 7 days of user_created.
