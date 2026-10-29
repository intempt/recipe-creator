---
frontmatter_id: at-risk-vips
slash_command: /at-risk-vips
description: High lifetime value customers who have stopped logging in, checked on personally by their account manager and flagged to the retention team before they churn.
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

# At-risk VIP customers

Slash command: /at-risk-vips

## Step 1: Build the at-risk VIP list

Build a segment of users named "At-Risk VIP Customers".
A user is in the segment only when all of these are true:
- their Lifetime value attribute is more than 1000
- they did not do the Session start event in the last 30 days

## Step 2: Draft a personal check-in

Generate a plain-text email for the users in "At-Risk VIP Customers" written as a personal note from their account manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the at-risk VIP list".

## Step 3: Alert the retention team

Generate a Slack message to the channel chosen for this run listing the users in "At-Risk VIP Customers" so the team can prioritize outreach to the highest-value accounts first. Use the result of "Build the at-risk VIP list".
