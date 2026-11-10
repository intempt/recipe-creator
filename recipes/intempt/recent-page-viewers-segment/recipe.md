---
frontmatter_id: recent-page-viewers-segment
slash_command: /recent-page-viewers-segment
description: This recipe helps marketers automatically identify and group users who have viewed any page on their site or app within the past week, tagging them with a reusable attribute so later segments and campaigns can target them without rebuilding the match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Recent Page Viewers Segment

Slash command: /recent-page-viewers-segment

## Step 1: Create Recent Page Viewers Segment

Create a segment called "Recent Page Viewers" for users. Base it on the "View page" event — the default autotracked event that fires on every page load. Add one group with one condition: triggered "View page" at least once in the last 7 days.

## Step 2: Tag the matched visitors

Create an attribute named "recent_page_viewer" on users in "Recent Page Viewers", set to true. Use the result of "Create Recent Page Viewers Segment".
