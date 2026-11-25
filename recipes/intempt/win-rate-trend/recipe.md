---
frontmatter_id: win-rate-trend
slash_command: /win-rate-trend
description: 'Emails a monthly win rate digest: win rate by month, the rolling 90 day win rate, year-over-year change and
  win rate by lead source, with a warning on sharp drops.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a monthly digest of win rate by month, the rolling win rate, the year-over-year change and win rate by lead
    source, flagging sharp drops.
  parameters:
  - name: time_range
    type: duration
    label: Time range to chart
    default: 18 mo
    required: false
  - name: rolling_window
    type: duration
    label: Rolling window for trend line
    default: 90 d
    required: false
  - name: top_sources
    type: number
    label: Number of top sources to break down
    default: 5
    required: false
  - name: acute_drop_points
    type: number
    label: Acute monthly drop threshold (percentage points)
    default: 5
    required: false
  - name: comparison_months
    type: number
    label: Trailing months for drop baseline
    default: 3
    required: false
  - name: decline_periods
    type: number
    label: Consecutive declining periods that flag a durable trend
    default: 3
    required: false
  - name: source_divergence_points
    type: number
    label: Source divergence threshold (percentage points)
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked as won
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
    - name: primary_user_id
      type: string
      meaning: Primary user linked to the deal
      optional: false
    - name: owner_id
      type: string
      meaning: Deal owner
      optional: true
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked as lost
    properties:
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
    - name: primary_user_id
      type: string
      meaning: Primary user linked to the deal
      optional: false
    - name: owner_id
      type: string
      meaning: Deal owner
      optional: true
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: currency
      type: string
      meaning: Deal currency
      optional: true
  - slot: user_utm_source
    kind: attribute
    meaning: The UTM source attribute on users used for lead source attribution
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_won_event
    - deal_lost_event
    - user_utm_source
    - time_range
    - rolling_window
    - top_sources
    - acute_drop_points
    - comparison_months
    - decline_periods
    - source_divergence_points
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes deals
      closed in the last {time_range}, where win rate is the count of {deal_won_event} divided by the count of {deal_won_event}
      plus {deal_lost_event}, by {deal_won_event.close_date} and {deal_lost_event.close_date}, and writes these figures: the
      win rate of each of the last 12 months; the win rate over the last {rolling_window}; the win rate of the last 12 months
      against the 12 months before; the win rate of the last 12 months for the {top_sources} {user_utm_source} values with
      the most closed deals, matched through {deal_won_event.primary_user_id} and {deal_lost_event.primary_user_id}, marking
      any source more than {source_divergence_points} percentage points from the overall rate. When last month''s win rate
      is more than {acute_drop_points} points below the average of the {comparison_months} months before, or the {rolling_window}
      win rate fell {decline_periods} months in a row, the email''s first line says so. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Win rate trend

Slash command: /win-rate-trend

## Step 1: Email the monthly win rate digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes deals closed in the last 18 mo, where win rate is the count of deal won event divided by the count of deal won event plus deal lost event, by close date and close date, and writes these figures: the win rate of each of the last 12 months; the win rate over the last 90 d; the win rate of the last 12 months against the 12 months before; the win rate of the last 12 months for the 5 user utm source values with the most closed deals, matched through primary user id and primary user id, marking any source more than 10 percentage points from the overall rate. When last month's win rate is more than 5 points below the average of the 3 months before, or the 90 d win rate fell 3 months in a row, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
