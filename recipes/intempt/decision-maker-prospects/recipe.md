---
frontmatter_id: decision-maker-prospects
slash_command: /decision-maker-prospects
description: Senior people who looked at your pricing in the last month, so AEs can talk to whoever actually holds the budget.
author:
  name: Intempt
  last_name: Technologies
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
- their Job title attribute contains any of "CEO", "CTO", "CFO", "CMO", "COO", "VP", "Vice President", "Director", "Head of" or "Chief"
- they did the View page event with a Page URL that contains "/pricing" at least once in the last 30 days
- their email attribute is not empty
