---
frontmatter_id: expansion-candidates
slash_command: /expansion-candidates
description: Users grouped by Plan for plan-based upgrade targeting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
---

# Users close to their plan limit

Slash command: /expansion-candidates

## Step 1: Build the near-limit list

Build a segment of users named "Expansion Candidates".
A user is in the segment only when all of these are true:
- their Plan attribute is not "enterprise"
- their Usage percentage attribute is 80 or more
