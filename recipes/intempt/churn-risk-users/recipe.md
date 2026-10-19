---
frontmatter_id: churn-risk-users
slash_command: /churn-risk-users
description: Paying users who used to log in regularly and have not shown up for a month, so you can reach them before they cancel.
author:
  name: Intempt
  last_name: Technologies
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
- they did the Session start event 5 or more times between 60 and 90 days ago
- they did not do the Session start event in the last 30 days
- their Plan attribute is not "free"
