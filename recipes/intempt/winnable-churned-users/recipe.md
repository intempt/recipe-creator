---
frontmatter_id: winnable-churned-users
slash_command: /winnable-churned-users
description: People who cancelled in the last two months but used the product heavily before they left, the best odds for a win-back.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Winnable churned users

Slash command: /winnable-churned-users

## Step 1: Build the win-back list

Build a segment of users named "Winnable Churned Users".
A user is in the segment only when all of these are true:
- they did the Subscription canceled event at least once in the last 60 days
- their Lifetime value attribute is more than 0
- their Total events attribute is 50 or more
