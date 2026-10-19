---
frontmatter_id: engaged-non-buyers
slash_command: /engaged-non-buyers
description: People who use your site a lot but have never placed an order, so you can aim a first-purchase offer at them.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# Engaged visitors who never bought

Slash command: /engaged-non-buyers

## Step 1: Build the non-buyer list

Build a segment of users named "Engaged Non-Buyers".
A user is in the segment only when all of these are true:
- their Total events attribute is 10 or more
- they have never done the Placed order event
- their Days since last activity attribute is 7 or less
- their email attribute is not empty
