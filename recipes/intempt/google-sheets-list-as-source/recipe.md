---
frontmatter_id: google-sheets-list-as-source
slash_command: /google-sheets-list-as-source
description: Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into imported
  users and a segment you can act on.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Imports a hand-kept Google Sheet, such as target accounts, event attendees or a suppression list, on a schedule
    and turns its rows into a segment you can act on.
  parameters:
  - name: sheet_name
    type: string
    label: Name of the Google Sheet to read
    required: true
  - name: schedule_frequency
    type: enum
    label: How often to re-import the sheet
    default: daily
    required: false
    options:
    - hourly
    - daily
    - weekly
  - name: match_key
    type: string
    label: Column used to match existing records (for example email or domain)
    default: email
    required: false
  requirements:
  - slot: google_sheet_source
    kind: integration
    meaning: A connected Google Sheets account with read access to the named sheet
    channel: google_sheets
  - slot: sheet_list_name
    kind: attribute
    meaning: The name of the sheet a user was last imported from, written by the import
  steps:
  - id: s1
    builds: automation
    uses:
    - google_sheet_source
    - sheet_name
    - schedule_frequency
    - match_key
    - sheet_list_name
    instruction: Build an automation that runs {schedule_frequency} on a schedule. Each run it reads the rows of the sheet
      named {sheet_name} through {google_sheet_source} and adds or updates one user per row, matched on the {match_key} column,
      setting the user's {sheet_list_name} attribute to {sheet_name}. Each run records how many rows were accepted, skipped
      and rejected, with the reason for every skipped or rejected row.
  - id: s2
    builds: segment
    uses:
    - s1
    - sheet_list_name
    - sheet_name
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Sheet list audience" with every user whose {sheet_list_name} attribute
      equals {sheet_name}, as set by the automation from "Import the rows on a schedule".
---

# Use a Google Sheet as a list

Slash command: /google-sheets-list-as-source

## Step 1: Import the rows on a schedule

Build an automation that runs daily on a schedule. Each run it reads the rows of the sheet named the name of the Google Sheet to read through google sheet source and adds or updates one user per row, matched on the email column, setting the user's sheet list name attribute to the name of the Google Sheet to read. Each run records how many rows were accepted, skipped and rejected, with the reason for every skipped or rejected row.

## Step 2: Turn them into an audience

Build a new segment of users named "Sheet list audience" with every user whose sheet list name attribute equals the name of the Google Sheet to read, as set by the automation from "Import the rows on a schedule".
