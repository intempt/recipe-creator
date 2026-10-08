---
description: Accounts created in the last week that have barely done anything yet, so SDRs know who to contact first.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Net-new prospect accounts

Slash command: /net-new-prospects

## Step 1: Build the net-new account list

Build a segment of accounts named "Net-New Prospects".
An account is in the segment only when all of these are true:
- its created_at attribute is within the last 7 days
- its total_events attribute is 5 or less
- its account_lifecycle attribute is "prospect"
- its has_open_deal attribute is false
