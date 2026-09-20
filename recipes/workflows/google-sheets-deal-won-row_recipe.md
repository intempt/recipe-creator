---
name: google-sheets-deal-won-row
description: Use when a user mentions "deal won to sheet", "append row when deal closes", "closed won spreadsheet", or asks for related help. Append a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already use instead of asking for a CRM seat.
arguments: []
intempt:
  id: google-sheets-deal-won-row
  title: "Log won deals to a sheet"
  version: 1.0.0
  slashCommand: /google-sheets-deal-won-row
  group: Workflows
  shortDescription: "Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already have."
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
      title: "Append a row on every win"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "When a deal moves to closed won, a row goes into the chosen sheet with the deal, account, amount, close date, owner and source. Columns are matched by header name and never by position, so inserting a column cannot silently misdirect every write after it. A sheet that is momentarily locked does not fail the run: the skipped rows are recorded so they can be recovered."
      prompt: 'Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Log won deals to a sheet

Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already have.

## Before you run it

- Connect google_sheets
- Send the `deal_stage_changed` event

## What it does

1. **Append a row on every win** (`create_workflow`)

   When a deal moves to closed won, a row goes into the chosen sheet with the deal, account, amount, close date, owner and source. Columns are matched by header name and never by position, so inserting a column cannot silently misdirect every write after it. A sheet that is momentarily locked does not fail the run: the skipped rows are recorded so they can be recovered.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
