---
description: "Customers who cancelled in the last month, sent a win-back email and flagged to the retention team while the reason is still fresh."
frontmatter_id: recently-churned-users
author:
  name: V
  last_name: Ranadheer
  org_name: intempt
  email: rana@intempt.com
---
# Recently cancelled customers

## Step 1: Build the recent-cancel list

Build a segment of users named "Recently Churned Users". A user is in the segment only when all of these are true: they did the Subscription canceled event at least once in the last 30 days, their Lifetime value attribute is more than 0.

## Step 2: Draft a win-back email

Generate a designed marketing email for the users in "Recently Churned Users" inviting them back. Three sentences, warm and non-defensive tone, asking what did not work and offering to help, no discount language, one button linking to the page for restarting their subscription. Use the result of "Build the recent-cancel list".

## Step 3: Notify the retention team

Generate a Slack message to the retention team channel listing the users in "Recently Churned Users" so the team can track cancellation volume and follow up personally with the highest-value ones. Use the result of "Build the recent-cancel list".
