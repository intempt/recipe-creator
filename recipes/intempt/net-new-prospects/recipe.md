---
frontmatter_id: net-new-prospects
slash_command: /net-new-prospects
description: Accounts created in the last week that have barely done anything yet, so SDRs know who to contact first.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Net-new prospect accounts

Slash command: /net-new-prospects

## Step 1: Build the net-new account list

Build a segment of accounts named "Net-New Prospects".
An account is in the segment only when all of these are true:
- its Created date attribute is within the last 7 days
- its Total events attribute is 5 or less
- its Lifecycle stage attribute is "prospect"
- its Has an open deal attribute is false
