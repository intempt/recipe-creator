---
frontmatter_id: account-engagement-score-trend
slash_command: /account-engagement-score-trend
description: Builds an engagement score on each account from its active users and click volume, and emails a weekly digest
  of the top accounts, sharp drops, fast growers and single-threaded accounts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores each account's engagement from active users and clicks, and emails a weekly digest flagging drops, growth
    and single-threaded accounts.
  parameters:
  - name: score_user_weight
    type: number
    label: Points per active user
    default: 5
    required: false
  - name: score_activity_weight
    type: number
    label: Points per click
    default: 0.1
    required: false
  - name: comparison_window
    type: duration
    label: Recent window scored
    default: 4 w
    required: false
  - name: baseline_window
    type: duration
    label: Earlier window it is compared with
    default: 8 w
    required: false
  - name: drop_threshold
    type: number
    label: Score drop that flags an account (%)
    default: 30
    required: false
  - name: growth_threshold
    type: number
    label: Score growth that flags an account (%)
    default: 50
    required: false
  - name: highlight_count
    type: number
    label: Accounts listed per figure
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: click_event
    kind: event
    meaning: A user clicked on an element in the product
  steps:
  - id: s1
    builds: attribute
    uses:
    - session_start_event
    - click_event
    - score_user_weight
    - score_activity_weight
    - comparison_window
    instruction: Build a new attribute on accounts named "engagement_score". Its value is the number of the account's users
      who did {session_start_event} in the last {comparison_window} times {score_user_weight}, plus the number of {click_event}
      events by the account's users in the last {comparison_window} times {score_activity_weight}, rounded to a whole number.
      It refreshes daily.
  - id: s2
    builds: automation
    uses:
    - s1
    - session_start_event
    - click_event
    - score_user_weight
    - score_activity_weight
    - comparison_window
    - baseline_window
    - drop_threshold
    - growth_threshold
    - highlight_count
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts by the
      attribute from "Score account engagement" and writes these figures: the {highlight_count} accounts with the highest
      score, by name; the accounts whose score over the last {comparison_window} is more than {drop_threshold}% below the
      same formula over the {baseline_window} before, by name and count; the accounts whose score grew more than {growth_threshold}%
      on that comparison, by name and count; the {highlight_count} accounts with the largest score growth against 7 days ago;
      the accounts whose users doing {session_start_event} fell over that comparison while their {click_event} count changed
      less than 10%, as single-threaded accounts. Then it emails these figures as plain-text lines, each with its window,
      to {digest_recipients}. Nothing else is sent.'
---

# Account engagement score trend

Slash command: /account-engagement-score-trend

## Step 1: Score account engagement

Build a new attribute on accounts named "engagement_score". Its value is the number of the account's users who did session start event in the last 4 w times 5, plus the number of click event events by the account's users in the last 4 w times 0.1, rounded to a whole number. It refreshes daily.

## Step 2: Email the weekly engagement digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts by the attribute from "Score account engagement" and writes these figures: the 5 accounts with the highest score, by name; the accounts whose score over the last 4 w is more than 30% below the same formula over the 8 w before, by name and count; the accounts whose score grew more than 50% on that comparison, by name and count; the 5 accounts with the largest score growth against 7 days ago; the accounts whose users doing session start event fell over that comparison while their click event count changed less than 10%, as single-threaded accounts. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
