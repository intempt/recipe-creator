---
frontmatter_id: net-new-prospects
slash_command: /net-new-prospects
description: Small accounts showing their first signs of life, welcomed by email and flagged to SDRs so follow-up happens while the account is still fresh.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Welcomes small accounts showing first activity by email and alerts SDRs with account name and size so follow-up
    happens while the account is fresh.
  parameters:
  - name: employee_threshold
    type: number
    label: Maximum employees count for a small account (exclusive)
    default: 100
    required: false
  - name: activity_window
    type: duration
    label: Window for recent session starts
    default: 7 d
    required: false
  - name: welcome_tone
    type: enum
    label: Tone of the welcome email
    default: warm
    required: false
    options:
    - warm
    - professional
    - playful
  - name: sdr_distribution_list
    type: string
    label: SDR distribution list address
    default: sdr-team
    required: false
  requirements:
  - slot: net_new_account_list
    kind: segment
    meaning: Accounts with fewer than a set number of employees whose users started a session recently
    creatable: true
    definition: accounts where employees attribute is less than {employee_threshold} and the users in the account together
      did {session_start} at least once in the last {activity_window}
  - slot: session_start
    kind: event
    meaning: A customer started a session in the product
  - slot: employees_count
    kind: attribute
    meaning: Number of employees at the account
  - slot: account_name
    kind: attribute
    meaning: Name of the account
  - slot: product_feature
    kind: knowledge
    meaning: The single product feature most worth trying first, with its in-product link
  steps:
  - id: s1
    builds: segment
    uses:
    - employees_count
    - employee_threshold
    - session_start
    - activity_window
    - net_new_account_list
    instruction: Build a segment named "Net-New Prospects" of accounts where {employees_count} is less than {employee_threshold}
      and the users in the account together did {session_start} at least once in the last {activity_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - product_feature
    - welcome_tone
    instruction: Generate a designed marketing email for the accounts in "Net-New Prospects" welcoming the team and pointing
      to {product_feature}. Write three sentences in a {welcome_tone} tone with no discount language. Include exactly one
      button linking to that feature inside the product.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - account_name
    - employees_count
    - sdr_distribution_list
    instruction: Generate a plain-text email to {sdr_distribution_list}. For each account in "Net-New Prospects", name the
      account using {account_name} and its employee count using {employees_count}, so follow-up happens while the account
      is still fresh.
---

# Newly active small accounts

Slash command: /net-new-prospects

## Step 1: Build the net-new account list

Build a segment of accounts named "Net-New Prospects".
An account is in the segment only when all of these are true:
- its employees attribute is less than 100
- the users in the account together did the Session start event at least once in the last 7 days

## Step 2: Send a welcome email

Generate a designed marketing email for the accounts in "Net-New Prospects" welcoming the team and pointing to the one feature most worth trying first. Three sentences, warm and encouraging tone, no discount language, one button linking to that feature inside the product. Use the result of "Build the net-new account list".

## Step 3: Notify SDRs

Generate a plain-text email to the SDR distribution list For each account in "Net-New Prospects", name the account and its employees count, so follow-up happens while the account is still fresh. Use the result of "Build the net-new account list".
