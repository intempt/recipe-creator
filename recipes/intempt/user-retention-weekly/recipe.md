---
frontmatter_id: user-retention-weekly
slash_command: /user-retention-weekly
description: Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which acquisition sources hold up best.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows the share of each week's new signups still returning at weeks 1, 4 and 12, broken down by acquisition source
    to find the best-retaining channels.
  parameters:
  - name: cohort_window
    type: duration
    label: Lookback window for signup cohorts
    default: 12 w
    required: false
  - name: w1_benchmark
    type: number
    label: W1 retention benchmark (%)
    default: 40
    required: false
  - name: w4_benchmark
    type: number
    label: W4 retention benchmark (%)
    default: 25
    required: false
  - name: w12_benchmark
    type: number
    label: W12 retention benchmark (%)
    default: 15
    required: false
  - name: w1_drop_threshold
    type: number
    label: Flag W1 drop vs prior cohort (percentage points)
    default: 5
    required: false
  - name: compare_period
    type: enum
    label: Comparison period
    default: previous_period
    required: false
    options:
    - previous_period
    - none
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created (signup)
    properties:
    - name: utm_source
      type: string
      meaning: Acquisition source of the user at first touch
      optional: true
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
  - slot: acquisition_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source (acquisition source)
  steps:
  - id: s1
    builds: report
    uses:
    - signup_event
    - session_event
    - acquisition_source_attribute
    - cohort_window
    - compare_period
    - w1_benchmark
    - w4_benchmark
    - w12_benchmark
    - w1_drop_threshold
    instruction: 'Create a retention report named "Weekly User Retention". Anchor event: {signup_event}. Return event: {session_event}.
      Cohort granularity: weekly. Time range: last {cohort_window}, requiring cohorts to have completed the full 12-week return
      window where possible. Breakdown by {acquisition_source_attribute}. Comparison: {compare_period}. Chart: retention curve
      with one line per cohort, plus a cohort table with W1, W4 and W12 columns. Add horizontal benchmark lines at W1 {w1_benchmark}%,
      W4 {w4_benchmark}% and W12 {w12_benchmark}%. Flag any cohort whose W1 retention dropped more than {w1_drop_threshold}
      percentage points versus the prior cohort. Highlight the acquisition source with the highest W12 retention. State whether
      the retention curves are flattening into a stable plateau (good) or continuously decaying (bad, no stable user base
      forming). Surface the source-by-source retention gap at W4, showing the point by which most low-quality signups have
      churned.'
---

# Weekly user retention

Slash command: /user-retention-weekly

## Step 1: Track weekly signup cohorts

Create a Retention report called "Weekly User Retention".
Anchor event: User created
Return event: Session start
Cohort granularity: Weekly
Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
Breakdown: By Users.UTM source (acquisition source)
Compare: Previous period (prior 12 weeks of cohorts)
Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns
Annotations:
- Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
- Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
- Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
- Identify whether retention curves are flattening over time (good (natural retention forming a plateau) or continuously decaying (bad) no stable user base forming).
Surface the source-by-source retention gap at W4: the moment by which most low-quality signups have churned out.
Taxonomy notes:
- User created and Session start are canonical. Users.UTM source is the canonical first-touch attribute.
