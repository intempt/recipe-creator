---
frontmatter_id: usage-spike-expansion-play
slash_command: /usage-spike-expansion-play
description: 'Scores paying accounts on usage growth, finds the ones outgrowing their plan, and runs an expansion play: an
  email to the champion, an email to the budget holder and an alert to the account team when no deal opens.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Scores paying accounts for expansion, finds those outgrowing their plan, and emails the champion and budget holder,
    alerting the account team when no deal opens.
  parameters:
  - name: expansion_score_threshold
    type: number
    label: Expansion score that makes an account expansion-ready (0-100)
    default: 70
    required: false
  - name: usage_growth_window
    type: duration
    label: Recent window for usage growth
    default: 30 d
    required: false
  - name: growth_baseline_window
    type: duration
    label: Earlier window usage growth is compared with
    default: 90 d
    required: false
  - name: deal_lookback
    type: duration
    label: An expansion deal opened in this window keeps the account out
    default: 90 d
    required: false
  - name: buyer_email_delay
    type: duration
    label: Wait before the budget holder email
    default: 7 d
    required: false
  - name: ae_alert_delay
    type: duration
    label: Wait after the budget holder email before alerting the account team
    default: 7 d
    required: false
  - name: champion_tone
    type: enum
    label: Tone for champion emails
    default: peer-to-peer enablement
    required: false
    options:
    - peer-to-peer enablement
    - neutral
    - formal
  - name: buyer_tone
    type: enum
    label: Tone for budget holder emails
    default: business-formal, value-substantive
    required: false
    options:
    - business-formal, value-substantive
    - neutral
    - friendly
  - name: alert_recipients
    type: string
    label: Email addresses of the account team that get the alert
    required: true
  requirements:
  - slot: account_plan
    kind: attribute
    meaning: The account's current plan; paying when it has a value that is not free or trial
  - slot: account_usage_event
    kind: event
    meaning: A user at a customer account used the product
    properties:
    - name: feature
      type: string
      meaning: Feature used
      optional: false
    - name: user_id
      type: string
      meaning: Active user identifier
      optional: false
  - slot: expansion_deal
    kind: event
    meaning: An expansion or upgrade deal was opened for an account
  - slot: upgrade_completed
    kind: event
    meaning: An account upgraded its plan
    optional: true
  - slot: champion_user
    kind: attribute
    meaning: True on the user who is the account's most active user (the champion)
  - slot: budget_holder_contact
    kind: attribute
    meaning: True on the user who is the account's economic buyer (admin, manager or finance owner)
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_plan
    - account_usage_event
    - usage_growth_window
    - growth_baseline_window
    instruction: 'Create a computed account attribute named expansion_signal_score, a number from 0 to 100, for accounts whose
      {account_plan} has a value that is not free or trial. Score from: (a) growth in distinct {account_usage_event.user_id}
      in the last {usage_growth_window} against the {growth_baseline_window} before; (b) growth in distinct {account_usage_event.feature}
      values per active user over the same windows; (c) the share of the account''s users active in the last {usage_growth_window}.
      Also store the strongest signal as user-growth, feature-depth or seat-coverage.'
  - id: s2
    builds: segment
    uses:
    - s1
    - account_plan
    - expansion_deal
    - expansion_score_threshold
    - deal_lookback
    dependsOn:
    - s1
    instruction: 'Build a new segment of accounts named "Expansion-Ready Accounts". An account is in it only when all of these
      are true: its {account_plan} has a value that is not free or trial; its expansion_signal_score from "Score the expansion
      signals" is {expansion_score_threshold} or more; none of its users did {expansion_deal} in the last {deal_lookback}.'
  - id: s3
    builds: email
    uses:
    - s1
    - champion_user
    - champion_tone
    dependsOn:
    - s1
    instruction: 'Write an email to the champion, the user whose {champion_user} attribute is true, at an account outgrowing
      its plan. Tone: {champion_tone}; the reader should feel recognised, not pitched. Open with the account''s strongest
      signal from "Score the expansion signals" (its team is growing, it uses the product more deeply, or most of its seats
      are active), say what teams at this stage use next on the higher plan, and end with one link to compare plans.'
  - id: s4
    builds: email
    uses:
    - s1
    - budget_holder_contact
    - buyer_tone
    dependsOn:
    - s1
    instruction: 'Write an email to the budget holder, the user whose {budget_holder_contact} attribute is true, at an account
      outgrowing its plan; they often do not use the product day to day. Tone: {buyer_tone}. Summarise the value the team
      got, citing the strongest signal from "Score the expansion signals", set out what the higher plan adds and why it pays
      at their usage, and end with one call to action to book a call with their account manager.'
  - id: s5
    builds: automation
    uses:
    - s2
    - s3
    - s4
    - expansion_deal
    - upgrade_completed
    - buyer_email_delay
    - ae_alert_delay
    - alert_recipients
    dependsOn:
    - s2
    - s3
    - s4
    instruction: Build an automation that starts when an account enters the segment from "Find accounts outgrowing the plan".
      It sends the email from "Write to the champion" to the account's champion; waits {buyer_email_delay}; sends the email
      from "Write to the budget holder" to the account's budget holder; waits {ae_alert_delay}; then, if no user at the account
      did {expansion_deal} or {upgrade_completed} since entry, emails {alert_recipients} the account name, its expansion_signal_score,
      its strongest signal and the two contacts. The account leaves the automation when any of its users does {expansion_deal}
      or {upgrade_completed}, or when it leaves the segment.
---

# Expansion play on a usage spike

Slash command: /usage-spike-expansion-play

## Step 1: Score the expansion signals

Create a computed account attribute named expansion_signal_score, a number from 0 to 100, for accounts whose account plan has a value that is not free or trial. Score from: (a) growth in distinct user id in the last 30 d against the 90 d before; (b) growth in distinct feature values per active user over the same windows; (c) the share of the account's users active in the last 30 d. Also store the strongest signal as user-growth, feature-depth or seat-coverage.

## Step 2: Find accounts outgrowing the plan

Build a new segment of accounts named "Expansion-Ready Accounts". An account is in it only when all of these are true: its account plan has a value that is not free or trial; its expansion_signal_score from "Score the expansion signals" is 70 or more; none of its users did expansion deal in the last 90 d.

## Step 3: Write to the champion

Write an email to the champion, the user whose champion user attribute is true, at an account outgrowing its plan. Tone: peer-to-peer enablement; the reader should feel recognised, not pitched. Open with the account's strongest signal from "Score the expansion signals" (its team is growing, it uses the product more deeply, or most of its seats are active), say what teams at this stage use next on the higher plan, and end with one link to compare plans.

## Step 4: Write to the budget holder

Write an email to the budget holder, the user whose budget holder contact attribute is true, at an account outgrowing its plan; they often do not use the product day to day. Tone: business-formal, value-substantive. Summarise the value the team got, citing the strongest signal from "Score the expansion signals", set out what the higher plan adds and why it pays at their usage, and end with one call to action to book a call with their account manager.

## Step 5: Work the account over two weeks

Build an automation that starts when an account enters the segment from "Find accounts outgrowing the plan". It sends the email from "Write to the champion" to the account's champion; waits 7 d; sends the email from "Write to the budget holder" to the account's budget holder; waits 7 d; then, if no user at the account did expansion deal or upgrade completed since entry, emails the email addresses of the account team that get the alert the account name, its expansion_signal_score, its strongest signal and the two contacts. The account leaves the automation when any of its users does expansion deal or upgrade completed, or when it leaves the segment.
