---
frontmatter_id: google-sheets-segment-weekly-export
slash_command: /google-sheets-segment-weekly-export
description: Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads by hand.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Writes a chosen audience segment into a Google Sheet every week, keeping the sheet updated instead of re-uploading
    a CSV by hand.
  parameters:
  - name: sheet_tab
    type: string
    label: Sheet tab name
    default: Sheet1
    required: false
  - name: export_frequency
    type: enum
    label: Export frequency
    default: weekly
    required: false
    options:
    - weekly
  - name: row_count_alert_check
    type: boolean
    label: Report row count before each run
    default: true
    required: false
  requirements:
  - slot: audience_segment
    kind: segment
    meaning: The audience segment whose members should be exported each week
  - slot: export_sheet
    kind: integration
    meaning: A Google Sheets connection where the segment members are written
    channel: google_sheets
  - slot: customer_record_id
    kind: attribute
    meaning: The unique record identifier used to match existing rows in the sheet
  steps:
  - id: s1
    builds: segment
    uses:
    - audience_segment
    instruction: Pick the segment {audience_segment} whose members should land in the sheet each week. Keep it as a segment
      rather than a filter inside the workflow so the same definition drives the export and any other use of the same audience.
  - id: s2
    builds: automation
    uses:
    - s1
    - audience_segment
    - export_sheet
    - customer_record_id
    - sheet_tab
    - export_frequency
    instruction: Create a scheduled workflow that runs {export_frequency} and reads the members of the segment chosen in "Pick
      the audience to export". Append-or-update the members to the Google Sheet {export_sheet}, tab {sheet_tab}, matched on
      {customer_record_id} so a re-run updates existing rows rather than duplicating them. Before each run, state the row
      count of the segment so an author can spot a segment that has unexpectedly collapsed or exploded.
---

# Weekly segment export to a sheet

Slash command: /google-sheets-segment-weekly-export

## Step 1: Pick the audience to export

Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience.

## Step 2: Refresh the sheet each week

Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it: a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded. Use the result of "Pick the audience to export".
