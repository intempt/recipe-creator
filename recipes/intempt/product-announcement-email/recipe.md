---
frontmatter_id: product-announcement-email
slash_command: /product-announcement-email
description: Writes a launch-day email in your brand colors and fonts, with the product hero image and a subject line written for opens and clicks.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Creates a launch-day announcement email in your brand colors and fonts, with the product hero image and a subject
    line written to drive opens and clicks.
  parameters:
  - name: tone
    type: string
    label: Tone of the announcement copy
    default: excited
  requirements:
  - slot: brand_kit
    kind: brand
    meaning: The project's brand kit with brand colors, fonts and logo
  - slot: featured_product_feed
    kind: product_feed
    meaning: A product catalog feed containing the product being launched with its hero image
  steps:
  - id: s1
    builds: email
    uses:
    - brand_kit
    - featured_product_feed
    - tone
    instruction: 'Create a product announcement email. Apply the brand tokens from {brand_kit} (colors, fonts, logo). Include
      a product hero block with the featured product image from {featured_product_feed}. Write an announcement subject line
      and body copy optimized for open rate and click-through, in a {tone} tone. Output: ready-to-send email template.'
---

# Product launch announcement email

Slash command: /product-announcement-email

## Step 1: Write the announcement email

Create a product announcement email.
Apply the project's brand tokens (colors, fonts, logo). Include a product hero block with the featured product image. Write an announcement subject line and body copy optimized for open rate and click-through.
Output: ready-to-send email template
