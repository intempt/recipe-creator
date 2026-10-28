---
description: "Free accounts showing real product usage, flagged to sales as a product-qualified lead and offered a look at what a paid plan unlocks."
frontmatter_id: pql-multi-user-account
author:
  name: V
  last_name: Ranadheer
  org_name: intempt
  email: rana@intempt.com
---
# Free accounts showing real usage

## Step 1: Build the active-free-account list

Build a segment of accounts named "PQL: Active Free Accounts". An account is in the segment only when all of these are true: the users in the account together did the Session start event 3 or more times in the last 14 days.

## Step 2: Alert sales

Generate a Slack message to the sales channel listing the accounts in "PQL: Active Free Accounts" so reps can reach out to this product-qualified lead while usage is fresh. Use the result of "Build the active-free-account list".

## Step 3: Send an upgrade email

Generate a designed marketing email for the accounts in "PQL: Active Free Accounts" showing what the team unlocks on a paid plan. Three sentences, confident and helpful tone, no discount language, one button linking to the pricing page. Use the result of "Build the active-free-account list".
