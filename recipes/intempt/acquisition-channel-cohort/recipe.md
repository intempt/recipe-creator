---
frontmatter_id: acquisition-channel-cohort
slash_command: /acquisition-channel-cohort
description: Visitors who keep coming back to the same pages, tagged with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Repeat Page Visitors

Slash command: /acquisition-channel-cohort

## Step 1: Build the repeat visitor list

Build a segment of users named "Repeat Page Visitors". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "repeat_visitor" on users in "Repeat Page Visitors", set to true. Use the result of "Build the repeat visitor list".
