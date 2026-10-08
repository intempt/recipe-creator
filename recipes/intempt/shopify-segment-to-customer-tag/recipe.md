---
description: Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against it.
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
  - ecommerce
  - media
---

# Tag Shopify customers from a segment

Slash command: /shopify-segment-to-customer-tag

## Step 1: Define the cohort to tag

Create the segment to tag: high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify.

## Step 2: Write the tag into Shopify

Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify's own rejection is surfaced verbatim: a tag limit and a permission error need different responses. Use the result of "Define the cohort to tag".
