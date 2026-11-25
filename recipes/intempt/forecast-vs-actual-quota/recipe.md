---
frontmatter_id: forecast-vs-actual-quota
slash_command: /forecast-vs-actual-quota
description: Emails a weekly digest of each rep's closed-won revenue against weighted forecast and quota, with pipeline coverage,
  projected closes and forecast accuracy flags.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of closed-won revenue per rep against forecast and quota, with pipeline coverage and forecast
    accuracy flags.
  parameters:
  - name: late_stages
    type: string
    label: Deal stages counted as late stage (comma separated)
    default: proposal, negotiation, contract
    required: false
  - name: coverage_minimum
    type: number
    label: Minimum pipeline coverage ratio (x)
    default: 3
    required: false
  - name: coverage_risk_threshold
    type: number
    label: Acute pipeline coverage risk threshold (x)
    default: 2
    required: false
  - name: projection_window
    type: duration
    label: Projected close window
    default: 30 d
    required: false
  - name: forecast_accuracy_band
    type: number
    label: Forecast accuracy tolerance (%)
    default: 20
    required: false
  - name: low_attainment_streak
    type: number
    label: Months in a row below quota that get flagged
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: closed_won_deal
    kind: event
    meaning: A deal was marked closed-won
    properties:
    - name: amount
      type: number
      meaning: Value of the won deal
      optional: false
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: deal_stage_change
    kind: event
    meaning: A deal moved to a new pipeline stage with its amount at that time
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved into
      optional: false
    - name: amount
      type: number
      meaning: Deal amount at this stage change
      optional: false
    - name: close_date
      type: date
      meaning: Expected close date of the deal
      optional: true
    - name: owner_id
      type: string
      meaning: Rep who owns the deal
      optional: false
  - slot: quota_target
    kind: attribute
    meaning: Per-period dollar quota target for a rep or the workspace
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - closed_won_deal
    - deal_stage_change
    - quota_target
    - late_stages
    - coverage_minimum
    - coverage_risk_threshold
    - projection_window
    - forecast_accuracy_band
    - low_attainment_streak
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes deals per rep ({closed_won_deal.owner_id},
      {deal_stage_change.owner_id}) for the last 30 days, the 30 days before, and each 30 days over the last 120 days, and
      writes these figures: closed-won revenue, the sum of {closed_won_deal.amount}; weighted forecast, the latest {deal_stage_change.amount}
      of each open {deal_stage_change.deal_id} with {deal_stage_change.close_date} in the window times its stage''s close
      rate over the last 180 days; quota attainment %, closed-won / {quota_target}, only when {quota_target} is set; pipeline
      coverage, open pipeline / {quota_target}; projected closes, open amount in stages {late_stages} closing in the next
      {projection_window}; forecast error %, |closed-won - forecast| / closed-won. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. The email flags reps with coverage under {coverage_risk_threshold}x
      (minimum {coverage_minimum}x), forecast error above {forecast_accuracy_band}%, and {low_attainment_streak} or more 30-day
      windows in a row below quota. Nothing else is sent.'
---

# Forecast versus quota

Slash command: /forecast-vs-actual-quota

## Step 1: Email the weekly forecast and quota digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes deals per rep (owner id, owner id) for the last 30 days, the 30 days before, and each 30 days over the last 120 days, and writes these figures: closed-won revenue, the sum of amount; weighted forecast, the latest amount of each open deal id with close date in the window times its stage's close rate over the last 180 days; quota attainment %, closed-won / quota target, only when quota target is set; pipeline coverage, open pipeline / quota target; projected closes, open amount in stages proposal, negotiation, contract closing in the next 30 d; forecast error %, |closed-won - forecast| / closed-won. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags reps with coverage under 2x (minimum 3x), forecast error above 20%, and 3 or more 30-day windows in a row below quota. Nothing else is sent.
