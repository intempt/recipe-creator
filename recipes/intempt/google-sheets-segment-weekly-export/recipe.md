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
  - name: target_sheet
    type: string
    label: Google Sheet the segment is written to
    required: true
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
    builds: automation
    uses:
    - audience_segment
    - export_sheet
    - customer_record_id
    - sheet_tab
    - target_sheet
    instruction: 'Build an automation that runs every Monday at 06:00 on a schedule. Each run it reads the current members
      of {audience_segment} and writes them to the sheet {target_sheet}, tab {sheet_tab}, through {export_sheet}: a member
      whose {customer_record_id} already has a row updates that row, any other member is appended as a new row. Each run first
      records the member count of {audience_segment} and the count from the run before.'
---

# Weekly segment export to a sheet

Slash command: /google-sheets-segment-weekly-export

## Step 1: Refresh the sheet each week

Build an automation that runs every Monday at 06:00 on a schedule. Each run it reads the current members of audience segment and writes them to the sheet the google Sheet the segment is written to, tab Sheet1, through export sheet: a member whose customer record id already has a row updates that row, any other member is appended as a new row. Each run first records the member count of audience segment and the count from the run before.
