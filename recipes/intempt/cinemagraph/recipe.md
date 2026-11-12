---
frontmatter_id: cinemagraph
slash_command: /cinemagraph
description: Turns a still photo into a looping clip where one element moves, such as steam or a pour, and everything else stays frozen.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a still photo into a seamless looping clip where one element, such as steam or a pour, moves while everything
    else stays frozen.
  parameters:
  - name: animated_element
    type: enum
    label: Element that moves
    default: gentle steam
    required: false
    options:
    - gentle steam
    - single leaf in breeze
    - liquid pour
  - name: motion_intensity
    type: enum
    label: Motion intensity
    default: subtle
    required: false
    options:
    - subtle
    - moderate
    - strong
  requirements:
  - slot: source_still_image
    kind: knowledge
    meaning: A still photo supplied by the customer to be turned into a looping clip
  steps:
  - id: s1
    builds: video
    instruction: 'Generate a cinemagraph from {source_still_image}. Keep the camera fixed. Keep everything frozen except one
      element: {animated_element}. Use {motion_intensity} motion with a subtle hypnotic loop and no visible cut.'
---

# Cinemagraph loop

Slash command: /cinemagraph

## Step 1: Animate one element

Generate a cinemagraph from a still image.
Camera stays fixed. Everything stays frozen except one element (gentle steam, single leaf in breeze, liquid pour). Subtle hypnotic loop with no visible cut.
Pipeline: image to video (camera-fixed, loop)
