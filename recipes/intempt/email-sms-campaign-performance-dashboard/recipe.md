---
frontmatter_id: email-sms-campaign-performance-dashboard
slash_command: /email-sms-campaign-performance-dashboard
description: Emails a weekly ranking of every email campaign and text message template by the revenue it produced, so you
  can see which sends earn their place.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly ranking of email campaigns and text message templates by revenue per send, with open, click and
    order rates for each.
  parameters:
  - name: reportWindow
    type: duration
    label: Sends included in the ranking
    default: 30 d
    required: false
  - name: attributionWindowDays
    type: number
    label: Days after a send an order counts for it
    default: 7
    required: false
  - name: leaderboardRowLimit
    type: number
    label: Campaigns listed in the ranking
    default: 30
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: email_sent
    kind: event
    meaning: A customer was sent an email
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: email_opened
    kind: event
    meaning: A customer opened an email
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: email_clicked
    kind: event
    meaning: A customer clicked a link in an email
    properties:
    - name: campaign_id
      type: string
      meaning: Campaign the email belongs to
      optional: false
  - slot: placed_order
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total
      optional: false
  - slot: messaged_sms
    kind: event
    meaning: A customer was sent a text message
    optional: true
    properties:
    - name: template_id
      type: string
      meaning: Template of the text message
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - email_sent
    - email_opened
    - email_clicked
    - placed_order
    - messaged_sms
    - reportWindow
    - attributionWindowDays
    - leaderboardRowLimit
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes sends in the last
      {reportWindow} and writes these figures: per {email_sent.campaign_id}, the sends, open rate ({email_opened}), click
      rate ({email_clicked}), clicks per open, the orders and sum of {placed_order.total_price} by recipients within {attributionWindowDays}
      days after the send, and revenue per send; the {leaderboardRowLimit} campaigns with the highest revenue per send, ranked;
      totals of sends and revenue across all campaigns against the {reportWindow} before; per {messaged_sms.template_id},
      when {messaged_sms} exists, the sends, orders within {attributionWindowDays} days and revenue per send. Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Email and SMS campaign results

Slash command: /email-sms-campaign-performance-dashboard

## Step 1: Email the weekly campaign ranking

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes sends in the last 30 d and writes these figures: per campaign id, the sends, open rate (email opened), click rate (email clicked), clicks per open, the orders and sum of total price by recipients within 7 days after the send, and revenue per send; the 30 campaigns with the highest revenue per send, ranked; totals of sends and revenue across all campaigns against the 30 d before; per template id, when messaged sms exists, the sends, orders within 7 days and revenue per send. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
