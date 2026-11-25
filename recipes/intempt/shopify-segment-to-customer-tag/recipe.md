---
frontmatter_id: shopify-segment-to-customer-tag
slash_command: /shopify-segment-to-customer-tag
description: Pushes a cohort computed here onto Shopify customers as a tag, so the store can merchandise against it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
prerequisites:
  integrations:
    - { value: shopify, severity: blocking }
portable:
  summary: Tags Shopify customers who belong to a chosen segment so the store can merchandise against that group, keeping
    the tag in sync with the segment.
  parameters:
  - name: tag_name
    type: string
    label: Shopify tag to write on members
    required: true
  - name: cohort_rule
    type: text
    label: Rule defining the cohort (e.g. high lifetime value, repeat buyer, lapsed)
    default: high lifetime value
    required: false
  requirements:
  - slot: customer_profile
    kind: attribute
    meaning: A customer profile record that can be matched to a Shopify customer
  - slot: shopify_store
    kind: integration
    meaning: A connected Shopify store where customer tags can be written
    channel: shopify
  steps:
  - id: s1
    builds: segment
    uses:
    - cohort_rule
    - customer_profile
    instruction: Build a new segment named "Cohort to Tag" of users matching {cohort_rule}.
  - id: s2
    builds: automation
    uses:
    - s1
    - shopify_store
    - tag_name
    dependsOn:
    - s1
    instruction: 'Create a workflow that adds the tag {tag_name} to each member of the segment from "Define the cohort to
      tag" in {shopify_store}. Tags are additive, and the workflow manages only the tag {tag_name}, so tags edited by hand
      in Shopify are not overwritten. Surface Shopify''s rejection verbatim: a tag limit error and a permission error must
      be reported separately and handled differently. Use the result of "Define the cohort to tag".'
---

# Tag Shopify customers from a segment

Slash command: /shopify-segment-to-customer-tag

## Step 1: Define the cohort to tag

Build a new segment named "Cohort to Tag" of users matching high lifetime value.

## Step 2: Write the tag into Shopify

Create a workflow that adds the tag the shopify tag to write on members to each member of the segment from "Define the cohort to tag" in shopify store. Tags are additive, and the workflow manages only the tag the shopify tag to write on members, so tags edited by hand in Shopify are not overwritten. Surface Shopify's rejection verbatim: a tag limit error and a permission error must be reported separately and handled differently. Use the result of "Define the cohort to tag".
