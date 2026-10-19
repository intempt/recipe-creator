---
frontmatter_id: high-intent-anonymous-visitors
slash_command: /high-intent-anonymous-visitors
description: Visitors you cannot email yet who keep coming back, so you can retarget them with ads or try to capture an address.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - media
---

# High-intent anonymous visitors

Slash command: /high-intent-anonymous-visitors

## Step 1: Build the anonymous visitor list

Build a segment of users named "High-Intent Anonymous Visitors".
A user is in the segment only when all of these are true:
- their Total events attribute is 5 or more
- their email attribute is empty
- they did the View page event 3 or more times in the last 7 days
- they did the Session start event 2 or more times in the last 7 days
