---
frontmatter_id: plg-sales-handoff-dashboard
slash_command: /plg-sales-handoff-dashboard
description: Finds free and trial users showing strong buying intent and emails sales a weekday morning list of them, with
  the accounts behind them, paywall views by feature and free-to-paid conversion.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
  - media-entertainment
portable:
  summary: Builds a segment of free users with buying intent and emails sales a weekday morning list of them, the accounts
    with several of them, and free-to-paid conversion.
  parameters:
  - name: intentWindow
    type: duration
    label: Window for intent signals
    default: 7 d
    required: false
  - name: minSessions
    type: number
    label: Sessions in the window that count as active
    default: 5
    required: false
  - name: pqaMinPqls
    type: number
    label: Intent users that make an account worth calling
    default: 3
    required: false
  - name: topUserCount
    type: number
    label: Users listed each morning
    default: 20
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: paywall_viewed_event
    kind: event
    meaning: A user on a free plan viewed the pricing page or was shown a paywall
    properties:
    - name: feature
      type: string
      meaning: Feature behind the paywall
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A user started a paid subscription
  - slot: plan_attribute
    kind: attribute
    meaning: The user's current plan, such as free, trial or a paid plan
  - slot: account_attribute
    kind: attribute
    meaning: The account (company) the user belongs to
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - paywall_viewed_event
    - subscription_started_event
    - plan_attribute
    - intentWindow
    - minSessions
    instruction: 'Build a new segment of users named "Free Users with Buying Intent". A user is in it only when all of these
      are true: their {plan_attribute} is free or trial; they did {session_start_event} {minSessions} or more times in the
      last {intentWindow}; they did {paywall_viewed_event} 1 or more times in the last {intentWindow}; they did not do {subscription_started_event}
      at any time.'
  - id: s2
    builds: automation
    uses:
    - s1
    - session_start_event
    - paywall_viewed_event
    - subscription_started_event
    - plan_attribute
    - account_attribute
    - intentWindow
    - pqaMinPqls
    - topUserCount
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs Monday to Friday at 08:00 on a schedule. Each run it analyzes the users in
      the segment from "Find free users with buying intent" and writes these figures: the number of users in it now and 7
      days ago; the {topUserCount} users in it with the most {session_start_event} in the last {intentWindow}, each with their
      email, {account_attribute} and the features they hit in {paywall_viewed_event.feature}; the {account_attribute} values
      with {pqaMinPqls} or more users in it; the share of users who were free or trial 30 days ago who did {subscription_started_event}
      in the last 30 days; the 5 {paywall_viewed_event.feature} values most often seen in the 7 days before a {subscription_started_event}
      in the last 30 days. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Free users worth calling

Slash command: /plg-sales-handoff-dashboard

## Step 1: Find free users with buying intent

Build a new segment of users named "Free Users with Buying Intent". A user is in it only when all of these are true: their plan attribute is free or trial; they did session start event 5 or more times in the last 7 d; they did paywall viewed event 1 or more times in the last 7 d; they did not do subscription started event at any time.

## Step 2: Email sales the morning call list

Build an automation that runs Monday to Friday at 08:00 on a schedule. Each run it analyzes the users in the segment from "Find free users with buying intent" and writes these figures: the number of users in it now and 7 days ago; the 20 users in it with the most session start event in the last 7 d, each with their email, account attribute and the features they hit in feature; the account attribute values with 3 or more users in it; the share of users who were free or trial 30 days ago who did subscription started event in the last 30 days; the 5 feature values most often seen in the 7 days before a subscription started event in the last 30 days. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
