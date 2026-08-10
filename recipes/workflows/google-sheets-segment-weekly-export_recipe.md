---
name: google-sheets-segment-weekly-export
description: Use when a user mentions "weekly segment export", "segment to spreadsheet", "scheduled sheet export", or asks for related help. Export a segment to a Google Sheet on a schedule, replacing the weekly CSV someone downloads and re-uploads by hand.
arguments: []
intempt:
  id: google-sheets-segment-weekly-export
  version: 1.0.0
  slashCommand: /google-sheets-segment-weekly-export
  group: Workflows
  shortDescription: "Export a segment to a Google Sheet on a schedule, replacing the weekly CSV someone downloads and re-uploads by hand."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [all]
    complexity: starter
    executionMode: live
    tags: [google-sheets, export, scheduled]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: google_sheets, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: Define The Segment To Export
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience.'
      prompt: 'Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience.'
    - step: 2
      title: Export It On A Schedule
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      description: 'Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it — a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded.'
      prompt: 'Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it — a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Google Sheets Segment Weekly Export

> **Not runnable yet.** Appending rows in Google Sheets has no backend. The connector reads today and cannot write, and Airbyte does not close that gap — its destinations write to warehouses, not into Google Sheets. This recipe is published so the demand is recorded and the workflow is designed, and it will fail at the write step until the operation ships.

## Procedure

1. **Define The Segment To Export** [`create_segment`] — Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience. → produces: segment
2. **Export It On A Schedule** [`create_workflow`] — Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it — a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded. → produces: workflow

## Prerequisites

- Integration **google_sheets** (blocking)
