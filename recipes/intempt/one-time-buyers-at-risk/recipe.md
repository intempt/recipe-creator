---
frontmatter_id: one-time-buyers-at-risk
slash_command: /one-time-buyers-at-risk
description: Customers who bought once, have not been back in two months, and are not trending well, so you can give them a reason to return.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# One-time buyers going cold

Slash command: /one-time-buyers-at-risk

## Step 1: Build the one-time-buyer list

Build a segment of users named "One-Time Buyers At Risk".
A user is in the segment only when all of these are true:
- they did the Placed order event exactly 1 time, at any time
- their Days since last activity attribute is 60 or more
- their Lifecycle score attribute is neither "Regulars" nor "Promising"
