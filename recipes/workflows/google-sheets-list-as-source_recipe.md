---
name: google-sheets-list-as-source
description: Use when a user mentions "sheet as a list", "import target accounts from sheets", "spreadsheet as source", or asks for related help. Treat a Google Sheet a team already maintains by hand (target accounts, an event list, a suppression list) as records the platform can segment and act on.
arguments: []
intempt:
  id: google-sheets-list-as-source
  title: "Use a Google Sheet as a list"
  version: 1.0.0
  slashCommand: /google-sheets-list-as-source
  group: Workflows
  shortDescription: "Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into records you can segment and act on."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [google-sheets, import, list]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: google_sheets, severity: blocking }
  invokesCommands:
    - create_workflow
    - create_segment
  procedure:
    - step: 1
      title: "Import the rows on a schedule"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Reads the named sheet and upserts the rows as records, matched on a key column such as email or domain. Each run reports how many rows were accepted, skipped and rejected, with a reason for each, because a hand kept sheet always has bad rows and a bare total teaches nobody which ones to fix."
      prompt: 'Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched on a key column such as email or domain. Report accepted, skipped and rejected counts per run with a reason per row: a hand-maintained sheet always has malformed rows, and a silent total teaches nobody which ones to fix.'
    - step: 2
      title: "Turn them into an audience"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - workflow
      description: "A segment over the imported records, so the list works everywhere else in the platform rather than only at the moment the sheet is read."
      prompt: 'Create a segment over the imported records so the list is usable everywhere else. This is the point of importing rather than reading the sheet at the moment of use: the list becomes an audience the rest of the platform understands.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Use a Google Sheet as a list

Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into records you can segment and act on.

## Before you run it

- Connect google_sheets

## What it does

1. **Import the rows on a schedule** (`create_workflow`)

   Reads the named sheet and upserts the rows as records, matched on a key column such as email or domain. Each run reports how many rows were accepted, skipped and rejected, with a reason for each, because a hand kept sheet always has bad rows and a bare total teaches nobody which ones to fix.

2. **Turn them into an audience** (`create_segment`)

   A segment over the imported records, so the list works everywhere else in the platform rather than only at the moment the sheet is read.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
