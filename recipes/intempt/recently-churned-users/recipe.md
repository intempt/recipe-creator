---
frontmatter_id: recently-churned-users
slash_command: /recently-churned-users
description: Customers who cancelled in the last month, sent a win-back email and flagged to the retention team while the reason is still fresh.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Recently cancelled customers

Slash command: /recently-churned-users

## Step 1: Build the recent-cancel list

Build a segment of users named "Recently Churned Users".
A user is in the segment only when all of these are true:
- they did the Subscription canceled event at least once in the last 30 days
- their Lifetime value attribute is more than 0

## Step 2: Draft a win-back email

Generate a designed marketing email for the users in "Recently Churned Users" inviting them back. Three sentences, warm and non-defensive tone, asking what did not work and offering to help, no discount language, one button linking to the page for restarting their subscription. Use the result of "Build the recent-cancel list".

## Step 3: Notify the retention team

Generate a Slack message to the channel chosen for this run listing the users in "Recently Churned Users" so the team can track cancellation volume and follow up personally with the highest-value ones. Use the result of "Build the recent-cancel list".
