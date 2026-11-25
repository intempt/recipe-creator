---
frontmatter_id: accounts-at-risk-count
slash_command: /accounts-at-risk-count
description: Flags accounts whose product use is falling, whose most active user went quiet or who raised a high-priority
  ticket, and emails a weekly at-risk count with the revenue behind it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds the at-risk accounts segment and emails a weekly digest of at-risk accounts, accounts to watch and the subscription
    revenue at risk.
  parameters:
  - name: trailingWindow
    type: duration
    label: Recent window compared
    default: 4 w
    required: false
  - name: baselineWindow
    type: duration
    label: Earlier window it is compared with
    default: 8 w
    required: false
  - name: distinctUserDropThreshold
    type: number
    label: Drop in active users that makes an account at risk (%)
    default: 30
    required: false
  - name: earlyWarningDropThreshold
    type: number
    label: Drop in active users that puts an account on the watch list (%)
    default: 10
    required: false
  - name: championInactivityWindow
    type: duration
    label: Days the most active user has been silent
    default: 14 d
    required: false
  - name: ticketLookback
    type: duration
    label: High-priority ticket lookback
    default: 30 d
    required: false
  - name: topAccountCount
    type: number
    label: At-risk accounts listed in the digest
    default: 5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the weekly digest
    required: true
  requirements:
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: ticket_created
    kind: event
    meaning: A customer created a support ticket
    properties:
    - name: priority
      type: string
      meaning: Priority level of the ticket (e.g. P1-P4 or High/Medium/Low)
      optional: false
  - slot: subscription_started
    kind: event
    meaning: A customer started or renewed a paid subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount
      optional: false
  - slot: account_tier
    kind: attribute
    meaning: Account tier such as Enterprise, Mid-Market or SMB
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start
    - ticket_created
    - trailingWindow
    - baselineWindow
    - distinctUserDropThreshold
    - championInactivityWindow
    - ticketLookback
    instruction: 'Build a new segment of accounts named "Accounts at Risk". An account is in it when any one of these is true:
      (a) the number of its users who did {session_start} in the last {trailingWindow} is at least {distinctUserDropThreshold}%
      lower than in the {baselineWindow} before that; (b) its user with the most {session_start} events in the last 30 days
      did not do {session_start} in the last {championInactivityWindow}; (c) one of its users did {ticket_created} with {ticket_created.priority}
      equal to P1 or High in the last {ticketLookback}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - session_start
    - subscription_started
    - account_tier
    - trailingWindow
    - baselineWindow
    - distinctUserDropThreshold
    - earlyWarningDropThreshold
    - topAccountCount
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the accounts in
      the segment from "Find accounts going quiet" and writes these figures: the number of accounts in it now and 7 days ago;
      the number of accounts not in it whose users doing {session_start} fell between {earlyWarningDropThreshold}% and {distinctUserDropThreshold}%
      over the last {trailingWindow} against the {baselineWindow} before, called accounts to watch; the revenue at risk, the
      sum of the latest {subscription_started.amount} of each account in the segment; the {topAccountCount} accounts in the
      segment with the highest amount, each by name; the counts split by {account_tier} when it is set. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Accounts at risk

Slash command: /accounts-at-risk-count

## Step 1: Find accounts going quiet

Build a new segment of accounts named "Accounts at Risk". An account is in it when any one of these is true: (a) the number of its users who did session start in the last 4 w is at least 30% lower than in the 8 w before that; (b) its user with the most session start events in the last 30 days did not do session start in the last 14 d; (c) one of its users did ticket created with priority equal to P1 or High in the last 30 d.

## Step 2: Email the weekly at-risk digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the accounts in the segment from "Find accounts going quiet" and writes these figures: the number of accounts in it now and 7 days ago; the number of accounts not in it whose users doing session start fell between 10% and 30% over the last 4 w against the 8 w before, called accounts to watch; the revenue at risk, the sum of the latest amount of each account in the segment; the 5 accounts in the segment with the highest amount, each by name; the counts split by account tier when it is set. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the weekly digest. Nothing else is sent.
