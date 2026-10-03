---
id: google-sheets-list-as-source
title: Use a Google Sheet as a list
slash_command: /google-sheets-list-as-source
group: Workflows
owner: intempt
summary: Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list,
  into records you can segment and act on.
description: >-
  Treat a Google Sheet a team already maintains by hand (target accounts, an event list, a suppression
  list) as records the platform can segment and act on.
version: 2.0.0
classification:
  product:
    - marketing
  agent: revops-automator
  mode:
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - google-sheets
    - import
    - list
prerequisites:
  integrations:
    - value: google_sheets
      severity: blocking
steps:
  - id: s1
    title: Import the rows on a schedule
    summary: >-
      Reads the named sheet and upserts the rows as records, matched on a key column such as email or
      domain. Each run reports how many rows were accepted, skipped and rejected, with a reason for each,
      because a hand kept sheet always has bad rows and a bare total teaches nobody which ones to fix.
    builds: workflow
    description: >-
      Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched
      on a key column such as email or domain. Report accepted, skipped and rejected counts per run with
      a reason per row: a hand-maintained sheet always has malformed rows, and a silent total teaches
      nobody which ones to fix.
  - id: s2
    title: Turn them into an audience
    summary: >-
      A segment over the imported records, so the list works everywhere else in the platform rather than
      only at the moment the sheet is read.
    builds: segment
    description: >-
      Create a segment over the imported records so the list is usable everywhere else. This is the point
      of importing rather than reading the sheet at the moment of use: the list becomes an audience the
      rest of the platform understands. Use the result of "Import the rows on a schedule".
    dependsOn:
      - s1
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Use a Google Sheet as a list

Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into records you can segment and act on.

## Steps

1. **Import the rows on a schedule** (builds workflow)

   Reads the named sheet and upserts the rows as records, matched on a key column such as email or domain. Each run reports how many rows were accepted, skipped and rejected, with a reason for each, because a hand kept sheet always has bad rows and a bare total teaches nobody which ones to fix.

2. **Turn them into an audience** (builds segment)

   A segment over the imported records, so the list works everywhere else in the platform rather than only at the moment the sheet is read.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **segment** (segment): Segment produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
