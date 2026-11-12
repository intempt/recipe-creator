---
frontmatter_id: icp-match-accounts
slash_command: /icp-match-accounts
description: Accounts sized right for your ideal customer profile, flagged to sales, sent an intro email, and tagged with an ICP-fit attribute so later segments and reports can reuse the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Finds accounts sized within your ideal customer profile, alerts sales in Slack, sends them a consultative intro
    email, and tags them with an ICP-fit attribute for reuse.
  parameters:
  - name: min_employees
    type: number
    label: Minimum employee count
    default: 50
    required: false
  - name: max_employees
    type: number
    label: Maximum employee count (exclusive)
    default: 500
    required: false
  - name: sales_channel
    type: string
    label: Sales Slack channel
    default: sales
    required: false
  - name: tone
    type: enum
    label: Email tone
    default: confident and consultative
    required: false
    options:
    - confident and consultative
    - friendly and casual
    - formal
  - name: cta_url_type
    type: string
    label: Call-booking page for the email button
    default: call-booking page
    required: false
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at an account's company
  - slot: icp_match_accounts
    kind: segment
    meaning: Accounts whose employee count falls within the ideal customer profile range
  - slot: sales_slack
    kind: integration
    meaning: A Slack workspace connection used to notify the sales channel
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - account_employees
    - min_employees
    - max_employees
    instruction: 'Build a segment of accounts named "ICP Match Accounts". An account is in the segment only when all of these
      are true: its {account_employees} is {min_employees} or more; its {account_employees} is less than {max_employees}.'
  - id: s2
    builds: slack
    uses:
    - s1
    - sales_slack
    - account_employees
    - sales_channel
    instruction: Generate a Slack message to the {sales_channel} channel for each account in the segment built in "Build the
      ICP list". Name the account and its {account_employees} count so reps can prioritize outreach to the newest matches
      first.
  - id: s3
    builds: email
    uses:
    - s1
    - account_employees
    - tone
    - cta_url_type
    instruction: Generate a designed marketing email for the accounts in the segment built in "Build the ICP list" introducing
      the product for a company of their size. Three sentences, {tone} tone, no discount language, one button linking to the
      {cta_url_type}.
  - id: s4
    builds: attribute
    uses:
    - s1
    instruction: Create an attribute named "icp_fit" on accounts in the segment built in "Build the ICP list", set to true.
---

# ICP-fit accounts

Slash command: /icp-match-accounts

## Step 1: Build the ICP list

Build a segment of accounts named "ICP Match Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- its employees attribute is less than 500

## Step 2: Alert sales

Generate a Slack message to the sales channel For each account in "ICP Match Accounts", name the account and its employees count, so reps can prioritize outreach to the newest matches first. Use the result of "Build the ICP list".

## Step 3: Send an intro email

Generate a designed marketing email for the accounts in "ICP Match Accounts" introducing the product for a company of their size. Three sentences, confident and consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the ICP list".

## Step 4: Tag the matched accounts

Create an attribute named "icp_fit" on accounts in "ICP Match Accounts", set to true. Use the result of "Build the ICP list".
