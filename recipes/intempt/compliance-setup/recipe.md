---
description: A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.
author:
  first_name: Harish
  last_name: Kumar
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/harish.jpg
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
- they have never done the consent_granted event
- they did the consent_revoked event after their most recent consent_granted event
