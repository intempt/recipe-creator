---
frontmatter_id: revenue-by-channel
slash_command: /revenue-by-channel
description: Emails a weekly digest of which acquisition channels brought in revenue over the last 30 days, each channel's
  share, and how the channel mix shifted against last year.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of revenue and revenue share by acquisition channel, against the period before and the same
    period last year, with mix-shift flags.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 30 d
    required: false
  - name: top_n_channels
    type: number
    label: Channels listed before grouping the rest as Other
    default: 8
    required: false
  - name: mix_shift_threshold_pp
    type: number
    label: Year-over-year share change that counts as a mix shift (percentage points)
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: order_placed_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order value of the placed order
      optional: false
  - slot: utm_source_attribute
    kind: attribute
    meaning: The user's first-touch UTM source recorded on the user record
  steps:
  - id: s1
    builds: automation
    uses:
    - order_placed_event
    - utm_source_attribute
    - time_window
    - top_n_channels
    - mix_shift_threshold_pp
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {order_placed_event}
      in the last {time_window} by the buyer''s {utm_source_attribute} and writes these figures for the top {top_n_channels}
      channels by revenue, with the rest grouped as Other: revenue (sum of {order_placed_event.total_price}) and share of
      total revenue, next to the {time_window} before and the same {time_window} a year ago, with the year-over-year change;
      channels whose revenue grew but whose share fell; channels whose revenue fell while their share held. When a channel''s
      share moved by {mix_shift_threshold_pp} or more percentage points year over year, the email''s first line names it as
      a mix shift. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing
      else is sent.'
---

# Revenue by acquisition channel

Slash command: /revenue-by-channel

## Step 1: Email the weekly channel revenue digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes order placed event in the last 30 d by the buyer's utm source attribute and writes these figures for the top 8 channels by revenue, with the rest grouped as Other: revenue (sum of total price) and share of total revenue, next to the 30 d before and the same 30 d a year ago, with the year-over-year change; channels whose revenue grew but whose share fell; channels whose revenue fell while their share held. When a channel's share moved by 5 or more percentage points year over year, the email's first line names it as a mix shift. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
