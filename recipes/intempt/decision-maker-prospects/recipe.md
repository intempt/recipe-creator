---
description: Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually holds the budget.
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

# Decision makers checking pricing

Slash command: /decision-maker-prospects

## Step 1: Build the decision-maker list

Build a segment of users named "Decision-Maker Prospects".
A user is in the segment only when all of these are true:
- their title attribute contains any of "CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of" or "Chief"
- they did the page_viewed event with a page_url that contains "/pricing" at least once in the last 30 days
- their email attribute is not empty
