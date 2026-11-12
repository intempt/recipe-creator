---
frontmatter_id: ugc-selfie-video
slash_command: /ugc-selfie-video
description: Turns a handheld selfie still into a 5 second candid clip with a subtle head turn and a natural smile.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - social-creator
portable:
  summary: Turns a handheld selfie still into a 5-second candid UGC-style clip with a subtle head turn and a natural smile.
  parameters:
  - name: clip_length
    type: duration
    label: Clip length
    default: 5 s
    required: false
  - name: motion_style
    type: enum
    label: Motion style
    default: candid
    required: false
    options:
    - candid
    - subtle
    - energetic
  - name: lighting_note
    type: text
    label: Lighting and feel
    default: real kitchen light, slight handheld drift. Authentic, not glamour.
    required: false
  requirements:
  - slot: selfie_still
    kind: knowledge
    meaning: A handheld selfie still image to animate into a video clip
  steps:
  - id: s1
    builds: video
    uses:
    - selfie_still
    - clip_length
    - lighting_note
    - motion_style
    instruction: Generate a UGC selfie video from the {selfie_still} still image. Seed the generation on the selfie still.
      Produce a {clip_length} candid handheld selfie clip with a subtle head turn and a natural smile, using {lighting_note}.
      Use image-to-video with candid motion in {motion_style} style.
---

# UGC selfie clip

Slash command: /ugc-selfie-video

## Step 1: Animate the selfie

Generate a UGC selfie video from a still.
Seed on the selfie still. 5s candid handheld selfie clip: subtle head turn, natural smile, real kitchen light, slight handheld drift. Authentic, not glamour.
Pipeline: image to video (candid motion)
