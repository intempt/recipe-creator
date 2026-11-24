---
frontmatter_id: product-qualified-accounts
slash_command: /product-qualified-accounts
description: Accounts showing real product usage, surfaced to sales as a product-qualified-lead draft with a ready-to-send plan email drafted.
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
  summary: Surfaces accounts with real product usage to sales as a product-qualified-lead alert and drafts a plan email for
    review before sending.
  parameters:
  - name: segment_name
    type: string
    label: Name of the active account segment
    default: 'PQL: Active Accounts'
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
  - slot: active_accounts
    kind: segment
    meaning: Accounts with recent product usage
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
    - active_accounts
    - s1
    instruction: Generate a Slack message to {sales_channel}. For each account in {active_accounts}, name the account so reps
      can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active account list".
      This drafts the Slack message only; a person on the team still posts it. Take the names or addresses from the member
      list of the step that built the segment (at most 20, then how many more); never write a placeholder or ask the reader
      to paste anything in. If no member list is available, name the segment and say it can be opened in Segments.
  - id: s3
    builds: email
    uses:
    - active_accounts
    - pricing_page
    - upgrade_email_sentences
    - email_tone
    - s1
    instruction: Generate a designed marketing email for the accounts in {active_accounts} showing what the team gets from
      a plan that fits how much they use the product. Write {upgrade_email_sentences} sentences in a {email_tone} tone with
      no discount language, and include one button linking to {pricing_page}. Use the result of "Build the active account
      list". This drafts the email only; a person still sends it. If the brand kit has no logo, use the brand name as a plain
      text header; the button links to the URL chosen for this run.
---

# Product-Qualified Active Accounts

Slash command: /product-qualified-accounts

## Step 1: Build the active account list

Build a segment of accounts named "PQL: Active Accounts". An account is in the segment only when all of these are true: the users in the account together did the Session start event 3 or more times in the last 14 days.

## Step 2: Draft a sales alert

Generate a Slack message to the sales channel. List the names of the accounts in "PQL: Active Accounts", taken from the member list in the result of "Build the active account list" (at most 20, then say how many more there are). If that result carries no member list, write no placeholder and do not ask the reader to paste anything in; say instead that the accounts are saved as the segment "PQL: Active Accounts" and can be opened in Segments. Say reps can reach out to these product-qualified leads while usage is fresh. This drafts the Slack message only; a person on the team still posts it.

## Step 3: Draft a plan email

Generate a designed marketing email for the accounts in "PQL: Active Accounts" showing what the team gets from a plan that fits how much they use the product. Three sentences, confident and helpful tone, no discount language, one button linking to the pricing page URL chosen for this run. If the brand kit has no logo, use the brand name as a plain text header. Use the result of "Build the active account list". This drafts the email only; a person still sends it.
