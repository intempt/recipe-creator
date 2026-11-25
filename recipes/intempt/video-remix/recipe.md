---
frontmatter_id: video-remix
slash_command: /video-remix
description: Pin one reference image and get back a short branded video clip anchored to it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns one reference image into a short branded video clip that keeps its subject, look and framing.
  parameters:
  - name: clip_style
    type: enum
    label: Motion style
    default: slow camera push-in
    required: false
    options:
    - slow camera push-in
    - gentle orbit
    - handheld drift
    - static camera, subject moves
  requirements:
  - slot: reference_clip
    kind: knowledge
    meaning: The reference image (a scene, product or brand image) the clip is anchored to
  - slot: brand_identity
    kind: brand
    meaning: The project's brand colours and look, used to keep the clip on-brand
    optional: true
  steps:
  - id: s1
    builds: video
    uses:
    - reference_clip
    - brand_identity
    - clip_style
    instruction: Generate one short video clip from {reference_clip}. Keep its subject, composition and colours, and animate
      it with a {clip_style}. Match the colours and look of {brand_identity}. No text on screen, no people speaking, no visible
      cut.
---

# Reference-anchored video remix

Slash command: /video-remix

## Step 1: Remix the reference into a clip

Generate one short video clip from reference clip. Keep its subject, composition and colours, and animate it with a slow camera push-in. Match the colours and look of brand identity. No text on screen, no people speaking, no visible cut.
