---
frontmatter_id: pipeline-value-snapshot
slash_command: /pipeline-value-snapshot
description: Emails a weekly digest of the value of your open pipeline, summed from deal events and broken out by stage, with
  a weighted forecast and the change against 30 days ago.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly digest of open pipeline value by stage, with weighted forecast, stage concentration flags and the
    30-day change.
  parameters:
  - name: closed_stages
    type: string
    label: Deal stage names that count as closed (comma separated)
    default: won, lost, closed
    required: false
  - name: compare_window
    type: duration
    label: Comparison window for pipeline shift
    default: 30 d
    required: false
  - name: weighting_lookback
    type: duration
    label: Trailing window for historical stage win-rates
    default: 180 d
    required: false
  - name: min_closed_deals
    type: number
    label: Minimum closed deals needed to use historical win-rates
    default: 50
    required: false
  - name: fallback_early_weight
    type: number
    label: Fallback win weight for early stages (%)
    default: 10
    required: false
  - name: fallback_mid_weight
    type: number
    label: Fallback win weight for mid stages (%)
    default: 30
    required: false
  - name: fallback_late_weight
    type: number
    label: Fallback win weight for late stages (%)
    default: 70
    required: false
  - name: late_stage_threshold
    type: number
    label: Late-stage concentration flag threshold (%)
    default: 40
    required: false
  - name: early_stage_threshold
    type: number
    label: Early-stage concentration flag threshold (%)
    default: 40
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_stage_event
    kind: event
    meaning: A deal's stage was changed in the CRM
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: amount
      type: number
      meaning: Deal value amount
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved into
      optional: false
  - slot: quota_target
    kind: attribute
    meaning: A sales quota target configured for the workspace
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_stage_event
    - quota_target
    - closed_stages
    - compare_window
    - weighting_lookback
    - min_closed_deals
    - fallback_early_weight
    - fallback_mid_weight
    - fallback_late_weight
    - late_stage_threshold
    - early_stage_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it takes the latest {deal_stage_event}
      per {deal_stage_event.deal_id}; a deal is open when its {deal_stage_event.new_stage} is not one of {closed_stages}.
      It writes: open pipeline value, the sum of {deal_stage_event.amount}, in total and per stage, now and {compare_window}
      ago, with the change in $ and %; each stage''s share %; weighted forecast, each open amount times its stage''s win rate
      over the last {weighting_lookback} (when fewer than {min_closed_deals} deals closed in that time, it uses {fallback_early_weight}%
      early, {fallback_mid_weight}% mid, {fallback_late_weight}% late and says so); the largest open deal; pipeline / {quota_target}
      when it is set. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. The
      email flags a late-stage (proposal, negotiation) share above {late_stage_threshold}% or an early-stage (qualification,
      discovery) share above {early_stage_threshold}%. Nothing else is sent.'
---

# Pipeline value snapshot

Slash command: /pipeline-value-snapshot

## Step 1: Email the weekly pipeline value digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it takes the latest deal stage event per deal id; a deal is open when its new stage is not one of won, lost, closed. It writes: open pipeline value, the sum of amount, in total and per stage, now and 30 d ago, with the change in $ and %; each stage's share %; weighted forecast, each open amount times its stage's win rate over the last 180 d (when fewer than 50 deals closed in that time, it uses 10% early, 30% mid, 70% late and says so); the largest open deal; pipeline / quota target when it is set. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags a late-stage (proposal, negotiation) share above 40% or an early-stage (qualification, discovery) share above 40%. Nothing else is sent.
