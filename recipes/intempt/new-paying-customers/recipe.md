---
frontmatter_id: new-paying-customers
slash_command: /new-paying-customers
description: Customers who started paying in the last month, welcomed by email and flagged to customer success during the window where onboarding decides whether they stay.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# New paying customers

Slash command: /new-paying-customers

## Step 1: Build the new-customer list

Build a segment of users named "New Paying Customers".
A user is in the segment only when all of these are true:
- they did the Subscription started event at least once in the last 30 days
- their Plan attribute is not "free"
- their Plan attribute is not "trial"

## Step 2: Send a welcome email

Generate a designed marketing email for the users in "New Paying Customers" welcoming them and highlighting one feature worth trying in their first week. Three sentences, warm tone, no upsell language, one button linking to that feature inside the product. Use the result of "Build the new-customer list".

## Step 3: Notify customer success

Generate a plain-text email to the customer success distribution list listing the users in "New Paying Customers" so the team can check in personally during their first week. Use the result of "Build the new-customer list".
