---
frontmatter_id: pql-multi-user-account
slash_command: /pql-multi-user-account
description: Free accounts showing real product usage, surfaced to sales as a product-qualified-lead draft with a ready-to-send upgrade email drafted.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Surfaces free accounts with real product usage to sales as a product-qualified-lead alert and drafts an upgrade
    email for review before sending.
  parameters:
  - name: segment_name
    type: string
    label: Name of the active free account segment
    default: 'PQL: Active Free Accounts'
    required: false
  - name: session_event_threshold
    type: number
    label: Minimum session starts in window
    default: 3
    required: false
  - name: usage_window
    type: duration
    label: Usage lookback window
    default: 14 d
    required: false
  - name: email_tone
    type: enum
    label: Upgrade email tone
    default: confident and helpful
    required: false
    options:
    - confident and helpful
    - friendly
    - formal
  - name: upgrade_email_sentences
    type: number
    label: Number of sentences in upgrade email
    default: 3
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: active_free_accounts
    kind: segment
    meaning: Accounts on the free plan with recent product usage
    creatable: true
    definition: accounts where the users in the account together did {session_start_event} at least {session_event_threshold}
      times in the last {usage_window}
  - slot: sales_channel
    kind: integration
    meaning: A Slack workspace channel where the sales team receives alerts
    channel: slack
  - slot: pricing_page
    kind: destination
    meaning: The public pricing page of the product
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - segment_name
    - session_event_threshold
    - usage_window
    instruction: Build a segment named {segment_name}. An account is in the segment only when the users in the account together
      did {session_start_event} {session_event_threshold} or more times in the last {usage_window}.
  - id: s2
    builds: slack
    uses:
    - sales_channel
    - active_free_accounts
    - s1
    instruction: Generate a Slack message to {sales_channel}. For each account in {active_free_accounts}, name the account
      so reps can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active-free-account
      list". This drafts the Slack message only; a person on the team still posts it.
  - id: s3
    builds: email
    uses:
    - active_free_accounts
    - pricing_page
    - upgrade_email_sentences
    - email_tone
    - s1
    instruction: Generate a designed marketing email for the accounts in {active_free_accounts} showing what the team unlocks
      on a paid plan. Write {upgrade_email_sentences} sentences in a {email_tone} tone with no discount language, and include
      one button linking to {pricing_page}. Use the result of "Build the active-free-account list". This drafts the email
      only; a person still sends it.
---

# Free accounts showing real usage

Slash command: /pql-multi-user-account

## Step 1: Build the active-free-account list

Build a segment of accounts named "PQL: Active Free Accounts". An account is in the segment only when all of these are true: the users in the account together did the Session start event 3 or more times in the last 14 days.

## Step 2: Draft a sales alert

Generate a Slack message to the sales channel. For each account in "PQL: Active Free Accounts", name the account, so reps can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active-free-account list". This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft an upgrade email

Generate a designed marketing email for the accounts in "PQL: Active Free Accounts" showing what the team unlocks on a paid plan. Three sentences, confident and helpful tone, no discount language, one button linking to the pricing page. Use the result of "Build the active-free-account list". This drafts the email only; a person still sends it.
