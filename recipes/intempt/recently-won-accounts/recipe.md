---
frontmatter_id: recently-won-accounts
slash_command: /recently-won-accounts
description: Accounts whose users just started paying, welcomed with an onboarding kickoff email and handed to the onboarding team while the account is still new.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Recently won accounts

Slash command: /recently-won-accounts

## Step 1: Build the recently-won list

Build a segment of accounts named "Recently-Won Accounts".
An account is in the segment only when all of these are true:
- the users in the account together did the Subscription started event at least once in the last 30 days

## Step 2: Send an onboarding kickoff email

Generate a designed marketing email for the accounts in "Recently-Won Accounts" welcoming the team and pointing to the first milestone worth hitting. Three sentences, warm and encouraging tone, no discount language, one button linking to the onboarding guide. Use the result of "Build the recently-won list".

## Step 3: Notify onboarding

Generate a plain-text email to the onboarding team distribution list listing the accounts in "Recently-Won Accounts" so implementation starts from one current list. Use the result of "Build the recently-won list".
