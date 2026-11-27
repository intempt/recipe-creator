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
    instruction: Build a new segment named {segment_name}. An account is in the segment only when the users in the account
      together did {session_start_event} {session_event_threshold} or more times in the last {usage_window}. When an account
      segment can't count its users' events, say why it was left out, build or reuse no people segment in its place, and rank
      the accounts by how many times their users together did {session_start_event} in the last {usage_window} (an analysis),
      keeping those at {session_event_threshold} or more.
  - id: s2
    builds: slack
    uses:
    - sales_channel
    - s1
    - usage_window
    dependsOn:
    - s1
    instruction: Generate a Slack message to {sales_channel}. For each account in the segment from "Build the active account
      list", name the account so reps can reach out to this product-qualified lead while usage is fresh. Use the result of
      "Build the active account list". This drafts the Slack message only; a person on the team still posts it. Take the names
      or addresses from the member list of the step that built the segment (at most 20, then how many more); never write a
      placeholder or ask the reader to paste anything in. When "Build the active account list" ranked accounts instead of
      building the segment, name those accounts (at most 20, then how many more) with each one's session count, and say they
      are ranked by their users' sessions in the last {usage_window} because an account segment could not count them. If no
      member list is available, name the segment and say it can be opened in Segments.
  - id: s3
    builds: email
    uses:
    - pricing_page
    - upgrade_email_sentences
    - email_tone
    - s1
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the accounts in the segment from "Build the active account list"
      showing what the team gets from a plan that fits how much they use the product. Write {upgrade_email_sentences} sentences
      in a {email_tone} tone with no discount language, and include one button linking to the pricing page address the person
      gives, else the brand's website. Use the result of "Build the active account list". This drafts the email only; a person
      still sends it. If the brand kit has no logo, use the brand name as a plain text header; the button links to the URL
      chosen for this run.
---

# Product-Qualified Active Accounts

Slash command: /product-qualified-accounts

## Step 1: Build the active account list

Build a new segment named PQL: Active Accounts. An account is in the segment only when the users in the account together did session start event 3 or more times in the last 14 d. When an account segment can't count its users' events, say why it was left out, build or reuse no people segment in its place, and rank the accounts by how many times their users together did session start event in the last 14 d (an analysis), keeping those at 3 or more.

## Step 2: Draft a sales alert

Generate a Slack message to sales channel. For each account in the segment from "Build the active account list", name the account so reps can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active account list". This drafts the Slack message only; a person on the team still posts it. Take the names or addresses from the member list of the step that built the segment (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. When "Build the active account list" ranked accounts instead of building the segment, name those accounts (at most 20, then how many more) with each one's session count, and say they are ranked by their users' sessions in the last 14 d because an account segment could not count them. If no member list is available, name the segment and say it can be opened in Segments.

## Step 3: Draft a plan email

Generate a designed marketing email for the accounts in the segment from "Build the active account list" showing what the team gets from a plan that fits how much they use the product. Write 3 sentences in a confident and helpful tone with no discount language, and include one button linking to the pricing page address the person gives, else the brand's website. Use the result of "Build the active account list". This drafts the email only; a person still sends it. If the brand kit has no logo, use the brand name as a plain text header; the button links to the URL chosen for this run.
