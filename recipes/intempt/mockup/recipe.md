---
frontmatter_id: mockup
slash_command: /mockup
description: Visitors returning on a near-daily basis, tagged as a power-user pool and invited into an early-access or loyalty list.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Daily Habit Visitors

Slash command: /mockup

## Step 1: Build the daily habit visitor list

Build a segment of users named "Daily Habit Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 4 times in the last 4 days.

## Step 2: Tag the matched visitors

Create an attribute named "daily_habit_user" on users in "Daily Habit Visitors", set to true. Use the result of "Build the daily habit visitor list".

## Step 3: Invite them to early access

Generate a designed marketing email for the users in "Daily Habit Visitors" inviting them into an early-access or loyalty list in recognition of how often they show up. Three sentences, warm and appreciative tone, no discount language, one button to join. Use the result of "Build the daily habit visitor list".
