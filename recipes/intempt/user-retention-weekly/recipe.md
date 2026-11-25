---
frontmatter_id: user-retention-weekly
slash_command: /user-retention-weekly
description: Emails a weekly digest of the share of each week's new signups still returning at weeks 1, 4 and 12, by acquisition
  source, to find the best-retaining channels.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of week 1, 4 and 12 retention for weekly signup cohorts by acquisition source, against benchmarks,
    with a flag on week-1 drops.
  parameters:
  - name: cohort_window
    type: duration
    label: Signup cohorts covered
    default: 12 w
    required: false
  - name: w1_benchmark
    type: number
    label: Week 1 retention benchmark (%)
    default: 40
    required: false
  - name: w4_benchmark
    type: number
    label: Week 4 retention benchmark (%)
    default: 25
    required: false
  - name: w12_benchmark
    type: number
    label: Week 12 retention benchmark (%)
    default: 15
    required: false
  - name: w1_drop_threshold
    type: number
    label: Week 1 drop against the prior cohort that gets flagged (percentage points)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created (signup)
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
  - slot: acquisition_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source (acquisition source)
  steps:
  - id: s1
    builds: automation
    uses:
    - signup_event
    - session_event
    - acquisition_source_attribute
    - cohort_window
    - w1_benchmark
    - w4_benchmark
    - w12_benchmark
    - w1_drop_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes weekly cohorts of
      users who did {signup_event} in the last {cohort_window} and writes these figures: for each cohort, its size and the
      share who did {session_event} in week 1, week 4 and week 12 after signup, marking weeks not yet reached; the latest
      complete week 1, week 4 and week 12 rates against {w1_benchmark}%, {w4_benchmark}% and {w12_benchmark}%; week 4 and
      week 12 retention by {acquisition_source_attribute}, naming the source with the highest week 12 retention and the gap
      between sources at week 4; whether the curves level off after week 4 or keep falling. When the latest cohort''s week
      1 rate is more than {w1_drop_threshold} percentage points below the cohort before, the email''s first line says so.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Weekly user retention

Slash command: /user-retention-weekly

## Step 1: Email the weekly retention digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes weekly cohorts of users who did signup event in the last 12 w and writes these figures: for each cohort, its size and the share who did session event in week 1, week 4 and week 12 after signup, marking weeks not yet reached; the latest complete week 1, week 4 and week 12 rates against 40%, 25% and 15%; week 4 and week 12 retention by acquisition source attribute, naming the source with the highest week 12 retention and the gap between sources at week 4; whether the curves level off after week 4 or keep falling. When the latest cohort's week 1 rate is more than 5 percentage points below the cohort before, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
