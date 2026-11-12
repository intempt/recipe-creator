---
frontmatter_id: video-remix
slash_command: /video-remix
description: Pin one image reference and get back a branded reel variant anchored to it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Pins one image reference and generates several branded reel video variations anchored to that reference clip.
  parameters:
  - name: fanout
    type: number
    label: Number of variations
    default: 4
    required: false
  - name: reference_count
    type: number
    label: Number of video references
    default: 1
    required: false
  requirements:
  - slot: reference_clip
    kind: knowledge
    meaning: A reference video clip, scene, avatar, or product image to anchor generated variations
  - slot: brand_identity
    kind: brand
    meaning: The project's brand assets used to keep generated reels on-brand
    optional: true
  steps:
  - id: s1
    builds: video
    uses:
    - reference_clip
    - brand_identity
    - fanout
    - reference_count
    instruction: Generate {fanout} branded reel video variations anchored to the {reference_clip} references, using up to
      {reference_count} video reference(s) and the {brand_identity} assets, with the Kling v3 image-to-video multi-reference
      pipeline.
---

# Reference-anchored video remix

Slash command: /video-remix

## Step 1: Pin clips and fan out

Generate branded video variations from reference pins.
Inputs:
- references: 1: 4 video references (clip, scene, avatar, product)
- fanout: number of variations (default: 4)
Pipeline: kling v3 i2v multi-ref
Runner: video-remix (custom)
Fan out branded reel variants anchored to the reference clips.
