---
frontmatter_id: single-threaded-accounts
slash_command: /single-threaded-accounts
description: Enterprise accounts where nobody has logged in for a month, the highest-stakes version of a churn signal, checked in on personally and flagged to the key accounts team.
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
  summary: Finds enterprise accounts with no logins for 30 days, sends each a personal check-in email from their account manager,
    and alerts the key accounts team on Slack.
  parameters:
  - name: employee_threshold
    type: number
    label: Minimum employees for an enterprise account
    default: 1000
    required: false
  - name: quiet_window
    type: duration
    label: Period with no session starts
    default: 30 d
    required: false
  - name: email_sentences
    type: number
    label: Number of sentences in the check-in email
    default: 3
    required: false
  - name: email_tone
    type: enum
    label: Tone of the check-in email
    default: warm and personal
    required: false
    options:
    - warm and personal
    - formal
    - casual
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at an account
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: key_accounts_channel
    kind: integration
    meaning: Slack workspace with the key accounts team channel
    channel: slack
  steps:
  - id: s1
    builds: segment
    uses:
    - account_employees
    - session_start
    - employee_threshold
    - quiet_window
    instruction: 'Build a segment of accounts named "Enterprise Accounts Going Quiet". An account is in the segment only when
      all of these are true: its {account_employees} is {employee_threshold} or more, and the users in the account together
      did not do {session_start} in the last {quiet_window}.'
  - id: s2
    builds: email_plain
    uses:
    - s1
    - email_sentences
    - email_tone
    instruction: For each account in "Enterprise Accounts Going Quiet", write a plain-text email as a personal note from their
      account manager. Ask how things are going and offer a quick call. Use exactly {email_sentences} sentences, a {email_tone}
      tone, no product pitch, and no discount language.
  - id: s3
    builds: slack
    uses:
    - s1
    - key_accounts_channel
    instruction: Post a message to the key accounts team channel in {key_accounts_channel}. For each account in "Enterprise
      Accounts Going Quiet", name the account and its employee count so the team can prioritize outreach before it becomes
      a renewal problem.
---

# Enterprise accounts going quiet

Slash command: /single-threaded-accounts

## Step 1: Build the quiet-enterprise list

Build a segment of accounts named "Enterprise Accounts Going Quiet".
An account is in the segment only when all of these are true:
- its employees attribute is 1000 or more
- the users in the account together did not do the Session start event in the last 30 days

## Step 2: Draft a personal check-in

Generate a plain-text email for the accounts in "Enterprise Accounts Going Quiet" written as a personal note from their account manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the quiet-enterprise list".

## Step 3: Alert the key accounts team

Generate a Slack message to the key accounts team channel For each account in "Enterprise Accounts Going Quiet", name the account and its employees count, so the team can prioritize outreach before it becomes a renewal problem. Use the result of "Build the quiet-enterprise list".
