---
description: Individual users who logged 5 or more session_start and 10 or more page_viewed events in the last 14 days, a high-engagement segment per user.
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
---

# Accounts with a buying group active

Slash command: /multi-stakeholder-engaged-accounts

## Step 1: Build the multi-stakeholder list

Build a segment of accounts named "Multi-Stakeholder Engaged Accounts".
An account is in the segment only when all of these are true:
- its users_count attribute is 3 or more
- the users in the account together did the session_start event 5 or more times in the last 14 days
- the users in the account together did the page_viewed event 10 or more times in the last 14 days
