---
name: google-sheets-list-as-source
description: Use when a user mentions "sheet as a list", "import target accounts from sheets", "spreadsheet as source", or asks for related help. Treat a Google Sheet a team already maintains by hand — target accounts, an event list, a suppression list — as records the platform can segment and act on.
arguments: []
intempt:
  id: google-sheets-list-as-source
  version: 1.0.0
  slashCommand: /google-sheets-list-as-source
  group: Workflows
  shortDescription: "Treat a Google Sheet a team already maintains by hand — target accounts, an event list, a suppression list — as records the platform can segment and act on."
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
      title: Read The Sheet On A Schedule
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched on a key column such as email or domain. Report accepted, skipped and rejected counts per run with a reason per row — a hand-maintained sheet always has malformed rows, and a silent total teaches nobody which ones to fix.'
      prompt: 'Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched on a key column such as email or domain. Report accepted, skipped and rejected counts per run with a reason per row — a hand-maintained sheet always has malformed rows, and a silent total teaches nobody which ones to fix.'
    - step: 2
      title: Segment On What The Sheet Says
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - workflow
      description: 'Create a segment over the imported records so the list is usable everywhere else. This is the point of importing rather than reading the sheet at the moment of use: the list becomes an audience the rest of the platform understands.'
      prompt: 'Create a segment over the imported records so the list is usable everywhere else. This is the point of importing rather than reading the sheet at the moment of use: the list becomes an audience the rest of the platform understands.'
---
