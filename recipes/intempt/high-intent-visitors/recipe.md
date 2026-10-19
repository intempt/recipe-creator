---
frontmatter_id: high-intent-visitors
slash_command: /high-intent-visitors
description: Free and unregistered users who read both your pricing and your docs in the last two weeks, the clearest sign somebody is close to buying.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# High-intent visitors

Slash command: /high-intent-visitors

## Step 1: Build the high-intent list

Build a segment of users named "High-Intent Visitors".
A user is in the segment only when all of these are true:
- they did the View page event with a Page URL that contains "/pricing" at least once in the last 14 days
- they did the View page event with a Page URL that contains "/docs" at least once in the last 14 days
- their Plan attribute is empty or is "free"
