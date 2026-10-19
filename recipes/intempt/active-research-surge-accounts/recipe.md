---
frontmatter_id: active-research-surge-accounts
slash_command: /active-research-surge-accounts
description: Users who viewed your pricing page 3 or more times in the past 7 days, so an AE can reach out while they are still looking.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Accounts researching pricing now

Slash command: /active-research-surge-accounts

## Step 1: Build the pricing-surge list

Build a segment of accounts named "Active Research Surge Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the View page event with a Page URL that contains "/pricing" 3 or more times in the last 7 days
- its Has an open deal attribute is false
