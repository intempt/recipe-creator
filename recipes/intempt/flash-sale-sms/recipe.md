---
frontmatter_id: flash-sale-sms
slash_command: /flash-sale-sms
description: Builds the list of recently active shoppers, drafts a time-limited offer text without inventing a discount or deadline it does not have, and drafts a reach note for marketing ops to review before anything sends.
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
portable:
  summary: Builds a list of recently active shoppers, drafts a time-limited flash sale text with no invented discount or deadline,
    and drafts a reach note for marketing ops to review before sending.
  parameters:
  - name: view_threshold
    type: number
    label: Minimum page views in the window
    default: 3
    required: false
  - name: view_window
    type: duration
    label: Lookback window for page views
    default: 7 d
    required: false
  - name: discount_percentage
    type: number
    label: Discount percentage for this run
    required: true
  - name: offer_end_date
    type: date
    label: Offer end date for this run
    required: true
  - name: sms_tone
    type: enum
    label: Tone of the SMS
    default: direct and urgent
    required: false
    options:
    - direct and urgent
    - friendly
    - neutral
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a page on the website
  - slot: marketing_ops_channel
    kind: integration
    meaning: Slack workspace with a marketing ops channel where reach notes are posted
    channel: slack
  - slot: sms_destination
    kind: destination
    meaning: An SMS channel able to reach shoppers
    channel: sms
  - slot: flash_sale_audience
    kind: segment
    meaning: Shoppers who viewed a page at least a set number of times in a recent window
    creatable: true
    definition: users who did {page_view_event} at least {view_threshold} times in the last {view_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - page_view_event
    - view_threshold
    - view_window
    instruction: Build a segment named "Flash Sale Audience" ({flash_sale_audience}). A user is in the segment only when they
      triggered {page_view_event} at least {view_threshold} times in the last {view_window}.
  - id: s2
    builds: sms
    uses:
    - s1
    - discount_percentage
    - offer_end_date
    - sms_tone
    - sms_destination
    instruction: Generate an SMS for the users in {flash_sale_audience} announcing a limited-time {discount_percentage}% discount
      on their next purchase, ending {offer_end_date}. Include a short.link preview card for the offer's landing page. Write
      one or two sentences in a {sms_tone} tone. Use the result of "Build the flash-sale audience". This drafts the SMS only;
      a person still sends it.
  - id: s3
    builds: slack
    uses:
    - s1
    - marketing_ops_channel
    instruction: Generate a Slack message to the marketing ops channel ({marketing_ops_channel}) noting the size of {flash_sale_audience}
      so the team can track reach before the sale goes out. Use the result of "Build the flash-sale audience". This drafts
      the Slack message only; a person on the team still posts it.
---

# Flash sale text message

Slash command: /flash-sale-sms

## Step 1: Build the flash-sale audience

Build a segment of users named "Flash Sale Audience". A user is in the segment only when all of these are true: triggered "View page" at least 3 times in the last 7 days.

## Step 2: Write the flash sale SMS

Generate an SMS for the users in "Flash Sale Audience" announcing a limited-time discount on their next purchase. Use the discount percentage and the offer's end date chosen for this run; do not invent either if neither is supplied. Include a short.link preview card for the offer's landing page. One or two sentences, direct and urgent tone. Use the result of "Build the flash-sale audience". This drafts the SMS only; a person still sends it.

## Step 3: Draft a note for marketing ops

Generate a Slack message to the marketing ops channel noting the size of "Flash Sale Audience" so the team can track reach before the sale goes out. Use the result of "Build the flash-sale audience". This drafts the Slack message only; a person on the team still posts it.
