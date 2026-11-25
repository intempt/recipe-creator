---
frontmatter_id: campaign-performance-leaderboard
slash_command: /campaign-performance-leaderboard
description: Emails a weekly leaderboard of email campaigns from the last 90 days, ranked by attributed revenue alongside
  sends, opens, clicks and conversions.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly leaderboard of email campaigns from the last 90 days ranked by attributed revenue, with sends,
    open, click and conversion rates and flags.
  parameters:
  - name: attribution_window
    type: duration
    label: Order window after an open or click
    default: 7 d
    required: false
  - name: time_range
    type: duration
    label: Campaigns sent in the last
    default: 90 d
    required: false
  - name: top_n
    type: number
    label: Campaigns listed by revenue
    default: 10
    required: false
  - name: top_highlight_count
    type: number
    label: Campaigns listed per efficiency figure
    default: 3
    required: false
  - name: open_rate_flag_threshold
    type: number
    label: Open rate that is flagged as inflated (%)
    default: 40
    required: false
  - name: ctor_low_threshold
    type: number
    label: Click-to-open rate that is flagged as low (%)
    default: 10
    required: false
  - name: conversion_low_threshold
    type: number
    label: Conversion rate that is flagged as low (%)
    default: 0.5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: email_sent_event
    kind: event
    meaning: A marketing email was sent to a customer
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: email_opened_event
    kind: event
    meaning: A customer opened a marketing email
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: email_clicked_event
    kind: event
    meaning: A customer clicked a link in a marketing email
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - email_sent_event
    - email_opened_event
    - email_clicked_event
    - placed_order_event
    - attribution_window
    - time_range
    - top_n
    - top_highlight_count
    - open_rate_flag_threshold
    - ctor_low_threshold
    - conversion_low_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes each campaign by
      {email_sent_event.campaign_id} sent in the last {time_range} and writes, per campaign: sends ({email_sent_event} count);
      open rate (customers with {email_opened_event} / sends); click rate (customers with {email_clicked_event} / sends);
      click-to-open rate (clickers / openers); conversions (customers who did {placed_order_event} within {attribution_window}
      after opening or clicking that campaign); attributed revenue (sum of {placed_order_event.total_price} of those orders);
      revenue per send. It lists the top {top_n} campaigns by attributed revenue, and the top {top_highlight_count} by revenue
      per send and by click-to-open rate. It flags campaigns with open rate above {open_rate_flag_threshold}%, click-to-open
      below {ctor_low_threshold}%, or conversion below {conversion_low_threshold}% of sends. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Campaign performance leaderboard

Slash command: /campaign-performance-leaderboard

## Step 1: Email the weekly campaign leaderboard

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes each campaign by campaign id sent in the last 90 d and writes, per campaign: sends (email sent event count); open rate (customers with email opened event / sends); click rate (customers with email clicked event / sends); click-to-open rate (clickers / openers); conversions (customers who did placed order event within 7 d after opening or clicking that campaign); attributed revenue (sum of total price of those orders); revenue per send. It lists the top 10 campaigns by attributed revenue, and the top 3 by revenue per send and by click-to-open rate. It flags campaigns with open rate above 40%, click-to-open below 10%, or conversion below 0.5% of sends. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
