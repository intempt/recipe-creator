---
frontmatter_id: big-basket-buyers
slash_command: /big-basket-buyers
description: Customers who spend heavily on every single order, so premium bundles and higher tiers go to people who already buy big.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# Big basket buyers

Slash command: /big-basket-buyers

## Step 1: Build the big-basket list

Build a segment of users named "Big-Basket Buyers".
A user is in the segment only when all of these are true:
- their Average order value attribute is 150 or more
- they did the Placed order event 2 or more times, at any time
- their Lifetime value attribute is 300 or more
