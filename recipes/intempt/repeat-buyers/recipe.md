---
frontmatter_id: repeat-buyers
slash_command: /repeat-buyers
description: Customers who have ordered three or more times this quarter and spent real money, the right list for loyalty perks and review requests.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce
---

# Repeat buyers

Slash command: /repeat-buyers

## Step 1: Build the repeat-buyer list

Build a segment of users named "Repeat Buyers".
A user is in the segment only when all of these are true:
- they did the Placed order event 3 or more times in the last 90 days
- their Lifetime value attribute is 100 or more
