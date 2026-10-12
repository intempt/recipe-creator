---
frontmatter_id: demo-requested-accounts
slash_command: /demo-requested-accounts
description: People who submitted a demo form in the last 30 days, so an SDR can follow up the same hour.
author:
  name: Harish Kumar
  first_name: Harish
  last_name: Kumar
  company: Intempt
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Accounts that asked for a demo

Slash command: /demo-requested-accounts

## Step 1: Build the demo-request list

Build a segment of accounts named "Demo-Requested Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the Submit on event on the demo request form chosen for this run at least once in the last 30 days
- its Has an open deal attribute is false
