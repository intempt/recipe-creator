---
frontmatter_id: quota-attainment-by-rep
slash_command: /quota-attainment-by-rep
description: Emails a weekly digest of each rep's closed revenue against their quota, with attainment, pipeline coverage and
  risk flags.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of each rep's closed revenue against quota, with attainment %, pipeline coverage, top performers
    and acute-risk flags.
  parameters:
  - name: attainment_window
    type: duration
    label: Period attainment is measured over
    default: 90 d
    required: false
  - name: attainment_green_pct
    type: number
    label: Green threshold (attainment %)
    default: 100
    required: false
  - name: attainment_yellow_pct
    type: number
    label: Yellow threshold (attainment %)
    default: 80
    required: false
  - name: acute_risk_attainment_pct
    type: number
    label: Acute risk attainment threshold (%)
    default: 50
    required: false
  - name: acute_risk_coverage_ratio
    type: number
    label: Acute risk pipeline coverage ratio
    default: 2
    required: false
  - name: top_bottom_gap_multiple
    type: number
    label: Top-to-median gap multiple that triggers a flag
    default: 3
    required: false
  - name: top_revenue_reps_count
    type: number
    label: Number of top reps by absolute revenue to highlight
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked won (closed-won) by a sales rep
    properties:
    - name: owner_id
      type: string
      meaning: The rep who owns the won deal
      optional: false
    - name: amount
      type: number
      meaning: Dollar amount of the won deal
      optional: false
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal's stage was changed, recording its new stage and amount
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: The stage the deal moved into
      optional: false
    - name: amount
      type: number
      meaning: Deal amount at the time of the stage change
      optional: false
  - slot: rep_quota_attribute
    kind: attribute
    meaning: A rep's quota target amount for the attainment period, stored on the rep's user record
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_won_event
    - deal_stage_changed_event
    - rep_quota_attribute
    - attainment_window
    - attainment_green_pct
    - attainment_yellow_pct
    - acute_risk_attainment_pct
    - acute_risk_coverage_ratio
    - top_bottom_gap_multiple
    - top_revenue_reps_count
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes each rep ({deal_won_event.owner_id})
      for the last {attainment_window}, the {attainment_window} before, and the same {attainment_window} a year ago, and writes
      per rep: closed revenue, the sum of {deal_won_event.amount}; quota from {rep_quota_attribute}; attainment %, closed
      / quota; pipeline coverage, the latest {deal_stage_changed_event.amount} of each open {deal_stage_changed_event.deal_id}
      (its {deal_stage_changed_event.new_stage} not won or lost) / quota; reps ranked by attainment, with green at {attainment_green_pct}%+,
      yellow from {attainment_yellow_pct}%, red below; the top {top_revenue_reps_count} reps by closed revenue. Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. The email''s first line names any rep
      under {acute_risk_attainment_pct}% attainment with coverage under {acute_risk_coverage_ratio}x as acute risk, and it
      flags when the top rep''s attainment is {top_bottom_gap_multiple}x the median rep''s or more. Nothing else is sent.'
---

# Quota attainment by rep

Slash command: /quota-attainment-by-rep

## Step 1: Email the weekly quota attainment digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes each rep (owner id) for the last 90 d, the 90 d before, and the same 90 d a year ago, and writes per rep: closed revenue, the sum of amount; quota from rep quota attribute; attainment %, closed / quota; pipeline coverage, the latest amount of each open deal id (its new stage not won or lost) / quota; reps ranked by attainment, with green at 100%+, yellow from 80%, red below; the top 3 reps by closed revenue. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email's first line names any rep under 50% attainment with coverage under 2x as acute risk, and it flags when the top rep's attainment is 3x the median rep's or more. Nothing else is sent.
