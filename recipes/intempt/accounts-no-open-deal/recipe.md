---
frontmatter_id: accounts-no-open-deal
slash_command: /accounts-no-open-deal
description: Established accounts whose users log in constantly, checked in on by email and flagged to account executives to review for expansion whitespace.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Finds established accounts with heavy user login activity, sends them a helpful check-in email, and emails the
    account executives a list of these accounts to review for expansion.
  parameters:
  - name: employees_min
    type: number
    label: Minimum employees count for an account
    default: 50
    required: false
  - name: session_min_count
    type: number
    label: Minimum session starts across account users
    default: 5
    required: false
  - name: activity_window
    type: duration
    label: Activity lookback window
    default: 30 d
    required: false
  - name: checkin_tone
    type: enum
    label: Tone of the check-in email
    default: consultative
    required: false
    options:
    - consultative
    - friendly
    - formal
  - name: call_booking_url
    type: string
    label: Call-booking page link for the email button
    default: <UNKNOWN>
    required: true
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at an account
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  - slot: expansion_whitespace_accounts
    kind: segment
    meaning: ''
    creatable: true
    definition: accounts where {account_employees} is at least {employees_min} and users in the account did {session_start}
      at least {session_min_count} times in the last {activity_window}
  - slot: account_executives_list
    kind: integration
    meaning: A distribution list reaching the account executives
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - account_employees
    - session_start
    - employees_min
    - session_min_count
    - activity_window
    instruction: 'Build a segment of accounts named "Expansion Whitespace Accounts". An account is in the segment only when
      all of these are true: its {account_employees} is {employees_min} or more; and the users in the account together did
      {session_start} {session_min_count} or more times in the last {activity_window}.'
  - id: s2
    builds: email
    uses:
    - expansion_whitespace_accounts
    - s1
    - checkin_tone
    - call_booking_url
    instruction: Generate a designed marketing email for the accounts in "Build the whitespace list" checking in on how the
      team is using the product and surfacing one feature they may not have tried yet. Three sentences, {checkin_tone} tone,
      no pricing language, one button linking to {call_booking_url}.
  - id: s3
    builds: email_plain
    uses:
    - account_executives_list
    - account_employees
    - s1
    instruction: Generate a plain-text email to {account_executives_list}. For each account in "Build the whitespace list",
      name the account and its {account_employees} count, so they can review each one for expansion opportunity.
---

# Expansion whitespace accounts

Slash command: /accounts-no-open-deal

## Step 1: Build the whitespace list

Build a segment of accounts named "Expansion Whitespace Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- the users in the account together did the Session start event 5 or more times in the last 30 days

## Step 2: Send a value check-in

Generate a designed marketing email for the accounts in "Expansion Whitespace Accounts" checking in on how the team is using the product and surfacing one feature they may not have tried yet. Three sentences, consultative and helpful tone, no pricing language, one button linking to a call-booking page. Use the result of "Build the whitespace list".

## Step 3: Flag to account executives

Generate a plain-text email to the account executive distribution list For each account in "Expansion Whitespace Accounts", name the account and its employees count, so they can review each one for expansion opportunity. Use the result of "Build the whitespace list".
