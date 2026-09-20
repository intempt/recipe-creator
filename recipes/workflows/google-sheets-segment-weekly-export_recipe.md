---
name: google-sheets-segment-weekly-export
description: Use when a user mentions "weekly segment export", "segment to spreadsheet", "scheduled sheet export", or asks for related help. Export a segment to a Google Sheet on a schedule, replacing the weekly CSV someone downloads and re-uploads by hand.
arguments: []
intempt:
  id: google-sheets-segment-weekly-export
  title: "Weekly segment export to a sheet"
  version: 1.0.0
  slashCommand: /google-sheets-segment-weekly-export
  group: Workflows
  shortDescription: "Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads by hand."
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
      title: "Pick the audience to export"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Define it as a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same list."
      prompt: 'Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience.'
    - step: 2
      title: "Refresh the sheet each week"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      description: "A weekly run writes the segment's members into the sheet, matched on the record identifier so a repeat run updates rows instead of duplicating them. The row count is stated before the run, so a segment that has collapsed or exploded is visible."
      prompt: 'Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it: a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly segment export to a sheet

Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads by hand.

## Before you run it

- Connect google_sheets

## What it does

1. **Pick the audience to export** (`create_segment`)

   Define it as a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same list.

2. **Refresh the sheet each week** (`create_workflow`)

   A weekly run writes the segment's members into the sheet, matched on the record identifier so a repeat run updates rows instead of duplicating them. The row count is stated before the run, so a segment that has collapsed or exploded is visible.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
