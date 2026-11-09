---
frontmatter_id: discount-only-buyers
slash_command: /discount-only-buyers
description: Visitors who have come back in more than one session, tagged with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Returning Visitors

Slash command: /discount-only-buyers

## Step 1: Build the returning visitor list

Build a segment of users named "Returning Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 2 times in the last 30 days.

## Step 2: Tag the matched visitors

Create an attribute named "returning_visitor" on users in "Returning Visitors", set to true. Use the result of "Build the returning visitor list".
