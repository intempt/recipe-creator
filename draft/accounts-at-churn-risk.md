---
description: "Large paying accounts where nobody has logged in for a month, the clearest detectable churn signal, checked in on personally and flagged to the retention team before it's too late."
frontmatter_id: accounts-at-churn-risk
author:
  name: V
  last_name: Ranadheer
  org_name: intempt
  email: rana@intempt.com
---
# Paying accounts going quiet

## Step 1: Build the at-risk account list

Build a segment of accounts named "Accounts At Churn Risk". An account is in the segment only when all of these are true: its employees attribute is 100 or more, the users in the account together did not do the Session start event in the last 30 days.

## Step 2: Draft a personal check-in

Generate a plain-text email for the accounts in "Accounts At Churn Risk" written as a personal note from their customer success manager, asking how things are going and offering a quick call. Three sentences, warm and personal tone, no product pitch, no discount language. Use the result of "Build the at-risk account list".

## Step 3: Alert the retention team

Generate a Slack message to the retention team channel listing the accounts in "Accounts At Churn Risk" so the team can prioritize outreach before renewal conversations start. Use the result of "Build the at-risk account list".
