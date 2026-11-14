---
frontmatter_id: product-videos
slash_command: /product-videos
description: Make one short video clip of each product in a product feed, each animated from that product's own photo.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Makes one short video clip of each product in a product feed (up to 5 per run by default), each animated from that
    product's own photo with a 360° spin, dolly-in, or floating reveal.
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
  - name: clip_length
    type: duration
    label: Clip length
    default: 5 s
    required: false
  - name: products_per_run
    type: number
    label: Products per run (1 to 20; set when the recipe is published)
    default: 5
    required: false
  requirements:
  - slot: product_catalog
    kind: product_feed
    meaning: A product feed whose products, each with a product image, get one video clip each
  steps:
  - id: s1
    builds: video
    uses:
    - product_catalog
    - scene
    - script
    - clip_length
    - products_per_run
    instruction: For each product in {product_catalog} (up to {products_per_run} per run), generate one product video from that product's own image. Produce
      a {clip_length} clip per product using the motion style {scene}, with optional direction {script}.
---

# One video per product

Slash command: /product-videos

## Step 1: Animate each product

Generate one product video for each product of a product feed.
Inputs:
- product feed: the products to animate (up to 5 per run)
- scene: motion style (360° rotation, dolly-in, floating reveal)
- script (optional): additional direction
Pipeline: kling i2v, once per product
Produce a 5-second clip of each product from its own catalog photo.
