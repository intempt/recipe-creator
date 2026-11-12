---
frontmatter_id: enterprise-accounts
slash_command: /enterprise-accounts
description: Companies with 1,000 or more employees, alerted to enterprise sales and welcomed with a dedicated-manager email, so outreach starts the moment they qualify.
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
  summary: Flags newly qualified enterprise accounts (1,000+ employees) to sales in Slack and sends them a welcome email introducing
    a dedicated account manager.
  parameters:
  - name: employee_threshold
    type: number
    label: Minimum employee count for enterprise accounts
    default: 1000
    required: false
  - name: email_tone
    type: string
    label: Tone of the welcome email
    default: professional
    required: false
  - name: email_sentence_count
    type: number
    label: Number of sentences in the welcome email body
    default: 3
    required: false
  - name: onboarding_link
    type: string
    label: Onboarding scheduling page URL
    required: true
  requirements:
  - slot: enterprise_accounts
    kind: segment
    meaning: Accounts with 1,000 or more employees
    creatable: true
    definition: accounts where employees is at least {employee_threshold}
  - slot: employees
    kind: attribute
    meaning: The number of employees at an account
  - slot: account_name
    kind: attribute
    meaning: The name of the account
  - slot: enterprise_sales_channel
    kind: integration
    meaning: Slack channel where the enterprise sales team receives alerts
    channel: slack
  - slot: account_manager
    kind: attribute
    meaning: The dedicated account manager assigned to an account
  steps:
  - id: s1
    builds: segment
    uses:
    - employees
    - employee_threshold
    instruction: Build a segment named "Enterprise Accounts" containing accounts where {employees} is {employee_threshold}
      or more.
  - id: s2
    builds: automation
    uses:
    - s1
    - enterprise_sales_channel
    - account_name
    - employees
    instruction: For each account in "Enterprise Accounts", send a Slack message to {enterprise_sales_channel} naming the
      account {account_name} and its {employees} count, sorted so the newest accounts appear first so reps can prioritize
      outreach.
  - id: s3
    builds: email
    uses:
    - s1
    - account_manager
    - email_sentence_count
    - email_tone
    - onboarding_link
    instruction: Create a designed marketing email for the accounts in "Enterprise Accounts" welcoming them to the enterprise
      tier and introducing their {account_manager}. Use {email_sentence_count} sentences in a {email_tone} tone with no pricing
      or discount language. Include one button linking to {onboarding_link}.
---

# Enterprise accounts

Slash command: /enterprise-accounts

## Step 1: Build the enterprise list

Build a segment of accounts named "Enterprise Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 1000 or more

## Step 2: Alert enterprise sales

Generate a Slack message to the enterprise sales channel For each account in "Enterprise Accounts", name the account and its employees count, so reps can prioritize outreach to the newest ones first. Use the result of "Build the enterprise list".

## Step 3: Welcome the account

Generate a designed marketing email for the accounts in "Enterprise Accounts" welcoming them to the enterprise tier and introducing their dedicated account manager. Three sentences, professional tone, no pricing or discount language, one button linking to the onboarding scheduling page. Use the result of "Build the enterprise list".
