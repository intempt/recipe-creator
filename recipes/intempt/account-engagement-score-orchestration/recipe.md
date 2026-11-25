---
frontmatter_id: account-engagement-score-orchestration
slash_command: /account-engagement-score-orchestration
description: Scores each paying account from 0 to 100 on how its whole team uses the product, then runs a different play for
  slipping, declining and inactive accounts and alerts customer success.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores each paying account 0-100 on whole-team product use, then emails slipping, declining and inactive accounts
    and alerts customer success when a score keeps falling.
  parameters:
  - name: min_account_age
    type: duration
    label: Minimum account age before scoring applies
    default: 30 d
    required: false
  - name: green_min_score
    type: number
    label: Healthy tier minimum score
    default: 75
    required: false
  - name: yellow_min_score
    type: number
    label: Slipping tier minimum score
    default: 40
    required: false
  - name: red_min_score
    type: number
    label: Declining tier minimum score (below it the account is dormant)
    default: 15
    required: false
  - name: yellow_followup_delay
    type: duration
    label: Wait before alerting customer success on a slipping account
    default: 7 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of customer success that get the alerts
    required: true
  requirements:
  - slot: account_usage_events
    kind: event
    meaning: A user at a customer account started a session or used a feature
    properties:
    - name: user_id
      type: string
      meaning: The user who acted
      optional: false
    - name: user_role
      type: string
      meaning: The user's role at the account
      optional: true
    - name: feature_name
      type: string
      meaning: Feature used
      optional: false
  - slot: ticket_created_event
    kind: event
    meaning: A user at a customer account created a support ticket
    optional: true
  - slot: account_plan
    kind: attribute
    meaning: The account's current plan; paying when it has a value that is not free or trial
  - slot: account_seats
    kind: attribute
    meaning: Number of seats the account pays for
  - slot: account_admin
    kind: attribute
    meaning: True on the user who is the account's admin
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer account canceled its subscription
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_usage_events
    - ticket_created_event
    - account_plan
    - account_seats
    - min_account_age
    - green_min_score
    - yellow_min_score
    - red_min_score
    instruction: 'Create a computed account attribute named account_engagement_score, a number from 0 to 100, refreshed daily,
      for accounts whose {account_plan} has a value that is not free or trial and that are older than {min_account_age}. Score
      from all users at the account over the last 30 days: (a) users with {account_usage_events} divided by {account_seats};
      (b) the change in {account_usage_events} count against the 30 days before; (c) distinct {account_usage_events.feature_name}
      values used; (d) distinct {account_usage_events.user_role} values active; (e) {ticket_created_event} count, lowering
      the score. Also store the tier: green at {green_min_score} or more, yellow from {yellow_min_score}, red from {red_min_score},
      dormant below {red_min_score}.'
  - id: s2
    builds: email
    uses:
    - s1
    - account_admin
    dependsOn:
    - s1
    instruction: Write an email to the admin (the user whose {account_admin} attribute is true) of an account in the yellow
      tier of "Score each account daily". Say that a few team members are logging in less often, offer two concrete ways to
      re-engage the team (inviting colleagues, a ready-made template), and end with one call to action to book a call with
      customer success.
  - id: s3
    builds: email
    uses:
    - s1
    - account_admin
    dependsOn:
    - s1
    instruction: Write an email to the admin (the user whose {account_admin} attribute is true) of an account in the red tier
      of "Score each account daily". Say plainly that the team's use of the product has dropped, ask what changed, and end
      with one call to action to book a 15-minute call with customer success.
  - id: s4
    builds: email
    uses:
    - s1
    - account_admin
    dependsOn:
    - s1
    instruction: Write an email to the admin (the user whose {account_admin} attribute is true) of an account in the dormant
      tier of "Score each account daily". Say it has been a while, list what is new in the product since then, and end with
      one call to action to restart with a short guided setup.
  - id: s5
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - s4
    - account_admin
    - subscription_canceled_event
    - yellow_followup_delay
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    - s4
    instruction: Build an automation that runs every day at 09:00 on a schedule over accounts whose tier from "Score each
      account daily" changed since the day before. When the new tier is yellow it sends the email from "Write the slipping-account
      email" to the account's admin, waits {yellow_followup_delay}, and if the tier is still yellow or lower emails {alert_recipients}
      the account name, score and tier. When the new tier is red it sends the email from "Write the declining-account email"
      to the admin and emails {alert_recipients} the account name, score and tier the same day. When the new tier is dormant
      it sends the email from "Write the dormant-account email" to the admin. An account that did {subscription_canceled_event}
      gets nothing.
---

# Account engagement scoring and plays

Slash command: /account-engagement-score-orchestration

## Step 1: Score each account daily

Create a computed account attribute named account_engagement_score, a number from 0 to 100, refreshed daily, for accounts whose account plan has a value that is not free or trial and that are older than 30 d. Score from all users at the account over the last 30 days: (a) users with account usage events divided by account seats; (b) the change in account usage events count against the 30 days before; (c) distinct feature name values used; (d) distinct user role values active; (e) ticket created event count, lowering the score. Also store the tier: green at 75 or more, yellow from 40, red from 15, dormant below 15.

## Step 2: Write the slipping-account email

Write an email to the admin (the user whose account admin attribute is true) of an account in the yellow tier of "Score each account daily". Say that a few team members are logging in less often, offer two concrete ways to re-engage the team (inviting colleagues, a ready-made template), and end with one call to action to book a call with customer success.

## Step 3: Write the declining-account email

Write an email to the admin (the user whose account admin attribute is true) of an account in the red tier of "Score each account daily". Say plainly that the team's use of the product has dropped, ask what changed, and end with one call to action to book a 15-minute call with customer success.

## Step 4: Write the dormant-account email

Write an email to the admin (the user whose account admin attribute is true) of an account in the dormant tier of "Score each account daily". Say it has been a while, list what is new in the product since then, and end with one call to action to restart with a short guided setup.

## Step 5: Run the play for each tier

Build an automation that runs every day at 09:00 on a schedule over accounts whose tier from "Score each account daily" changed since the day before. When the new tier is yellow it sends the email from "Write the slipping-account email" to the account's admin, waits 7 d, and if the tier is still yellow or lower emails the email addresses of customer success that get the alerts the account name, score and tier. When the new tier is red it sends the email from "Write the declining-account email" to the admin and emails the email addresses of customer success that get the alerts the account name, score and tier the same day. When the new tier is dormant it sends the email from "Write the dormant-account email" to the admin. An account that did subscription canceled event gets nothing.
