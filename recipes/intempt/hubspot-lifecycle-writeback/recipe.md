---
frontmatter_id: hubspot-lifecycle-writeback
slash_command: /hubspot-lifecycle-writeback
description: Pushes the lifecycle stage computed from real product and billing behaviour onto the HubSpot contact, so sales and marketing read the same thing.
author:
  name: Trishik Shrestha
  first_name: Trishik
  last_name: Shrestha
  company: Intempt
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
---

# Write lifecycle back to HubSpot

Slash command: /hubspot-lifecycle-writeback

## Step 1: Define the lifecycle honestly

Create the lifecycle attribute from product and billing reality (trialing, active, at risk, churned) rather than from whatever a form last said. This is the value worth having in two systems.

## Step 2: Push it one way to HubSpot

Create a workflow updating the HubSpot contact property when the lifecycle changes. The direction is one way on this field: Intempt owns it, HubSpot displays it. A field written from both sides needs a stated winner, and pretending otherwise is how a CRM and a CDP quietly disagree for months. Use the result of "Define the lifecycle honestly".
