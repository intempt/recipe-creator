---
frontmatter_id: winnable-churned-users
slash_command: /winnable-churned-users
description: Customers who cancelled in the last two months but are still logging in, texted a quick way back in and flagged to the retention team as the best odds for a win-back.
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

# Winnable churned users

Slash command: /winnable-churned-users

## Step 1: Build the win-back list

Build a segment of users named "Winnable Churned Users".
A user is in the segment only when all of these are true:
- they did the Subscription canceled event at least once in the last 60 days
- their Lifetime value attribute is more than 0
- they did the Session start event at least once in the last 7 days

## Step 2: Send a quick win-back text

Generate an SMS for the users in "Winnable Churned Users" letting them know they are welcome back and it only takes a minute to reactivate. One or two sentences, warm and direct tone, no discount language. Use the result of "Build the win-back list".

## Step 3: Alert the retention team

Generate a Slack message to the channel chosen for this run listing the users in "Winnable Churned Users" and noting that they are still active despite cancelling, so the team prioritizes them first. Use the result of "Build the win-back list".
