---
frontmatter_id: acquisition-channel-cohort
slash_command: /acquisition-channel-cohort
description: Customers grouped by the channel that brought them in, so you can compare how well each channel's buyers stick around.
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
portable:
  summary: Builds a segment of the users a paid search channel brought in who went on to place an order, so you can compare
    how well each channel's buyers stick around.
  parameters:
  - name: utmSource
    type: string
    label: Acquisition source for this cohort
    default: google
    required: false
  - name: utmMedium
    type: string
    label: Acquisition medium for this cohort
    default: cpc
    required: false
  requirements:
  - slot: utm_source
    kind: attribute
    meaning: The source that first brought the user in
  - slot: utm_medium
    kind: attribute
    meaning: The medium that first brought the user in
  - slot: order_created
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: segment
    uses:
    - utm_source
    - utm_medium
    - order_created
    - utmSource
    - utmMedium
    instruction: 'Build a new segment of users named "Google Paid Acquired". A user is in the segment only when all of these
      are true: {utm_source} is {utmSource}; {utm_medium} is {utmMedium}; and they did {order_created} at least once, at any
      time.'
---

# Customers by acquisition channel

Slash command: /acquisition-channel-cohort

## Step 1: Build the channel cohort

Build a new segment of users named "Google Paid Acquired". A user is in the segment only when all of these are true: utm source is google; utm medium is cpc; and they did order created at least once, at any time.
