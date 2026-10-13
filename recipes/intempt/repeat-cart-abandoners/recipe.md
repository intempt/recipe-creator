---
frontmatter_id: repeat-cart-abandoners
slash_command: /repeat-cart-abandoners
description: People who have walked away from checkout twice or more this month without buying, usually a sign of friction or price resistance.
author:
  name: Harish Kumar
  first_name: Harish
  last_name: Kumar
  company: Intempt
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
  org_name: intempt
classification:
  industry:
  - ecommerce
---

# Repeat cart abandoners

Slash command: /repeat-cart-abandoners

## Step 1: Build the repeat-abandoner list

Build a segment of users named "Repeat Cart Abandoners".
A user is in the segment only when all of these are true:
- they did the Abandoned checkout event 2 or more times in the last 30 days
- they did not do the Placed order event in the last 30 days
