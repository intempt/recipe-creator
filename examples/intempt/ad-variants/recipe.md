---
frontmatter_id: ad-variants
slash_command: /ad-variants
description: Takes an ad you already have and returns six variants, one for each dimension you choose to vary.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Takes one ad you already have and produces six image variants, each changing a single element (headline, palette,
    background, model, call to action, or aspect ratio).
  parameters:
  - name: source_ad
    type: attachment
    label: Source ad image
    required: true
  requirements: []
  steps:
  - id: s1
    builds: image
    uses:
    - source_ad
    instruction: 'Generate six images from {source_ad}. Each image changes exactly one thing and keeps everything else from
      the original ad: one with a new headline; one with a new colour palette; one with a new background; one with a different
      model; one with a new call to action; one at a different aspect ratio.'
---

# Six variants of one ad

Slash command: /ad-variants

## Step 1: Fan out the variants

Generate six images from the ad image attached to this run.
Each image changes exactly one thing and keeps everything else from the original ad:
- one with a new headline
- one with a new colour palette
- one with a new background
- one with a different model
- one with a new call to action
- one at a different aspect ratio
