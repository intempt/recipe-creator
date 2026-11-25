---
frontmatter_id: analytics-foundation
slash_command: /analytics-foundation
description: 'Analyzes your tracked product events every week and emails the headline numbers: active users, top actions,
  conversion between your key steps and new-user retention, each against the week before.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a weekly digest of headline product numbers from your tracked events: active users, top actions, key-step
    conversion and new-user retention, with week-over-week change.'
  parameters:
  - name: activation_step
    type: string
    label: Event name that counts as the key conversion step
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: product_events
    kind: event
    meaning: A customer performed any tracked product action
  - slot: signup_event
    kind: event
    meaning: A new user signed up
  steps:
  - id: s1
    builds: automation
    uses:
    - product_events
    - signup_event
    - activation_step
    - digest_recipients
    instruction: 'Build an analytics automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {product_events}
      and {signup_event} and writes these figures, each for the last 7 days and the 7 days before with the change in percent:
      weekly active users (users who did any {product_events}); new users who did {signup_event}; the 5 most frequent {product_events}
      by count; the share of users who did {signup_event} between 7 and 14 days ago who then did the {activation_step} event
      within 7 days of signing up; the share of users who signed up between 28 and 35 days ago who did any {product_events}
      in the last 7 days (week-4 retention). Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Analytics foundation

Slash command: /analytics-foundation

## Step 1: Email the weekly headline numbers

Build an analytics automation that runs every Monday at 08:00 on a schedule. Each run it analyzes product events and signup event and writes these figures, each for the last 7 days and the 7 days before with the change in percent: weekly active users (users who did any product events); new users who did signup event; the 5 most frequent product events by count; the share of users who did signup event between 7 and 14 days ago who then did the the event name that counts as the key conversion step event within 7 days of signing up; the share of users who signed up between 28 and 35 days ago who did any product events in the last 7 days (week-4 retention). Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
