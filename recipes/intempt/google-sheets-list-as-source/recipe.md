---
frontmatter_id: google-sheets-list-as-source
slash_command: /google-sheets-list-as-source
description: Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into records you can segment and act on.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns a hand-maintained Google Sheet, such as target accounts, event attendees or a suppression list, into records
    you can segment and act on across the platform.
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
  - name: segment_name
    type: string
    label: Name of the audience segment built from the imported records
    default: Sheet list audience
    required: false
  requirements:
  - slot: google_sheet_source
    kind: integration
    meaning: A connected Google Sheets account with read access to the named sheet
    channel: google_sheets
  - slot: sheet_record
    kind: attribute
    meaning: A record imported from the Google Sheet, matched on a key column such as email or domain
    properties:
    - name: row_key
      type: string
      meaning: The value of the key column for the row, such as email or domain
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - google_sheet_source
    - sheet_name
    - schedule_frequency
    - match_key
    instruction: Create a scheduled workflow that runs {schedule_frequency} and reads rows from the sheet named {sheet_name}
      via {google_sheet_source}, then upserts them as records matched on the {match_key} column. Report accepted, skipped
      and rejected counts for each run, with a reason for every skipped or rejected row, so malformed rows can be found and
      fixed.
  - id: s2
    builds: segment
    uses:
    - s1
    - sheet_record
    - segment_name
    instruction: Create a segment named {segment_name} over the records imported by "Import the rows on a schedule" so the
      list can be used by every other part of the platform. Build it on {sheet_record} so the imported list is an audience
      the platform understands, rather than reading the sheet at the moment of use.
---

# Use a Google Sheet as a list

Slash command: /google-sheets-list-as-source

## Step 1: Import the rows on a schedule

Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched on a key column such as email or domain. Report accepted, skipped and rejected counts per run with a reason per row: a hand-maintained sheet always has malformed rows, and a silent total teaches nobody which ones to fix.

## Step 2: Turn them into an audience

Create a segment over the imported records so the list is usable everywhere else. This is the point of importing rather than reading the sheet at the moment of use: the list becomes an audience the rest of the platform understands. Use the result of "Import the rows on a schedule".
