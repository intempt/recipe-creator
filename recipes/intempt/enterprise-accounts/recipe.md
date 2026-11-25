---
frontmatter_id: enterprise-accounts
slash_command: /enterprise-accounts
description: Companies with 1,000 or more employees, emailed to enterprise sales and welcomed with a dedicated-manager email,
  so outreach starts the moment they qualify.
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
  summary: Builds the enterprise accounts segment, alerts enterprise sales by email when an account joins it, and sends the
    account a dedicated-manager welcome email.
  parameters:
  - name: employee_threshold
    type: number
    label: Employees at or above which an account is enterprise
    default: 1000
    required: false
  - name: email_tone
    type: string
    label: Welcome email tone
    default: professional
    required: false
  - name: email_sentence_count
    type: number
    label: Sentences in the welcome email
    default: 3
    required: false
  - name: onboarding_link
    type: string
    label: Link the welcome email's button opens
    required: true
  - name: alert_recipients
    type: string
    label: Email addresses of the enterprise sales team
    required: true
  requirements:
  - slot: employees
    kind: attribute
    meaning: Account attribute with the number of employees
  - slot: account_name
    kind: attribute
    meaning: Account attribute with the account's name
  - slot: account_manager
    kind: attribute
    meaning: Account attribute with the name of the dedicated account manager
  steps:
  - id: s1
    builds: segment
    uses:
    - employees
    - employee_threshold
    instruction: Build a new segment of accounts named "Enterprise Accounts". An account is in it when its {employees} attribute
      is {employee_threshold} or more.
  - id: s2
    builds: email
    uses:
    - s1
    - account_manager
    - email_tone
    - email_sentence_count
    - onboarding_link
    dependsOn:
    - s1
    instruction: Write a designed HTML email for the users of accounts in the segment from "Build the enterprise list", welcoming
      them to the enterprise tier and introducing the dedicated manager named in their account's {account_manager} attribute.
      Use {email_sentence_count} sentences in a {email_tone} tone with no pricing or discount language, and one button linking
      to {onboarding_link}.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account_name
    - employees
    - account_manager
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that starts when an account enters the segment from "Build the enterprise list". It emails
      {alert_recipients} one plain-text alert with the account's {account_name}, {employees} and {account_manager}, then sends
      the email from "Welcome the account" to the account's users.
---

# Enterprise accounts

Slash command: /enterprise-accounts

## Step 1: Build the enterprise list

Build a new segment of accounts named "Enterprise Accounts". An account is in it when its employees attribute is 1000 or more.

## Step 2: Welcome the account

Write a designed HTML email for the users of accounts in the segment from "Build the enterprise list", welcoming them to the enterprise tier and introducing the dedicated manager named in their account's account manager attribute. Use 3 sentences in a professional tone with no pricing or discount language, and one button linking to the link the welcome email's button opens.

## Step 3: Alert enterprise sales

Build an automation that starts when an account enters the segment from "Build the enterprise list". It emails the email addresses of the enterprise sales team one plain-text alert with the account's account name, employees and account manager, then sends the email from "Welcome the account" to the account's users.
