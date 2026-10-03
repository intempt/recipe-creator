---
id: google-sheets-deal-won-row
title: Log won deals to a sheet
slash_command: /google-sheets-deal-won-row
group: Workflows
owner: intempt
summary: Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the
  sheet they already have.
description: >-
  Append a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet
  they already use instead of asking for a CRM seat.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
  complexity: starter
  executionMode: live
  tags:
    - google-sheets
    - deal-won
    - handoff
prerequisites:
  events:
    - value: deal_stage_changed
      severity: blocking
  integrations:
    - value: google_sheets
      severity: blocking
steps:
  - id: s1
    title: Append a row on every win
    summary: >-
      When a deal moves to closed won, a row goes into the chosen sheet with the deal, account, amount,
      close date, owner and source. Columns are matched by header name and never by position, so inserting
      a column cannot silently misdirect every write after it. A sheet that is momentarily locked does
      not fail the run: the skipped rows are recorded so they can be recovered.
    builds: workflow
    description: >-
      Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the
      chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by
      header name, never by position, so someone inserting a column in the sheet does not silently redirect
      every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should
      not fail the run, and the skipped rows need to be recoverable.
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Log won deals to a sheet

Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already have.

## Steps

1. **Append a row on every win** (builds workflow)

   When a deal moves to closed won, a row goes into the chosen sheet with the deal, account, amount, close date, owner and source. Columns are matched by header name and never by position, so inserting a column cannot silently misdirect every write after it. A sheet that is momentarily locked does not fail the run: the skipped rows are recorded so they can be recovered.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
