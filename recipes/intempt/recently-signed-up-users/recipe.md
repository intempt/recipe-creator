---
frontmatter_id: recently-signed-up-users
slash_command: /recently-signed-up-users
description: Everyone whose first session was within the last 30 days, welcomed by email and flagged to the onboarding team while the activation window is still open.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Recent signups

Slash command: /recently-signed-up-users

## Step 1: Build the new signup list

Build a segment of users named "Recently Signed-Up Users".
A user is in the segment only when all of these are true:
- they did the Session start event at least once in the last 30 days
- they did not do the Session start event more than 30 days ago

## Step 2: Send a welcome email

Generate a designed marketing email for the users in "Recently Signed-Up Users" welcoming them and pointing to the one action most worth taking in their first week. Three sentences, warm and encouraging tone, no discount language, one button linking to that action inside the product. Use the result of "Build the new signup list".

## Step 3: Notify onboarding

Generate a plain-text email to the onboarding team distribution list listing the users in "Recently Signed-Up Users" so the team can check in while the activation window is still open. Use the result of "Build the new signup list".
