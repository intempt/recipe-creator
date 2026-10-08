---
description: Paid subscriptions that end within the next three months, so renewal conversations start early instead of the week before.
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
  - finance
  - media
---

# Renewals due in 90 days

Slash command: /renewal-window-90-day

## Step 1: Build the renewal list

Build a segment of users named "Renewal Window: 90 Days".
A user is in the segment only when all of these are true:
- their end_date attribute is in the future and within the next 90 days
- their plan_name attribute is not "free"
