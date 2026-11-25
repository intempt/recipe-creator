---
frontmatter_id: deal-velocity-by-stage
slash_command: /deal-velocity-by-stage
description: Emails a weekly digest of how long deals stay in each sales stage, which stage is the bottleneck, and how won
  deals' stage speed compares with lost deals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of median time in each sales stage, the bottleneck stage, stages that slowed down, and won
    versus lost deal speed.
  parameters:
  - name: lookback_window
    type: duration
    label: Window of stage changes analyzed
    default: 90 d
    required: false
  - name: comparison_window
    type: duration
    label: Earlier window it is compared with
    default: 90 d
    required: false
  - name: worsening_threshold_pct
    type: number
    label: Slowdown in a stage that gets flagged (%)
    default: 30
    required: false
  - name: won_vs_lost_speed_ratio
    type: number
    label: How many times slower lost deals must be in a stage to be flagged
    default: 2
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_stage_changed_event
    kind: event
    meaning: A deal moved from one sales stage to another
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: previous_stage
      type: string
      meaning: Stage the deal left
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal entered
      optional: false
    - name: time_in_previous_stage
      type: number
      meaning: Time the deal spent in the previous stage
      optional: true
  - slot: deal_created_event
    kind: event
    meaning: A new deal was created
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A deal was won (closed won)
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was lost (closed lost)
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_stage_changed_event
    - deal_created_event
    - deal_won_event
    - deal_lost_event
    - lookback_window
    - comparison_window
    - worsening_threshold_pct
    - won_vs_lost_speed_ratio
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {deal_stage_changed_event}
      in the last {lookback_window}, taking time in stage from {deal_stage_changed_event.time_in_previous_stage}, or else
      from the gap between successive events with the same {deal_stage_changed_event.deal_id} (for the first stage, from {deal_created_event}
      with the same deal_id), and writes these figures per {deal_stage_changed_event.previous_stage}: the median, average
      and 75th-percentile days in stage, next to the median for the {comparison_window} before; the stage with the longest
      median, called the bottleneck; each stage''s median for deals that later did {deal_won_event} and for deals that later
      did {deal_lost_event}. When a stage''s median rose by more than {worsening_threshold_pct}%, or lost deals sat in a stage
      at least {won_vs_lost_speed_ratio} times longer than won deals, the email''s first line says so. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Deal velocity by stage

Slash command: /deal-velocity-by-stage

## Step 1: Email the weekly deal velocity digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes deal stage changed event in the last 90 d, taking time in stage from time in previous stage, or else from the gap between successive events with the same deal id (for the first stage, from deal created event with the same deal_id), and writes these figures per previous stage: the median, average and 75th-percentile days in stage, next to the median for the 90 d before; the stage with the longest median, called the bottleneck; each stage's median for deals that later did deal won event and for deals that later did deal lost event. When a stage's median rose by more than 30%, or lost deals sat in a stage at least 2 times longer than won deals, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
