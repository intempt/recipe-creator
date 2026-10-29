---
frontmatter_id: accounts-no-open-deal
slash_command: /accounts-no-open-deal
description: Established accounts whose users log in constantly, checked in on by email and flagged to account executives to review for expansion whitespace.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Expansion whitespace accounts

Slash command: /accounts-no-open-deal

## Step 1: Build the whitespace list

Build a segment of accounts named "Expansion Whitespace Accounts".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- the users in the account together did the Session start event 5 or more times in the last 30 days

## Step 2: Send a value check-in

Generate a designed marketing email for the accounts in "Expansion Whitespace Accounts" checking in on how the team is using the product and surfacing one feature they may not have tried yet. Three sentences, consultative and helpful tone, no pricing language, one button linking to a call-booking page. Use the result of "Build the whitespace list".

## Step 3: Flag to account executives

Generate a plain-text email to the account executive distribution list listing the accounts in "Expansion Whitespace Accounts" so they can review each one for expansion opportunity. Use the result of "Build the whitespace list".
