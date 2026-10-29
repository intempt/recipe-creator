---
frontmatter_id: icp-match-accounts
slash_command: /icp-match-accounts
description: Accounts sized right for your ideal customer profile, flagged to sales, sent an intro email, and tagged with an ICP-fit attribute so later segments and reports can reuse the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# ICP-fit accounts

Slash command: /icp-match-accounts

## Step 1: Build the ICP list

Build a segment of accounts named "ICP Match Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- its employees attribute is less than 500

## Step 2: Alert sales

Generate a Slack message to the sales channel listing the accounts in "ICP Match Accounts" so reps can prioritize outreach to the newest matches first. Use the result of "Build the ICP list".

## Step 3: Send an intro email

Generate a designed marketing email for the accounts in "ICP Match Accounts" introducing the product for a company of their size. Three sentences, confident and consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the ICP list".

## Step 4: Tag ICP-fit accounts

Create an attribute named "icp_fit" on accounts. Set it to true for every account in "ICP Match Accounts" and false for every other account, refreshed daily, so later segments and reports can filter on fit without rebuilding this logic. Use the result of "Build the ICP list".
