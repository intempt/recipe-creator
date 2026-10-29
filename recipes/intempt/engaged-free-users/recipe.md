---
frontmatter_id: engaged-free-users
slash_command: /engaged-free-users
description: Free-plan users logging in often enough to be ready for a paid plan, offered the upgrade by email and queued for growth outreach.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Engaged free users

Slash command: /engaged-free-users

## Step 1: Build the engaged free list

Build a segment of users named "Engaged Free Users".
A user is in the segment only when all of these are true:
- their Plan attribute is "free"
- they did the Session start event 5 or more times in the last 14 days

## Step 2: Send an upgrade email

Generate a designed marketing email for the users in "Engaged Free Users" introducing the paid plan's feature most relevant to someone already using the product this often. Three sentences, encouraging tone, no discount language, one button linking to the pricing page. Use the result of "Build the engaged free list".

## Step 3: Notify growth

Generate a plain-text email to the growth team distribution list listing the users in "Engaged Free Users" so outreach can be prioritized by how active each one already is. Use the result of "Build the engaged free list".
