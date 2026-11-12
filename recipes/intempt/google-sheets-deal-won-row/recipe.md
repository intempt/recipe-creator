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
    instruction: 'Trigger when {deal_won_event} fires, i.e. a deal stage changes to Closed Won. Append one row to the sheet
      {target_sheet}, tab {sheet_tab}, using the {google_sheets_integration} connection. Map columns by header name, never
      by position, so inserting a column in the sheet does not redirect later writes. Write these values: deal name from {deal_won_event.deal_name},
      account from {deal_won_event.account}, amount from {deal_won_event.amount}, close date from {deal_won_event.close_date},
      owner from {deal_won_event.owner}, source from {deal_won_event.source}. On a write failure, apply {failure_policy}:
      skip the row and record it so skipped rows can be recovered, so a temporarily locked sheet does not fail the run.'
---

# Log won deals to a sheet

Slash command: /google-sheets-deal-won-row

## Step 1: Append a row on every win

Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable.
