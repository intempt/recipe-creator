---
frontmatter_id: highly-active-multisession-visitors
slash_command: /highly-active-multisession-visitors
description: Visitors who return across several sessions and view many pages, tagged with a reusable attribute and flagged to growth as the strongest organic engagement signal available without any custom tracking.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Highly Active Multi-Session Visitors

Slash command: /highly-active-multisession-visitors

## Step 1: Build the highly active visitor list

Build a segment of users named "Highly Active Multi-Session Visitors". A user is in the segment only when all of these are true: triggered "Session start" at least 3 times in the last 30 days; triggered "View page" at least 5 times in the last 30 days.

## Step 2: Tag the matched visitors

Create an attribute named "power_browser" on users in "Highly Active Multi-Session Visitors", set to true. Use the result of "Build the highly active visitor list".

## Step 3: Alert growth

Generate a Slack message to the growth team channel. Say how many users are in "Highly Active Multi-Session Visitors" right now, so the team has a ready-made shortlist worth a closer look. Use the result of "Build the highly active visitor list".
