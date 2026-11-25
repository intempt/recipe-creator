---
frontmatter_id: enterprise-domain-signup-to-ae-task
slash_command: /enterprise-domain-signup-to-ae-task
description: Spots when a self serve signup comes from a large company, tiers the account and emails an AE the moment it qualifies
  instead of leaving it in the free funnel, with a weekly signup digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Tiers every new account by company size, emails AEs about enterprise signups with no owner, and sends a weekly
    enterprise signup digest.
  parameters:
  - name: enterprise_employee_threshold
    type: number
    label: Employees at or above which an account is enterprise
    default: 1000
    required: false
  - name: mid_market_employee_threshold
    type: number
    label: Employees at or above which an account is mid-market
    default: 100
    required: false
  - name: lookback_window
    type: duration
    label: How recent a signup counts
    default: 30 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the enterprise AE team alerted about new signups
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: signup_event
    kind: event
    meaning: A user signed up for the self-serve product
    properties:
    - name: email_domain
      type: string
      meaning: Domain of the email the user signed up with
      optional: false
  - slot: account_employee_count
    kind: attribute
    meaning: Account attribute with the employee count
  - slot: ae_assignment
    kind: attribute
    meaning: Account attribute with the AE currently assigned to the account
    optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A user booked a meeting with sales
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_employee_count
    - signup_event
    - enterprise_employee_threshold
    - mid_market_employee_threshold
    instruction: 'Build a computed attribute on accounts named "account_tier" with one of the values enterprise, mid-market,
      smb or consumer: consumer when the account''s users signed up with {signup_event.email_domain} equal to a free personal
      email domain such as outlook.com, yahoo.com, hotmail.com or icloud.com; otherwise enterprise when {account_employee_count}
      is {enterprise_employee_threshold} or more, mid-market when it is {mid_market_employee_threshold} or more, and smb below
      that or when it is empty.'
  - id: s2
    builds: segment
    uses:
    - s1
    - signup_event
    - ae_assignment
    - lookback_window
    dependsOn:
    - s1
    instruction: Build a new segment of accounts named "Enterprise signups without an AE". An account is in it when its account_tier
      attribute from "Work out the account tier" is enterprise, at least one of its users did {signup_event} in the last {lookback_window},
      and its {ae_assignment} attribute is empty.
  - id: s3
    builds: automation
    uses:
    - s2
    - signup_event
    - account_employee_count
    - alert_recipients
    dependsOn:
    - s2
    instruction: Build an automation that starts when an account enters the segment from "Find enterprise signups with no
      AE". It emails {alert_recipients} one plain-text alert with the account name, {account_employee_count}, {signup_event.email_domain},
      and the name and email of each user who did {signup_event}, asking an AE to take the account. Nothing is sent to the
      account's users.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - signup_event
    - meeting_scheduled_event
    - digest_recipients
    dependsOn:
    - s1
    - s2
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts whose users
      did {signup_event} in the last 7 days and writes these figures: the number of those accounts by account_tier from "Work
      out the account tier", with the same counts for the 7 days before; the number of accounts in the segment from "Find
      enterprise signups with no AE" now; and the number of enterprise accounts with a {meeting_scheduled_event} in the last
      30 days. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else
      is sent.'
---

# Enterprise signup to AE task

Slash command: /enterprise-domain-signup-to-ae-task

## Step 1: Work out the account tier

Build a computed attribute on accounts named "account_tier" with one of the values enterprise, mid-market, smb or consumer: consumer when the account's users signed up with email domain equal to a free personal email domain such as outlook.com, yahoo.com, hotmail.com or icloud.com; otherwise enterprise when account employee count is 1000 or more, mid-market when it is 100 or more, and smb below that or when it is empty.

## Step 2: Find enterprise signups with no AE

Build a new segment of accounts named "Enterprise signups without an AE". An account is in it when its account_tier attribute from "Work out the account tier" is enterprise, at least one of its users did signup event in the last 30 d, and its ae assignment attribute is empty.

## Step 3: Hand it to the right AE

Build an automation that starts when an account enters the segment from "Find enterprise signups with no AE". It emails the email addresses of the enterprise AE team alerted about new signups one plain-text alert with the account name, account employee count, email domain, and the name and email of each user who did signup event, asking an AE to take the account. Nothing is sent to the account's users.

## Step 4: Email the weekly enterprise digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts whose users did signup event in the last 7 days and writes these figures: the number of those accounts by account_tier from "Work out the account tier", with the same counts for the 7 days before; the number of accounts in the segment from "Find enterprise signups with no AE" now; and the number of enterprise accounts with a meeting scheduled event in the last 30 days. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
