---
id: google-sheets-segment-weekly-export
title: Weekly segment export to a sheet
slash_command: /google-sheets-segment-weekly-export
group: Workflows
owner: intempt
summary: Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads
  by hand.
description: >-
  Export a segment to a Google Sheet on a schedule, replacing the weekly CSV someone downloads and re-uploads
  by hand.
version: 2.0.0
classification:
  product:
    - marketing
  agent: revops-automator
  mode:
    - all
  complexity: starter
  executionMode: live
  tags:
    - google-sheets
    - export
    - scheduled
prerequisites:
  integrations:
    - value: google_sheets
      severity: blocking
steps:
  - id: s1
    title: Pick the audience to export
    summary: >-
      Define it as a segment rather than a filter inside the workflow, so the same definition drives the
      export and anything else that needs the same list.
    builds: segment
    description: >-
      Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather
      than a filter inside the workflow, so the same definition drives the export and anything else that
      needs the same audience.
  - id: s2
    title: Refresh the sheet each week
    summary: >-
      A weekly run writes the segment's members into the sheet, matched on the record identifier so a
      repeat run updates rows instead of duplicating them. The row count is stated before the run, so
      a segment that has collapsed or exploded is visible.
    builds: workflow
    description: >-
      Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly.
      Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than
      duplicating it: a plain append turns a weekly export into a growing pile nobody trusts. State the
      row count before the run so an author can see a segment that has unexpectedly collapsed or exploded.
      Use the result of "Pick the audience to export".
    dependsOn:
      - s1
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly segment export to a sheet

Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads by hand.

## Steps

1. **Pick the audience to export** (builds segment)

   Define it as a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same list.

2. **Refresh the sheet each week** (builds workflow)

   A weekly run writes the segment's members into the sheet, matched on the record identifier so a repeat run updates rows instead of duplicating them. The row count is stated before the run, so a segment that has collapsed or exploded is visible.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
