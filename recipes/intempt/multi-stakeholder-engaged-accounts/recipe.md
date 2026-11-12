---
frontmatter_id: multi-stakeholder-engaged-accounts
slash_command: /multi-stakeholder-engaged-accounts
description: Accounts where several people are actively using the product at once, the clearest sign a real buying committee has formed, flagged to sales and sent a resource built for teams.
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
  summary: Flags accounts where several people are actively using the product together, alerting sales in Slack and emailing
    a team-focused resource with a call-booking button.
  parameters:
  - name: session_window
    type: duration
    label: Activity window
    default: 14 d
    required: false
  - name: session_start_threshold
    type: number
    label: Minimum session start events
    default: 5
    required: false
  - name: page_view_threshold
    type: number
    label: Minimum page view events
    default: 10
    required: false
  - name: email_tone
    type: enum
    label: Email tone
    default: consultative
    required: false
    options:
    - consultative
    - friendly
    - direct
  - name: email_sentence_count
    type: number
    label: Email body sentence count
    default: 3
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page in the product
  - slot: account_employee_count
    kind: attribute
    meaning: The number of employees at an account
  - slot: account_name
    kind: attribute
    meaning: The name of an account
  - slot: multi_stakeholder_accounts
    kind: segment
    meaning: Accounts where several users together are actively using the product
    creatable: true
    definition: accounts whose users together did {session_start_event} at least {session_start_threshold} times in the last
      {session_window} and together did {page_view_event} at least {page_view_threshold} times in the last {session_window}
  - slot: sales_slack
    kind: destination
    meaning: A Slack channel the sales team reads for account alerts
    channel: slack
  - slot: team_resource_brand
    kind: brand
    meaning: The company brand used for marketing emails, including a call-booking page link
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - page_view_event
    - session_start_threshold
    - page_view_threshold
    - session_window
    instruction: 'Build a segment of accounts named "Multi-Stakeholder Engaged Accounts". An account is in the segment only
      when all of these are true: the users in the account together did {session_start_event} {session_start_threshold} or
      more times in the last {session_window}; the users in the account together did {page_view_event} {page_view_threshold}
      or more times in the last {session_window}.'
  - id: s2
    builds: slack
    uses:
    - sales_slack
    - account_name
    - account_employee_count
    - s1
    instruction: Send a Slack message to {sales_slack} for each account in "Multi-Stakeholder Engaged Accounts" naming the
      account {account_name} and its employee count {account_employee_count}, so reps know a buying committee may have formed
      and can act while interest is high. Use the result of "Build the multi-stakeholder list".
  - id: s3
    builds: email
    uses:
    - team_resource_brand
    - email_tone
    - email_sentence_count
    - s1
    instruction: Generate a designed marketing email in the {email_tone} tone for the accounts in "Multi-Stakeholder Engaged
      Accounts" offering a resource built for teams evaluating the product together. The body is {email_sentence_count} sentences,
      with no discount language, and one button linking to a call-booking page. Use the brand {team_resource_brand}. Use the
      result of "Build the multi-stakeholder list".
---

# Accounts with a buying group active

Slash command: /multi-stakeholder-engaged-accounts

## Step 1: Build the multi-stakeholder list

Build a segment of accounts named "Multi-Stakeholder Engaged Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the Session start event 5 or more times in the last 14 days
- the users in the account together did the View page event 10 or more times in the last 14 days

## Step 2: Alert sales

Generate a Slack message to the sales channel For each account in "Multi-Stakeholder Engaged Accounts", name the account and its employees count, so reps know a buying committee may have formed and can act while interest is high. Use the result of "Build the multi-stakeholder list".

## Step 3: Send a team resource

Generate a designed marketing email for the accounts in "Multi-Stakeholder Engaged Accounts" offering a resource built for teams evaluating the product together. Three sentences, consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the multi-stakeholder list".
