---
frontmatter_id: ugc-photo
slash_command: /ugc-photo
description: Re-shoots a studio packshot as a candid handheld phone photo of a real person holding the product.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: placeholder
  parameters:
  - name: setting
    type: enum
    label: Background setting
    default: kitchen or bathroom counter
    required: false
    options:
    - kitchen or bathroom counter
    - kitchen counter
    - bathroom counter
  - name: exposure
    type: enum
    label: Exposure
    default: slightly underexposed
    required: false
    options:
    - slightly underexposed
    - natural
    - underexposed
  requirements:
  - slot: product_packshot
    kind: product_feed
    meaning: A studio packshot image of the product to be photographed
  steps:
  - id: s1
    builds: image
    uses:
    - product_packshot
    - setting
    - exposure
    instruction: 'Edit the studio packshot {product_packshot}. Re-render it as a candid handheld selfie: a real person holding
      the same product at arm''s length, with a {setting} behind them, real skin texture, the face cropped at half, and {exposure}.
      Make it look authentic, not glamorous, and do not change the product.'
---

# UGC-style product photo

Slash command: /ugc-photo

## Step 1: Reshoot as a candid photo

Edit the studio packshot attached to this run.
Re-render it as a candid handheld selfie: a real person holding the same product at arm's length, a kitchen or bathroom counter behind them, real skin texture, the face cropped at half, and slightly underexposed.
Make it look authentic, not glamorous, and do not change the product.
