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
  summary: Finds established accounts with heavy login activity, writes them a check-in email, and writes the account executives
    a list of these accounts to review for expansion.
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
    required: true
  requirements:
  - slot: account_employees
    kind: attribute
    meaning: The number of employees at an account
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
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
    - s1
    - checkin_tone
    - call_booking_url
    dependsOn:
    - s1
    instruction: Generate a designed marketing email for the accounts in "Build the whitespace list" checking in on how the
      team is using the product and surfacing one feature they may not have tried yet. Three sentences, {checkin_tone} tone,
      no pricing language, one button linking to {call_booking_url}. If the brand kit has no logo, use the brand name as a
      plain text header. Every button links to a URL given for this run or named in this step; never leave a button without
      a link.
  - id: s3
    builds: email_plain
    uses:
    - account_executives_list
    - account_employees
    - s1
    dependsOn:
    - s1
    instruction: 'Generate a plain-text email to {account_executives_list}. For each account in "Build the whitespace list",
      name the account and its {account_employees} count, so they can review each one for expansion opportunity. Take names
      and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never
      write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no
      markup and no unsubscribe line.'
---

# Expansion whitespace accounts

Slash command: /accounts-no-open-deal

## Step 1: Build the whitespace list

Build a segment of accounts named "Expansion Whitespace Accounts". An account is in the segment only when all of these are true: its account employees is 50 or more; and the users in the account together did session start 5 or more times in the last 30 d.

## Step 2: Send a value check-in

Generate a designed marketing email for the accounts in "Build the whitespace list" checking in on how the team is using the product and surfacing one feature they may not have tried yet. Three sentences, consultative tone, no pricing language, one button linking to Call-booking page link for the email button. If the brand kit has no logo, use the brand name as a plain text header. Every button links to a URL given for this run or named in this step; never leave a button without a link.

## Step 3: Flag to account executives

Generate a plain-text email to account executives list. For each account in "Build the whitespace list", name the account and its account employees count, so they can review each one for expansion opportunity. Take names and addresses from the member list in the result of the step that built the list (at most 20, then how many more); never write a placeholder or ask the reader to paste anything in. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
