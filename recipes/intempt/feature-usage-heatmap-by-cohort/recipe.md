---
frontmatter_id: feature-usage-heatmap-by-cohort
slash_command: /feature-usage-heatmap-by-cohort
description: Emails a monthly digest comparing feature adoption across signup cohort months, flagging features that newer
  cohorts use less and cohorts with weak onboarding.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a monthly digest of feature adoption by signup cohort month, flagging features needing re-introduction and
    cohorts with weak onboarding.
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
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
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
    builds: automation
    uses:
    - feature_click_event
    - user_first_seen
    - usage_window
    - cohort_window
    - feature_pattern
    - sticky_threshold
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes users
      whose {user_first_seen} is in the last {cohort_window}, grouped by the month of {user_first_seen} (signup cohort), and
      writes these figures: for each {feature_click_event.target_id} matching {feature_pattern}, the % of each cohort that
      did {feature_click_event} with it in the last {usage_window}; features where older cohorts adopt more than newer ones
      (likely onboarding regression); features where newer cohorts adopt more (recent improvement); features above {sticky_threshold}%
      in every cohort (universally sticky); cohorts with low adoption across most features (weak onboarding). Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Feature usage by signup cohort

Slash command: /feature-usage-heatmap-by-cohort

## Step 1: Email the monthly cohort adoption digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes users whose user first seen is in the last 6 mo, grouped by the month of user first seen (signup cohort), and writes these figures: for each target id matching the feature target_id pattern, the % of each cohort that did feature click event with it in the last 90 d; features where older cohorts adopt more than newer ones (likely onboarding regression); features where newer cohorts adopt more (recent improvement); features above 30% in every cohort (universally sticky); cohorts with low adoption across most features (weak onboarding). Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
