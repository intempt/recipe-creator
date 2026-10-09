---
description: Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes something a sales team can run against.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
  - media
---

# Segment into a Salesforce campaign

Slash command: /salesforce-segment-to-campaign

## Step 1: Define the audience once

Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating it in Salesforce, so there is one answer to who is in the audience.

## Step 2: Add members without doubling

Create a workflow that adds each member to the named Salesforce campaign with a campaign member status. Adding is idempotent (a member already in the campaign is left alone rather than duplicated) and removal is deliberately not part of this recipe, because campaign membership is a record of who was contacted and deleting it destroys attribution. Use the result of "Define the audience once".
