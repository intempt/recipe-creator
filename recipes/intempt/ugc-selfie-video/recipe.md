---
frontmatter_id: ugc-selfie-video
slash_command: /ugc-selfie-video
description: Makes a candid UGC-style selfie clip of your brand character saying the words you write.
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
  summary: Makes a 5-second candid UGC-style selfie clip of your brand character saying the words you write, with a subtle
    head turn and a natural smile.
  parameters:
  - name: script
    type: text
    label: What the character says (at least a sentence or two)
    required: true
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
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - script
    - clip_length
    - lighting_note
    - motion_style
    instruction: Make a UGC selfie video of the brand's presenter character saying {script}. Produce a {clip_length} candid
      handheld selfie clip with a subtle head turn and a natural smile, using {lighting_note}, in {motion_style} style.
---

# UGC selfie clip

Slash command: /ugc-selfie-video

## Step 1: Animate the selfie

Generate a UGC selfie video of the brand character (never an uploaded photo of a real person) saying your words. 5s candid handheld selfie clip: subtle head turn, natural smile, real kitchen light, slight handheld drift. Authentic, not glamour.
Pipeline: image to video (candid motion)
