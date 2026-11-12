---
frontmatter_id: accounts-at-churn-risk
slash_command: /accounts-at-churn-risk
description: Large paying accounts where nobody has logged in for a month, the clearest detectable churn signal, checked in on personally and flagged to the retention team before it's too late.
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
  summary: Finds large paying accounts that have gone quiet for a month, sends each a personal check-in email, and alerts
    the retention team on Slack before renewals.
  parameters:
  - name: employee_threshold
    type: number
    label: Minimum employee count for an account to be considered
    default: 100
    required: false
  - name: inactivity_window
    type: duration
    label: Period with no session start before an account is considered at risk
    default: 30 d
    required: false
  - name: retention_channel
    type: string
    label: Slack channel for the retention team
    default: retention team channel
    required: false
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The employees count stored on an account
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: at_risk_accounts
    kind: segment
    meaning: Paying accounts with large headcount where no user has started a session recently
    creatable: true
    definition: accounts where {account_employees} is at least {employee_threshold} and the users in the account did not do
      {session_start} in the last {inactivity_window}
  - slot: retention_slack
    kind: integration
    meaning: Slack workspace used to message the retention team
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - account_employees
    - session_start
    - employee_threshold
    - inactivity_window
    instruction: 'Build a segment of accounts named "Accounts At Churn Risk". An account is in the segment only when all of
      these are true: its {account_employees} is {employee_threshold} or more; and the users in the account together did not
      do {session_start} in the last {inactivity_window}.'
  - id: s2
    builds: email_plain
    uses:
    - s1
    - at_risk_accounts
    instruction: Generate a plain-text email for each account in {at_risk_accounts} written as a personal note from their
      customer success manager, asking how things are going and offering a quick call. Three sentences, warm and personal
      tone, no product pitch, no discount language.
  - id: s3
    builds: slack
    uses:
    - s1
    - at_risk_accounts
    - account_employees
    - retention_slack
    instruction: Generate a Slack message to the retention team channel. For each account in {at_risk_accounts}, name the
      account and its {account_employees} count, so the team can prioritize outreach before renewal conversations start.
---

# Paying accounts going quiet

Slash command: /accounts-at-churn-risk

## Step 1: Build the at-risk account list

Build a segment of accounts named "Accounts At Churn Risk".
An account is in the segment only when all of these are true:
- its employees attribute is 100 or more
- the users in the account together did not do the Session start event in the last 30 days

## Step 2: Draft a personal check-in

Generate a plain-text email for the accounts in "Accounts At Churn Risk" written as a personal note from their customer success manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the at-risk account list".

## Step 3: Alert the retention team

Generate a Slack message to the retention team channel For each account in "Accounts At Churn Risk", name the account and its employees count, so the team can prioritize outreach before renewal conversations start. Use the result of "Build the at-risk account list".
