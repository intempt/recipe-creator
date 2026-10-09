---
description: Identify product-qualified leads by segmenting free and trial users who log multiple sessions and complete key activation goals.
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
  - ecommerce
---

# Free accounts with a team trying it

Slash command: /pql-multi-user-account

## Step 1: Build the team-trial list

Build a segment of accounts named "PQL: Multi-User Account".
An account is in the segment only when all of these are true:
- its User count attribute is 2 or more
- the users in the account together did the Session start event 3 or more times in the last 14 days
- the users in the account together did the Completed a journey goal event at least once in the last 14 days
