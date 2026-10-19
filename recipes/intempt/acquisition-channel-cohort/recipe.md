---
frontmatter_id: acquisition-channel-cohort
slash_command: /acquisition-channel-cohort
description: Customers grouped by the channel that brought them in, so you can compare how well each channel's buyers stick around.
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
---

# Customers by acquisition channel

Slash command: /acquisition-channel-cohort

## Step 1: Build the channel cohort

Build a segment of users named "Google Paid Acquired".
A user is in the segment only when all of these are true:
- their UTM source attribute is "google"
- their UTM medium attribute is "cpc"
- they did the Placed order event at least once, at any time
