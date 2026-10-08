---
description: Writes a segment into a Google Sheet every week, replacing the CSV someone downloads and re-uploads by hand.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
---

# Weekly segment export to a sheet

Slash command: /google-sheets-segment-weekly-export

## Step 1: Pick the audience to export

Create or pick the segment whose members should land in the sheet each week. Keep it a segment rather than a filter inside the workflow, so the same definition drives the export and anything else that needs the same audience.

## Step 2: Refresh the sheet each week

Create a scheduled workflow that reads the segment and appends its members to a Google Sheet weekly. Use append-or-update matched on the record identifier so a re-run maintains the sheet rather than duplicating it: a plain append turns a weekly export into a growing pile nobody trusts. State the row count before the run so an author can see a segment that has unexpectedly collapsed or exploded. Use the result of "Pick the audience to export".
