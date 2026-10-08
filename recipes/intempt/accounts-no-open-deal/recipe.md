---
description: Customer accounts with no open deal and account-level health attributes, plus per-user recent session activity, so AEs can review expansion whitespace.
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

# Healthy accounts with no open deal

Slash command: /accounts-no-open-deal

## Step 1: Build the whitespace list

Build a segment of accounts named "Accounts With No Open Deal".
An account is in the segment only when all of these are true:
- its has_open_deal attribute is false
- its account_health attribute is "healthy"
- its users_count attribute is 3 or more
- the users in the account together did the session_start event 5 or more times in the last 30 days
