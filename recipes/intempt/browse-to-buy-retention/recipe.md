---
frontmatter_id: browse-to-buy-retention
slash_command: /browse-to-buy-retention
description: Measures how long first-time visitors take to place an order, by acquisition source, and emails it weekly so
  you can tell fast converting channels from slow ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of how fast first-time visitors place a first order, by acquisition source, flagging fast
    and slow converting sources.
  parameters:
  - name: time_range
    type: duration
    label: Weeks of first-visit cohorts looked at
    default: 12 w
    required: false
  - name: breakdown_top_n
    type: number
    label: Sources listed
    default: 6
    required: false
  - name: benchmark_w1_rate
    type: number
    label: Typical week-1 first-order rate (%)
    default: 5
    required: false
  - name: w12_flag_threshold
    type: number
    label: Week-12 first-order rate below which a source is flagged (%)
    default: 8
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a session on the site or app
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
  - slot: utm_source_attribute
    kind: attribute
    meaning: The UTM source that brought the user to the site
  steps:
  - id: s1
    builds: automation
    uses:
    - session_start_event
    - placed_order_event
    - utm_source_attribute
    - time_range
    - breakdown_top_n
    - benchmark_w1_rate
    - w12_flag_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users by the week
      of their first {session_start_event}, for first visits in the last {time_range} and in the {time_range} before, and
      writes these figures: the share of first-time visitors who did their first {placed_order_event} within 1, 2, 4, 8 and
      12 weeks of the first visit, for both windows; the same week-1 and week-12 shares for the top {breakdown_top_n} values
      of {utm_source_attribute} by visitors; the source with the highest week-1 share (fastest) and the one with the highest
      week-12 share (best overall); each source whose week-12 share is below {w12_flag_threshold}%, named as a browse-to-buy
      gap. When the overall week-1 share is below {benchmark_w1_rate}%, the email''s first line says so. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Browse to buy retention

Slash command: /browse-to-buy-retention

## Step 1: Track first visit to first order

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users by the week of their first session start event, for first visits in the last 12 w and in the 12 w before, and writes these figures: the share of first-time visitors who did their first placed order event within 1, 2, 4, 8 and 12 weeks of the first visit, for both windows; the same week-1 and week-12 shares for the top 6 values of utm source attribute by visitors; the source with the highest week-1 share (fastest) and the one with the highest week-12 share (best overall); each source whose week-12 share is below 8%, named as a browse-to-buy gap. When the overall week-1 share is below 5%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
