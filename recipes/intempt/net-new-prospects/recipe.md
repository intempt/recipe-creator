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
    instruction: Build a new segment named "Net-New Prospects" of accounts where {employees_count} is less than {employee_threshold}
      and the users in the account together did {session_start} at least once in the last {activity_window}.
  - id: s2
    builds: email
    uses:
    - s1
    - product_feature
    - welcome_tone
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the accounts in "Net-New Prospects" welcoming the team and pointing
      to {product_feature}. Write three sentences in a {welcome_tone} tone with no discount language. Include exactly one
      button linking to that feature inside the product. If the brand kit has no logo, use the brand name as a plain text
      header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - account_name
    - employees_count
    - sdr_distribution_list
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to {sdr_distribution_list}. For each account in "Net-New Prospects", name the
      account using {account_name} and its employee count using {employees_count}, so follow-up happens while the account
      is still fresh. Take names and addresses from the member list in the result of the step that built the list (at most
      20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain
      text only: no HTML tags, no markup and no unsubscribe line.'
---

# Newly active small accounts

Slash command: /net-new-prospects

## Step 1: Build the net-new account list

Build a new segment named "Net-New Prospects" of accounts where employees count is less than 100 and the users in the account together did session start at least once in the last 7 d.

## Step 2: Send a welcome email

Generate a designed marketing email for the accounts in "Net-New Prospects" welcoming the team and pointing to product feature. Write three sentences in a warm tone with no discount language. Include exactly one button linking to that feature inside the product. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Notify SDRs

Generate a plain-text email to sdr-team. For each account in "Net-New Prospects", name the account using account name and its employee count using employees count, so follow-up happens while the account is still fresh. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
