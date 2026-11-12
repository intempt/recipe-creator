---
frontmatter_id: mid-market-accounts
slash_command: /mid-market-accounts
description: Companies with 100 to 1,000 employees, flagged to inside sales and sent a getting-started email, so your mid-market motion starts automatically.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Flags mid-market accounts with 100 to 1,000 employees to inside sales and sends them a friendly getting-started
    email inviting a walkthrough booking.
  parameters:
  - name: min_employees
    type: number
    label: Minimum employee count
    default: 100
    required: false
  - name: max_employees
    type: number
    label: Maximum employee count (exclusive)
    default: 1000
    required: false
  - name: email_tone
    type: enum
    label: Email tone
    default: friendly and consultative
    required: false
    options:
    - friendly and consultative
    - formal
    - casual
  - name: email_sentence_count
    type: number
    label: Number of sentences in the email body
    default: 3
    required: false
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at a company account
  - slot: sales_ops_list
    kind: destination
    meaning: The sales ops distribution list that receives account notifications
    channel: email
  - slot: walkthrough_booking_page
    kind: knowledge
    meaning: The link to the page where prospects can book a product walkthrough
  steps:
  - id: s1
    builds: segment
    uses:
    - account_employees
    - min_employees
    - max_employees
    instruction: Build a segment named "Mid-Market Accounts" of accounts where {account_employees} is at least {min_employees}
      and {account_employees} is less than {max_employees}.
  - id: s2
    builds: email_plain
    uses:
    - s1
    - sales_ops_list
    - account_employees
    instruction: Generate a plain-text email to {sales_ops_list}. For each account in "Mid-Market Accounts", name the account
      and its {account_employees} count, ordered so the newest accounts appear first so inside sales can assign owners.
  - id: s3
    builds: email
    uses:
    - s1
    - email_tone
    - email_sentence_count
    - walkthrough_booking_page
    instruction: Generate a designed marketing email for the accounts in "Mid-Market Accounts" with a {email_tone} tone, written
      in {email_sentence_count} sentences, introducing features relevant to a growing team and inviting them to book a walkthrough.
      Do not use discount language. Include exactly one button linking to {walkthrough_booking_page}.
---

# Mid-market accounts

Slash command: /mid-market-accounts

## Step 1: Build the mid-market list

Build a segment of accounts named "Mid-Market Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 100 or more
- its employees attribute is less than 1000

## Step 2: Notify sales ops

Generate a plain-text email to the sales ops distribution list For each account in "Mid-Market Accounts", name the account and its employees count, so inside sales can assign owners to the newest accounts first. Use the result of "Build the mid-market list".

## Step 3: Send a getting-started email

Generate a designed marketing email for the accounts in "Mid-Market Accounts" introducing features relevant to a growing team and inviting them to book a walkthrough. Three sentences, friendly and consultative tone, no discount language, one button linking to the walkthrough booking page. Use the result of "Build the mid-market list".
