---
description: Adds a row to a Google Sheet every time a deal is won, so finance and ops keep working in the sheet they already have.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
---

# Log won deals to a sheet

Slash command: /google-sheets-deal-won-row

## Step 1: Append a row on every win

Create a workflow triggered on deal stage changing to Closed Won. One step: append a row to the chosen Google Sheet with deal name, account, amount, close date, owner and source. Map columns by header name, never by position, so someone inserting a column in the sheet does not silently redirect every write after it. Failure policy is skip-and-record: a sheet that is momentarily locked should not fail the run, and the skipped rows need to be recoverable.
