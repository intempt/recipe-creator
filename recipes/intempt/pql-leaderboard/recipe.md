---
frontmatter_id: pql-leaderboard
slash_command: /pql-leaderboard
description: Builds a segment of free and trial users with strong product use, scores them, and emails sales a weekly leaderboard
  with contact details and accounts to prioritize.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds the product qualified lead segment and a PQL score, and emails sales a weekly leaderboard of top PQLs, PQL-heavy
    accounts and PQL conversion.
  parameters:
  - name: window
    type: duration
    label: PQL rolling window
    default: 14 d
    required: false
  - name: min_sessions
    type: number
    label: Minimum distinct session days
    default: 3
    required: false
  - name: min_goal_completions
    type: number
    label: Minimum activation journey goal completions
    default: 1
    required: false
  - name: min_core_clicks
    type: number
    label: Minimum clicks on core feature targets
    default: 10
    required: false
  - name: core_target_pattern
    type: text
    label: Core feature target id pattern
    default: core-feature*
    required: false
  - name: account_pqa_threshold
    type: number
    label: PQL count at one account that marks a PQA
    default: 3
    required: false
  - name: leaderboard_size
    type: number
    label: PQLs listed in the weekly email
    default: 20
    required: false
  - name: benchmark_low
    type: number
    label: Low PQL-to-paid conversion benchmark (%)
    default: 10
    required: false
  - name: benchmark_healthy_low
    type: number
    label: Healthy PQL-to-paid conversion lower bound (%)
    default: 15
    required: false
  - name: benchmark_healthy_high
    type: number
    label: Healthy PQL-to-paid conversion upper bound (%)
    default: 30
    required: false
  - name: benchmark_high
    type: number
    label: High PQL-to-paid conversion benchmark (%)
    default: 35
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_event
    kind: event
    meaning: A user started a session in the product
  - slot: journey_goal_event
    kind: event
    meaning: A user completed a goal in the activation journey
  - slot: click_event
    kind: event
    meaning: A user clicked an element in the product
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: subscription_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: trial_end
      type: date
      meaning: Trial end date; empty means a paid subscription
      optional: false
  - slot: user_account
    kind: attribute
    meaning: The account (company) a user belongs to, used to group users into accounts
  steps:
  - id: s1
    builds: segment
    uses:
    - session_event
    - journey_goal_event
    - click_event
    - subscription_event
    - window
    - min_sessions
    - min_goal_completions
    - min_core_clicks
    - core_target_pattern
    instruction: 'Build a new segment of users named "Product Qualified Leads". A user is in it when all of these are true:
      they never did {subscription_event} with {subscription_event.trial_end} empty (not paying); they did {session_event}
      on {min_sessions} or more different days in the last {window}; they did {journey_goal_event} {min_goal_completions}
      or more times in the last {window}; they did {click_event} with {click_event.target_id} matching {core_target_pattern}
      {min_core_clicks} or more times in the last {window}.'
  - id: s2
    builds: attribute
    uses:
    - session_event
    - journey_goal_event
    - click_event
    - window
    - core_target_pattern
    instruction: 'Build a computed user attribute named "PQL score", a number from 0 to 100: 5 x the number of different days
      the user did {session_event} in the last {window}, plus 15 x the number of {journey_goal_event} in the last {window},
      plus 1 x the number of {click_event} with {click_event.target_id} matching {core_target_pattern} in the last {window},
      capped at 100.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - subscription_event
    - user_account
    - account_pqa_threshold
    - leaderboard_size
    - benchmark_low
    - benchmark_healthy_low
    - benchmark_healthy_high
    - benchmark_high
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the
      segment from "Find product qualified leads" and writes: the {leaderboard_size} users with the highest attribute from
      "Score each lead", each with name, email, {user_account} and score; the number of users in the segment now and 7 days
      ago; accounts ({user_account}) with {account_pqa_threshold} or more users in it; the % of users in it 30 days ago who
      since did {subscription_event} with {subscription_event.trial_end} empty (PQL conversion); the most common behavior
      among them. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. The email
      reads the conversion as healthy between {benchmark_healthy_low}% and {benchmark_healthy_high}%, too lenient under {benchmark_low}%
      and too strict over {benchmark_high}%. Nothing else is sent.'
---

# Product qualified lead leaderboard

Slash command: /pql-leaderboard

## Step 1: Find product qualified leads

Build a new segment of users named "Product Qualified Leads". A user is in it when all of these are true: they never did subscription event with trial end empty (not paying); they did session event on 3 or more different days in the last 14 d; they did journey goal event 1 or more times in the last 14 d; they did click event with target id matching core-feature* 10 or more times in the last 14 d.

## Step 2: Score each lead

Build a computed user attribute named "PQL score", a number from 0 to 100: 5 x the number of different days the user did session event in the last 14 d, plus 15 x the number of journey goal event in the last 14 d, plus 1 x the number of click event with target id matching core-feature* in the last 14 d, capped at 100.

## Step 3: Email the weekly PQL leaderboard

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users in the segment from "Find product qualified leads" and writes: the 20 users with the highest attribute from "Score each lead", each with name, email, user account and score; the number of users in the segment now and 7 days ago; accounts (user account) with 3 or more users in it; the % of users in it 30 days ago who since did subscription event with trial end empty (PQL conversion); the most common behavior among them. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email reads the conversion as healthy between 15% and 30%, too lenient under 10% and too strict over 35%. Nothing else is sent.
