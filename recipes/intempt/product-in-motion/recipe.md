---
frontmatter_id: product-in-motion
slash_command: /product-in-motion
description: Turns a product packshot into a slow 360 degree turntable spin video on the same backdrop.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a product packshot into a slow 360-degree turntable spin video on the same backdrop, with a fixed camera
    and no text or logo.
  parameters:
  - name: rotation_style
    type: string
    label: Rotation style
    default: slow elegant turntable rotation
    required: false
  - name: luxury_tone
    type: string
    label: Visual tone
    default: Luxury e-commerce 360° spin
    required: false
  requirements:
  - slot: product_packshot
    kind: knowledge
    meaning: A product packshot image to be turned into a spin video
  steps:
  - id: s1
    builds: video
    uses:
    - product_packshot
    - rotation_style
    - luxury_tone
    instruction: 'Generate a product turntable spin video from {product_packshot}. Camera fixed. Apply {rotation_style} of
      the product on the same backdrop. Style: {luxury_tone}. No text, no logo. Pipeline: image to video (camera-fixed, turntable).'
---

# Turntable product spin

Slash command: /product-in-motion

## Step 1: Spin the product

Generate a product turntable spin video.
Camera fixed. Slow elegant turntable rotation of the product, same backdrop. Luxury e-commerce 360° spin. No text, no logo.
Pipeline: image to video (camera-fixed, turntable)
