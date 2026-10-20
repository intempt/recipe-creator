---
frontmatter_id: multi-product-buyers
slash_command: /multi-product-buyers
description: Customers who have bought more than once and spent a meaningful amount, so cross-sell offers reach people with broad interest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# Multi-product buyers

Slash command: /multi-product-buyers

## Step 1: Build the repeat-spend list

Build a segment of users named "Multi-Product Buyers".
A user is in the segment only when all of these are true:
- they did the Placed order event 2 or more times in the last 180 days
- their Lifetime value attribute is 200 or more
