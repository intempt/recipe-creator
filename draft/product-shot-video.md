---
description: Turn a static product image into a 5-second video clip with a 360 spin, dolly-in, or floating reveal.
author:
  first_name: Aurobind
  last_name: Venu
  job_title: Creative Director
  company: Intempt
org_name: intempt
classification:
  industry:
  - b2b-saas
  - ecommerce
  - media
  - social
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
