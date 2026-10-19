---
frontmatter_id: at-risk-vips
slash_command: /at-risk-vips
description: Your biggest spenders who have gone quiet for about six weeks, so you can reach out personally before they drift away for good.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# At-risk VIP customers

Slash command: /at-risk-vips

## Step 1: Build the at-risk VIP list

Build a segment of users named "At-Risk VIPs".
A user is in the segment only when all of these are true:
- their Lifetime value attribute is 1000 or more
- their Days since last activity attribute is between 45 and 90
- they did the Placed order event 2 or more times, at any time
- they did not do the Placed order event in the last 45 days
