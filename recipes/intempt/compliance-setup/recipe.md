---
frontmatter_id: compliance-setup
slash_command: /compliance-setup
description: A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
---

# Marketing consent suppression list

Slash command: /compliance-setup

## Step 1: Build the suppression list

Build a segment of users named "Marketing Consent Suppression List".
A user is in the segment when any of these is true:
- they have never done the Subscribed consent event
- they did the Unsubscribed consent event after their most recent Subscribed consent event
