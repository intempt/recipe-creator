---
frontmatter_id: customer-lifecycle-distribution
slash_command: /customer-lifecycle-distribution
description: Builds Champions and At risk customer segments from the lifecycle score and emails a weekly digest of customers,
  lifetime value, recency and order value per lifecycle stage.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds Champions and At risk customer segments and emails a weekly digest of how customers spread across the six
    lifecycle stages, with value per stage and alerts.
  parameters:
  - name: window_short
    type: duration
    label: Short comparison window
    default: 30 d
    required: false
  - name: window_long
    type: duration
    label: Long comparison window
    default: 90 d
    required: false
  - name: champions_shrink_threshold
    type: number
    label: Shrink in Champions that gets flagged (%)
    default: 10
    required: false
  - name: at_risk_ltv_share_threshold
    type: number
    label: Share of lifetime value in At risk that gets flagged (%)
    default: 25
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: lifecycle_score_attribute
    kind: attribute
    meaning: 'The user''s lifecycle stage, one of: At risk, Needs attention, New customers, Promising, Regulars, Champions'
  - slot: lifetime_value_attribute
    kind: attribute
    meaning: The user's lifetime value (a number)
  - slot: days_since_last_activity_attribute
    kind: attribute
    meaning: Days since the user's last activity (a number)
  - slot: average_order_value_attribute
    kind: attribute
    meaning: The user's average order value (a number)
  steps:
  - id: s1
    builds: segment
    uses:
    - lifecycle_score_attribute
    instruction: 'Build a new segment of users named "Lifecycle Champions": users whose {lifecycle_score_attribute} is Champions.'
  - id: s2
    builds: segment
    uses:
    - lifecycle_score_attribute
    instruction: 'Build a new segment of users named "Lifecycle At Risk": users whose {lifecycle_score_attribute} is At risk.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - lifecycle_score_attribute
    - lifetime_value_attribute
    - days_since_last_activity_attribute
    - average_order_value_attribute
    - window_short
    - window_long
    - champions_shrink_threshold
    - at_risk_ltv_share_threshold
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users with a {lifecycle_score_attribute}
      and writes these figures for each of the six stages (At risk, Needs attention, New customers, Promising, Regulars, Champions):
      the number of users; the sum of {lifetime_value_attribute} and its share of the total; the average {days_since_last_activity_attribute};
      the average {average_order_value_attribute}. It also writes the size of the segment from "Find the Champions" and the
      segment from "Find the customers at risk" now, {window_short} ago and {window_long} ago. When Champions shrank by more
      than {champions_shrink_threshold}% over {window_short}, or At risk holds more than {at_risk_ltv_share_threshold}% of
      total lifetime value, the email''s first line says so. Then it emails these figures as plain-text lines, each with its
      window, to {digest_recipients}. Nothing else is sent.'
---

# Customer lifecycle distribution

Slash command: /customer-lifecycle-distribution

## Step 1: Find the Champions

Build a new segment of users named "Lifecycle Champions": users whose lifecycle score attribute is Champions.

## Step 2: Find the customers at risk

Build a new segment of users named "Lifecycle At Risk": users whose lifecycle score attribute is At risk.

## Step 3: Email the weekly lifecycle digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users with a lifecycle score attribute and writes these figures for each of the six stages (At risk, Needs attention, New customers, Promising, Regulars, Champions): the number of users; the sum of lifetime value attribute and its share of the total; the average days since last activity attribute; the average average order value attribute. It also writes the size of the segment from "Find the Champions" and the segment from "Find the customers at risk" now, 30 d ago and 90 d ago. When Champions shrank by more than 10% over 30 d, or At risk holds more than 25% of total lifetime value, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
