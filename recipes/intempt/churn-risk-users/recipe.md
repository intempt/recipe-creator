---
description: Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.
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

# Paid users going quiet

Slash command: /churn-risk-users

## Step 1: Build the silent paid-user list

Build a segment of users named "Churn Risk Users".
A user is in the segment only when all of these are true:
- they did the session_start event 5 or more times between 60 and 90 days ago
- they did not do the session_start event in the last 30 days
- their plan_name attribute is not "free"
