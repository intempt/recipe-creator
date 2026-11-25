---
frontmatter_id: saas-growth-command-center
slash_command: /saas-growth-command-center
description: 'Emails a SaaS founder a weekly digest of whether the business is growing and whether that growth is healthy:
  weekly actives, new subscription revenue, trial conversion, activation, retention and feature adoption.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: 'Emails a weekly growth digest: weekly actives, new and lost subscription revenue, trial-to-paid, activation, week-4
    retention, stickiness and feature adoption by plan.'
  parameters:
  - name: activationWindow
    type: duration
    label: Window after signup to activate
    default: 7 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: user_created_event
    kind: event
    meaning: A new user signed up
  - slot: activation_event
    kind: event
    meaning: A user reached the product's activation moment
  - slot: feature_used_event
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: amount
      type: number
      meaning: Monthly subscription amount
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: amount
      type: number
      meaning: Monthly amount of the canceled subscription
      optional: false
  - slot: plan_attribute
    kind: attribute
    meaning: The user's current plan, such as free, trial or a paid plan
  steps:
  - id: s1
    builds: automation
    uses:
    - session_start_event
    - user_created_event
    - activation_event
    - feature_used_event
    - subscription_started_event
    - subscription_canceled_event
    - plan_attribute
    - activationWindow
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes
      these figures: weekly active users (did {session_start_event} in the last 7 days) against each of the 4 weeks before;
      new subscription revenue, the sum of {subscription_started_event.amount} in the last 30 days, and lost revenue, the
      sum of {subscription_canceled_event.amount}, against the 30 days before; trial-to-paid, the share of users who did {user_created_event}
      between 30 and 60 days ago who did {subscription_started_event} within 30 days of it; activation, the share of users
      who signed up between 7 and 37 days ago who did {activation_event} within {activationWindow}; week-4 retention of users
      who signed up 4 to 5 weeks ago; stickiness, average daily actives over the last 30 days divided by the users active
      in those 30 days; the 5 {feature_used_event.feature} values used by the most weekly actives, per {plan_attribute}. When
      stickiness fell against the 30 days before while weekly actives rose, the email''s first line says so. Then it emails
      these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# SaaS growth command center

Slash command: /saas-growth-command-center

## Step 1: Email the weekly growth digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes these figures: weekly active users (did session start event in the last 7 days) against each of the 4 weeks before; new subscription revenue, the sum of amount in the last 30 days, and lost revenue, the sum of amount, against the 30 days before; trial-to-paid, the share of users who did user created event between 30 and 60 days ago who did subscription started event within 30 days of it; activation, the share of users who signed up between 7 and 37 days ago who did activation event within 7 d; week-4 retention of users who signed up 4 to 5 weeks ago; stickiness, average daily actives over the last 30 days divided by the users active in those 30 days; the 5 feature values used by the most weekly actives, per plan attribute. When stickiness fell against the 30 days before while weekly actives rose, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
