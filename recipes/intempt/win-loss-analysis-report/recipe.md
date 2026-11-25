---
frontmatter_id: win-loss-analysis-report
slash_command: /win-loss-analysis-report
description: Emails a weekly digest splitting closed deals into won and lost by lead source, deal size and stage at loss,
  with win rate, revenue and flags on where to scale or fix the sales process.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of won and lost deals, win rate and revenue by lead source, deal size and stage at loss,
    with low win-rate flags.
  parameters:
  - name: lookback_period
    type: duration
    label: Window of closed deals
    default: 6 m
    required: false
  - name: win_rate_alert_threshold
    type: number
    label: Win rate below which a lead source is flagged (%)
    default: 25
    required: false
  - name: deal_size_small_max
    type: number
    label: Largest small deal
    default: 10000
    required: false
  - name: deal_size_enterprise_min
    type: number
    label: Smallest enterprise deal
    default: 50000
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won (closed-won)
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: primary_user_id
      type: string
      meaning: ID of the primary user linked to the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked as lost (closed-lost)
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: primary_user_id
      type: string
      meaning: ID of the primary user linked to the deal
      optional: false
    - name: previous_stage
      type: string
      meaning: Deal stage immediately before it was lost
      optional: false
  - slot: user_utm_source
    kind: attribute
    meaning: The UTM source recorded on a user, used as lead source attribution
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_won_event
    - deal_lost_event
    - user_utm_source
    - lookback_period
    - win_rate_alert_threshold
    - deal_size_small_max
    - deal_size_enterprise_min
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {deal_won_event}
      and {deal_lost_event} in the last {lookback_period} and writes these figures: deals won, deals lost, win rate (won divided
      by won plus lost), revenue won (sum of {deal_won_event.amount}) and revenue lost (sum of {deal_lost_event.amount}),
      next to the {lookback_period} before; the same figures by lead source, the {user_utm_source} of the deal''s primary
      user ({deal_won_event.primary_user_id} or {deal_lost_event.primary_user_id}); win rate by deal size: small (up to {deal_size_small_max}),
      mid and enterprise (from {deal_size_enterprise_min}); lost deals and revenue by {deal_lost_event.previous_stage}. When
      a lead source''s win rate is below {win_rate_alert_threshold}%, the email''s first line names it. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Win loss analysis

Slash command: /win-loss-analysis-report

## Step 1: Email the weekly win-loss digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes deal won event and deal lost event in the last 6 m and writes these figures: deals won, deals lost, win rate (won divided by won plus lost), revenue won (sum of amount) and revenue lost (sum of amount), next to the 6 m before; the same figures by lead source, the user utm source of the deal's primary user (primary user id or primary user id); win rate by deal size: small (up to 10000), mid and enterprise (from 50000); lost deals and revenue by previous stage. When a lead source's win rate is below 25%, the email's first line names it. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
