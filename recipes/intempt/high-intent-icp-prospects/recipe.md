---
frontmatter_id: high-intent-icp-prospects
slash_command: /high-intent-icp-prospects
description: ICP-sized accounts with recent activity on your site, flagged to sales and sent an outreach email while interest is still warm.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# ICP accounts showing intent

Slash command: /high-intent-icp-prospects

## Step 1: Build the hot ICP list

Build a segment of accounts named "High-Intent ICP Prospects".
An account is in the segment only when all of these are true:
- its employees attribute is 50 or more
- its employees attribute is less than 1000
- the users in the account together did the View page event at least once in the last 7 days

## Step 2: Alert sales

Generate a Slack message to the sales channel listing the accounts in "High-Intent ICP Prospects" so reps can reach out while interest is still warm. Use the result of "Build the hot ICP list".

## Step 3: Send an outreach email

Generate a designed marketing email for the accounts in "High-Intent ICP Prospects" introducing the product's most relevant feature for a company of their size. Three sentences, confident and consultative tone, no discount language, one button linking to a call-booking page. Use the result of "Build the hot ICP list".
