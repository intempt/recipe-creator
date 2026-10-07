---
frontmatter_id: recent-page-viewers-segment
slash_command: /recent-page-viewers-segment
description: This recipe helps marketers automatically identify and group users who have viewed any page on their site or app within the past week, making it easy to target recently active visitors.
author:
  name: Beso
  last_name: Gugushvili
  org_name: intempt-internal-use-only
---

# Recent Page Viewers

## Step 1: Create Recent Page Viewers Segment

Create a segment called "Recent Page Viewers" for users. Base it on the "View page" event — the default autotracked event that fires on every page load. Add one group with one condition: triggered "View page" at least once in the last 7 days.
