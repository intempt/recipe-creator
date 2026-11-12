---
frontmatter_id: product-shot-video
slash_command: /product-shot-video
description: Turn a static product image into a 5-second video clip with a 360 spin, dolly-in, or floating reveal.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a static product image into a 5-second video clip with a 360° spin, dolly-in, or floating reveal, with an
    optional music bed.
  parameters:
  - name: scene
    type: enum
    label: Motion style
    default: 360° rotation
    required: false
    options:
    - 360° rotation
    - dolly-in
    - floating reveal
  - name: script
    type: text
    label: Additional direction (optional)
    required: false
  - name: music
    type: boolean
    label: Enable music bed
    default: true
    required: false
  - name: clip_length
    type: duration
    label: Clip length
    default: 5 s
    required: false
  requirements:
  - slot: product_catalog
    kind: product_feed
    meaning: A catalog of products with product images that the clip is generated from
  steps:
  - id: s1
    builds: video
    uses:
    - product_catalog
    - scene
    - script
    - music
    - clip_length
    instruction: Generate a product shot video from the static image of {product_catalog}. Produce a {clip_length} clip using
      the motion style {scene}, with optional direction {script}. If {music} is enabled, add a music bed to the clip.
---

# Product clip from a still

Slash command: /product-shot-video

## Step 1: Animate the product

Generate a product shot video from a static image.
Inputs:
- productId: catalog product
- scene: motion style (360° rotation, dolly-in, floating reveal)
- script (optional): additional direction
- music: enable music bed (default: true)
Pipeline: kling i2v + mmaudio-v2
Produce a 5-second clip (360° rotation, dolly-in, or floating reveal) with optional music bed.
