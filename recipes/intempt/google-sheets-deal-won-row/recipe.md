---
frontmatter_id: google-sheets-deal-won-row
slash_command: /google-sheets-deal-won-row
description: Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already have.
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
    - { value: google_sheets, severity: blocking }
portable:
  summary: Adds a row to a Google Sheet each time a deal is won, so finance and ops can keep working in the sheet they already
    use.
  parameters:
  - name: target_sheet
    type: string
    label: Google Sheet to append won deals to
    required: true
  - name: sheet_tab
    type: string
    label: Sheet tab name
    required: true
  - name: failure_policy
    type: enum
    label: Failure policy when a row cannot be written
    default: skip_and_record
    options:
    - skip_and_record
    - fail_run
    - retry
  requirements:
  - slot: deal_won_event
    kind: event
    meaning: A deal stage changed to Closed Won
    properties:
    - name: deal_name
      type: string
      meaning: Name of the deal
      optional: false
    - name: account
      type: string
      meaning: Account the deal belongs to
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
    - name: close_date
      type: date
      meaning: Date the deal closed
      optional: false
    - name: owner
      type: string
      meaning: Deal owner
      optional: false
    - name: source
      type: string
      meaning: Lead or deal source
      optional: false
  - slot: google_sheets_integration
    kind: integration
    meaning: A connected Google Sheets account with write access to the target sheet
    channel: google_sheets
  steps:
  - id: s1
    builds: automation
    uses:
    - deal_won_event
    - google_sheets_integration
    - target_sheet
    - sheet_tab
    - failure_policy
    instruction: 'Build an automation triggered when {deal_won_event} happens. It appends one row to the sheet {target_sheet},
      tab {sheet_tab}, through {google_sheets_integration}, matching columns by header name: deal name from {deal_won_event.deal_name},
      account from {deal_won_event.account}, amount from {deal_won_event.amount}, close date from {deal_won_event.close_date},
      owner from {deal_won_event.owner}, source from {deal_won_event.source}. When a row cannot be written it applies {failure_policy},
      where skip_and_record skips the row and records it for recovery.'
---

# Log won deals to a sheet

Slash command: /google-sheets-deal-won-row

## Step 1: Append a row on every win

Build an automation triggered when deal won event happens. It appends one row to the sheet the google Sheet to append won deals to, tab the sheet tab name, through google sheets integration, matching columns by header name: deal name from deal name, account from account, amount from amount, close date from close date, owner from owner, source from source. When a row cannot be written it applies skip_and_record, where skip_and_record skips the row and records it for recovery.
