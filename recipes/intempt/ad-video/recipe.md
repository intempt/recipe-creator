---
frontmatter_id: ad-video
slash_command: /ad-video
description: Turns one product still into a 5 second cinematic spot using Kling image to video, with no text or logo.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns one product still into a 5-second cinematic product video with subtle camera drift and soft dust, keeping
    the same backdrop and no text or logo.
  parameters:
  - name: clip_length
    type: duration
    label: Clip length
    default: 5 s
    required: false
  - name: camera_motion
    type: string
    label: Camera motion
    default: smooth subtle camera drift
    required: false
  - name: ambient_effect
    type: string
    label: Ambient effect
    default: soft dust particles
    required: false
  requirements:
  - slot: product_still
    kind: attribute
    meaning: A product still image to animate into the video
  steps:
  - id: s1
    builds: video
    uses:
    - product_still
    - clip_length
    - camera_motion
    - ambient_effect
    instruction: Generate a cinematic ad video from {product_still}. Seed the generation on the product still. Produce a cinematic
      {clip_length} product spot with {camera_motion}, {ambient_effect}, and the same backdrop as the still. No text and no
      logo overlay. Use an image-to-video pipeline (Kling or Seedance).
---

# Cinematic ad spot

Slash command: /ad-video

## Step 1: Animate the product still

Generate a cinematic ad video from a product still.
Seed on the product still. Produce a cinematic 5s product spot with smooth subtle camera drift, soft dust particles, same backdrop. No text, no logo overlay.
Pipeline: image to video (kling/seedance)
