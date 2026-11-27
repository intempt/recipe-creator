---
frontmatter_id: seat-expansion-signal-to-ae-task
slash_command: /seat-expansion-signal-to-ae-task
description: Tells the AE by email when a paying customer is running out of seats or people from their domain keep signing
  up, which is the clearest upsell signal there is, with a weekly expansion digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags paying accounts near their seat limit or with a signup spike, emails the AE team, and sends a weekly expansion-signal
    digest.
  parameters:
  - name: seat_warning_threshold
    type: number
    label: Share of plan seats in use that counts as near the limit (0 to 1)
    default: 0.8
    required: false
  - name: domain_signup_count
    type: number
    label: New signups from the account that count as a spike
    default: 3
    required: false
  - name: domain_signup_window
    type: duration
    label: Window the signup spike is counted over
    default: 14 d
    required: false
  - name: engagement_lookback
    type: duration
    label: Skip accounts an AE engaged in this window
    default: 30 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the AE team alerted about expansion signals
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: active_seats
    kind: attribute
    meaning: Account attribute with the number of seats in use
  - slot: seat_limit
    kind: attribute
    meaning: Account attribute with the number of seats on the plan
  - slot: plan
    kind: attribute
    meaning: Account attribute with the current plan, empty or free/trial when not paying
  - slot: user_signed_up
    kind: event
    meaning: A new user signed up for the product
  - slot: ae_engagement
    kind: event
    meaning: An account executive logged an engagement activity on an account
  - slot: ae_owner
    kind: attribute
    meaning: Account attribute with the name of the assigned account executive
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - active_seats
    - seat_limit
    instruction: 'Build a computed attribute on accounts named "seat_capacity_used": the account''s {active_seats} attribute
      divided by its {seat_limit} attribute, as a number rounded to two decimals. When the project has no seats-in-use attribute,
      the number of distinct users of the account who did {user_signed_up} or a session event in the last 30 days stands in
      for {active_seats} (a stand-in the reply names). Accounts with no {seat_limit} value have no value.'
  - id: s2
    builds: segment
    uses:
    - s1
    - plan
    - user_signed_up
    - ae_engagement
    - seat_warning_threshold
    - domain_signup_count
    - domain_signup_window
    - engagement_lookback
    dependsOn:
    - s1
    instruction: Build a new segment of accounts named "Seat-expansion candidates". An account is in it when its {plan} attribute
      has a value that is not free or trial, none of its users had {ae_engagement} in the last {engagement_lookback}, and
      either its seat_capacity_used attribute from "Measure how full the plan is" is {seat_warning_threshold} or more, or
      {domain_signup_count} or more of its users did {user_signed_up} in the last {domain_signup_window}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - plan
    - ae_owner
    - user_signed_up
    - domain_signup_window
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that starts when an account enters the segment from "Find accounts near a limit". It
      emails {alert_recipients} one plain-text alert with the account name, {ae_owner}, {plan}, seat_capacity_used from "Measure
      how full the plan is", and the number of its users who did {user_signed_up} in the last {domain_signup_window}, asking
      the AE to open an expansion conversation. Nothing is sent to the account's users.
  - id: s4
    builds: automation
    uses:
    - s2
    - ae_engagement
    - digest_recipients
    dependsOn:
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from
      "Find accounts near a limit" and writes these figures: accounts that entered it in the last 7 days and in the 7 days
      before; how many entered on the seat limit and how many on the signup spike; and how many accounts that entered in the
      last 30 days had {ae_engagement} since. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Seat expansion signal to AE

Slash command: /seat-expansion-signal-to-ae-task

## Step 1: Measure how full the plan is

Build a computed attribute on accounts named "seat_capacity_used": the account's active seats attribute divided by its seat limit attribute, as a number rounded to two decimals. When the project has no seats-in-use attribute, the number of distinct users of the account who did user signed up or a session event in the last 30 days stands in for active seats (a stand-in the reply names). Accounts with no seat limit value have no value.

## Step 2: Find accounts near a limit

Build a new segment of accounts named "Seat-expansion candidates". An account is in it when its plan attribute has a value that is not free or trial, none of its users had ae engagement in the last 30 d, and either its seat_capacity_used attribute from "Measure how full the plan is" is 0.8 or more, or 3 or more of its users did user signed up in the last 14 d.

## Step 3: Raise the expansion alert

Build an automation that starts when an account enters the segment from "Find accounts near a limit". It emails the email addresses of the AE team alerted about expansion signals one plain-text alert with the account name, ae owner, plan, seat_capacity_used from "Measure how full the plan is", and the number of its users who did user signed up in the last 14 d, asking the AE to open an expansion conversation. Nothing is sent to the account's users.

## Step 4: Email the weekly expansion digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the segment from "Find accounts near a limit" and writes these figures: accounts that entered it in the last 7 days and in the 7 days before; how many entered on the seat limit and how many on the signup spike; and how many accounts that entered in the last 30 days had ae engagement since. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
