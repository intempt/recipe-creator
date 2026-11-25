---
frontmatter_id: salesforce-usage-to-opportunity
slash_command: /salesforce-usage-to-opportunity
description: Keeps active seats and usage trend on each account's open Salesforce opportunity current, so the forecast reflects
  what the account is doing rather than what was said on a call.
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
    - { value: salesforce, severity: blocking }
portable:
  summary: Computes active seats and usage trend per account and writes them to the account's open Salesforce opportunity
    every week.
  parameters:
  - name: activeWindow
    type: duration
    label: Window usage is measured over
    default: 30 d
    required: false
  requirements:
  - slot: account_usage_event
    kind: event
    meaning: A user used the product (a session or feature action)
  - slot: open_opportunity
    kind: integration
    channel: salesforce
    meaning: Salesforce account with open opportunities whose usage fields can be written
  steps:
  - id: s1
    builds: attribute
    uses:
    - account_usage_event
    - activeWindow
    instruction: 'Build a computed attribute on accounts named "usage_active_seats": the number of the account''s users who
      did {account_usage_event} at least once in the last {activeWindow}.'
  - id: s2
    builds: attribute
    uses:
    - account_usage_event
    - activeWindow
    instruction: 'Build a computed attribute on accounts named "usage_trend" with one of the values growing, flat or declining:
      compare the account''s count of {account_usage_event} in the last {activeWindow} with the {activeWindow} before that;
      growing when it is 10% or more higher, declining when it is 10% or more lower, flat otherwise.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - open_opportunity
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that runs every Monday at 06:00 on a schedule. For each account with an open opportunity
      in {open_opportunity}, it writes usage_active_seats from "Count active seats" and usage_trend from "Read the usage trend"
      to that opportunity's usage fields. It never writes stage, amount or close date.
---

# Usage onto the Salesforce opportunity

Slash command: /salesforce-usage-to-opportunity

## Step 1: Count active seats

Build a computed attribute on accounts named "usage_active_seats": the number of the account's users who did account usage event at least once in the last 30 d.

## Step 2: Read the usage trend

Build a computed attribute on accounts named "usage_trend" with one of the values growing, flat or declining: compare the account's count of account usage event in the last 30 d with the 30 d before that; growing when it is 10% or more higher, declining when it is 10% or more lower, flat otherwise.

## Step 3: Update the open opportunity

Build an automation that runs every Monday at 06:00 on a schedule. For each account with an open opportunity in open opportunity, it writes usage_active_seats from "Count active seats" and usage_trend from "Read the usage trend" to that opportunity's usage fields. It never writes stage, amount or close date.
