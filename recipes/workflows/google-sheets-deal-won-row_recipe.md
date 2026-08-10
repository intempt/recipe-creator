---
name: google-sheets-deal-won-row
description: Use when a user mentions "deal won to sheet", "append row when deal closes", "closed won spreadsheet", or asks for related help. Append a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already use instead of asking for a CRM seat.
arguments: []
intempt:
  id: google-sheets-deal-won-row
  version: 1.0.0
  slashCommand: /google-sheets-deal-won-row
  group: Workflows
  shortDescription: "Append a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already use instead of asking for a CRM seat."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b]
    complexity: starter
    executionMode: live
    tags: [google-sheets, deal-won, handoff]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    events:
      - { value: deal_stage_changed, severity: blocking }
    integrations:
      - { value: google_sheets, severity: blocking }
  invokesCommands:
    - create_workflow
  procedure:
    - step: 1
      title: Append Won Deals To A Sheet
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable.'
      prompt: 'Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Google Sheets Deal Won Row

> **Not runnable yet.** Appending a row in Google Sheets has no backend. The connector reads today and cannot write, and Airbyte does not close that gap — its destinations write to warehouses, not into Google Sheets. This recipe is published so the demand is recorded and the workflow is designed, and it will fail at the write step until the operation ships.

## Procedure

1. **Append Won Deals To A Sheet** [`create_workflow`] — Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable. → produces: workflow

## Prerequisites

- Event `deal_stage_changed` (blocking)
- Integration **google_sheets** (blocking)
