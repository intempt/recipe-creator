---
description: Turns a sheet your team keeps by hand, target accounts or an event list or a suppression list, into records you can segment and act on.
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

# Use a Google Sheet as a list

Slash command: /google-sheets-list-as-source

## Step 1: Import the rows on a schedule

Create a scheduled workflow that reads rows from the named sheet and upserts them as records, matched on a key column such as email or domain. Report accepted, skipped and rejected counts per run with a reason per row: a hand-maintained sheet always has malformed rows, and a silent total teaches nobody which ones to fix.

## Step 2: Turn them into an audience

Create a segment over the imported records so the list is usable everywhere else. This is the point of importing rather than reading the sheet at the moment of use: the list becomes an audience the rest of the platform understands. Use the result of "Import the rows on a schedule".
