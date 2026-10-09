---
description: Accounts that became customers in the last quarter, so onboarding and implementation start from one current list.
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

# Recently won accounts

Slash command: /recently-won-accounts

## Step 1: Build the recently-won list

Build a segment of accounts named "Recently-Won Accounts".
An account is in the segment only when all of these are true:
- its Lifecycle changed date attribute is within the last 90 days
- its Lifecycle stage attribute is "customer"
- its Has an open deal attribute is false
