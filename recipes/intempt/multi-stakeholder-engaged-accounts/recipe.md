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
    instruction: 'Build a new segment of accounts named "Multi-Stakeholder Engaged Accounts". An account is in the segment
      only when all of these are true: the users in the account together did {session_start_event} {session_start_threshold}
      or more times in the last {session_window}; the users in the account together did {page_view_event} {page_view_threshold}
      or more times in the last {session_window}.'
  - id: s2
    builds: slack
    uses:
    - sales_slack
    - account_name
    - account_employee_count
    - s1
    dependsOn:
    - s1
    instruction: Send a Slack message to {sales_slack} for each account in "Multi-Stakeholder Engaged Accounts" naming the
      account {account_name} and its employee count {account_employee_count}, so reps know a buying committee may have formed
      and can act while interest is high. Use the result of "Build the multi-stakeholder list". Take names and addresses from
      the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder
      or ask the reader to paste anything in.
  - id: s3
    builds: email
    uses:
    - team_resource_brand
    - email_tone
    - email_sentence_count
    - s1
    dependsOn:
    - s1
    instruction: Generate a designed marketing email in the {email_tone} tone for the accounts in "Multi-Stakeholder Engaged
      Accounts" offering a resource built for teams evaluating the product together. The body is {email_sentence_count} sentences,
      with no discount language, and one button linking to a call-booking page. Use the brand {team_resource_brand}. Use the
      result of "Build the multi-stakeholder list". If the brand kit has no logo, use the brand name as a plain text header.
      Every button links to a URL given for this run or named in this step; never leave a button without a link.
---

# Accounts with a buying group active

Slash command: /multi-stakeholder-engaged-accounts

## Step 1: Build the multi-stakeholder list

Build a new segment of accounts named "Multi-Stakeholder Engaged Accounts". An account is in the segment only when all of these are true: the users in the account together did session start event 5 or more times in the last 14 d; the users in the account together did page view event 10 or more times in the last 14 d.

## Step 2: Alert sales

Send a Slack message to sales slack for each account in "Multi-Stakeholder Engaged Accounts" naming the account account name and its employee count account employee count, so reps know a buying committee may have formed and can act while interest is high. Use the result of "Build the multi-stakeholder list". Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in.

## Step 3: Send a team resource

Generate a designed marketing email in the consultative tone for the accounts in "Multi-Stakeholder Engaged Accounts" offering a resource built for teams evaluating the product together. The body is 3 sentences, with no discount language, and one button linking to a call-booking page. Use the brand team resource brand. Use the result of "Build the multi-stakeholder list". If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.
