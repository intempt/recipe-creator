---
frontmatter_id: demo-requested-accounts
slash_command: /demo-requested-accounts
description: People who submitted a demo form in the last 30 days, so an SDR can follow up the same hour.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds a segment of accounts whose users submitted the demo request form in the last 30 days and have no open deal,
    so an SDR can follow up the same hour.
  parameters:
  - name: lookbackWindow
    type: duration
    label: Lookback window for demo form submissions
    default: 30 d
    required: false
  - name: demoFormName
    type: string
    label: Demo request form chosen for this run
    required: true
  requirements:
  - slot: demo_request_submitted
    kind: event
    meaning: A customer submitted a demo request form
    properties:
    - name: form_name
      type: string
      meaning: Name of the form that was submitted
      optional: false
  - slot: has_open_deal
    kind: attribute
    meaning: Whether the account has an open deal
  steps:
  - id: s1
    builds: segment
    uses:
    - demo_request_submitted
    - has_open_deal
    - lookbackWindow
    - demoFormName
    instruction: 'Build a new segment of accounts named "Demo-Requested Accounts". An account is in the segment only when
      all of these are true: the users in the account together did {demo_request_submitted} with form_name equal to {demoFormName}
      at least once in the last {lookbackWindow}; and {has_open_deal} is false.'
---

# Accounts that asked for a demo

Slash command: /demo-requested-accounts

## Step 1: Build the demo-request list

Build a new segment of accounts named "Demo-Requested Accounts". An account is in the segment only when all of these are true: the users in the account together did demo request submitted with form_name equal to the demo request form chosen for this run at least once in the last 30 d; and has open deal is false.
