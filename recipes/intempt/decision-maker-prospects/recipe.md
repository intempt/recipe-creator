---
frontmatter_id: decision-maker-prospects
slash_command: /decision-maker-prospects
description: Customers who have paid for a year or two straight, invited into loyalty recognition by email and flagged to customer marketing for a testimonial or case study.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Long-time loyal customers

Slash command: /decision-maker-prospects

## Step 1: Build the loyal-customer list

Build a segment of users named "Long-Time Loyal Customers".
A user is in the segment only when all of these are true:
- their Plan attribute is not "free"
- they did the Subscription started event at least once between 365 and 730 days ago

## Step 2: Send a loyalty recognition email

Generate a designed marketing email for the users in "Long-Time Loyal Customers" thanking them for their continued support and inviting them into loyalty recognition. Three sentences, warm and appreciative tone, no discount language, one button linking to the loyalty or referral page. Use the result of "Build the loyal-customer list".

## Step 3: Alert customer marketing

Generate a Slack message to the channel chosen for this run listing the users in "Long-Time Loyal Customers" as candidates for a testimonial or case study. Use the result of "Build the loyal-customer list".
