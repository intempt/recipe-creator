---
frontmatter_id: mid-market-accounts
slash_command: /mid-market-accounts
description: Companies with 100 to 1,000 employees, flagged to inside sales and sent a getting-started email, so your mid-market motion starts automatically.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Mid-market accounts

Slash command: /mid-market-accounts

## Step 1: Build the mid-market list

Build a segment of accounts named "Mid-Market Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 100 or more
- its employees attribute is less than 1000

## Step 2: Notify sales ops

Generate a plain-text email to the sales ops distribution list listing the accounts in "Mid-Market Accounts" so inside sales can assign owners to the newest accounts first. Use the result of "Build the mid-market list".

## Step 3: Send a getting-started email

Generate a designed marketing email for the accounts in "Mid-Market Accounts" introducing features relevant to a growing team and inviting them to book a walkthrough. Three sentences, friendly and consultative tone, no discount language, one button linking to the walkthrough booking page. Use the result of "Build the mid-market list".
