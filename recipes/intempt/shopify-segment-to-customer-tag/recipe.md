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
portable:
  summary: Tags Shopify customers who belong to a chosen segment so the store can merchandise against that group, keeping
    the tag in sync with the segment.
  parameters:
  - name: tag_name
    type: string
    label: Shopify tag to write on members
    default: <UNKNOWN>
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
  - slot: tagged_cohort
    kind: segment
    meaning: The customer cohort to tag in Shopify
    creatable: true
    definition: users matching {cohort_rule}
  steps:
  - id: s1
    builds: segment
    uses:
    - cohort_rule
    - customer_profile
    instruction: Create the segment {tagged_cohort} of users matching {cohort_rule}. The segment is the definition; the Shopify
      tag is only its shadow in the store.
  - id: s2
    builds: automation
    uses:
    - s1
    - tagged_cohort
    - shopify_store
    - tag_name
    instruction: 'Create a workflow that adds the tag {tag_name} to each member of {tagged_cohort} in {shopify_store}. Tags
      are additive, and the workflow manages only the tag {tag_name}, so tags edited by hand in Shopify are not overwritten.
      Surface Shopify''s rejection verbatim: a tag limit error and a permission error must be reported separately and handled
      differently. Use the result of "Define the cohort to tag".'
---

# Tag Shopify customers from a segment

Slash command: /shopify-segment-to-customer-tag

## Step 1: Define the cohort to tag

Create the segment to tag: high lifetime value, repeat buyer, lapsed, whatever the store wants to treat differently. The segment is the definition; the tag is only its shadow in Shopify.

## Step 2: Write the tag into Shopify

Create a workflow that tags each member in Shopify. Tags are additive and the workflow states which tag it manages, because a tag the store team also edits by hand will otherwise be fought over silently. Shopify's own rejection is surfaced verbatim: a tag limit and a permission error need different responses. Use the result of "Define the cohort to tag".
