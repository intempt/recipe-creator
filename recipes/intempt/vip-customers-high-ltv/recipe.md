---
frontmatter_id: vip-customers-high-ltv
slash_command: /vip-customers-high-ltv
description: Customers who have spent 1,000 or more across repeat orders, the base list for rewards, early access, and concierge support.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# VIP customers

Slash command: /vip-customers-high-ltv

## Step 1: Build the VIP list

Build a segment of users named "VIP Customers".
A user is in the segment only when all of these are true:
- their Lifetime value attribute is 1000 or more
- they did the Placed order event 2 or more times, at any time
