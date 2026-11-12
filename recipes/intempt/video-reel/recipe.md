---
frontmatter_id: video-reel
slash_command: /video-reel
description: Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene on its own, with voice and music.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Creates a 5 or 10 second short video reel from a script, featuring your avatar, a catalog product, or a scene alone,
    with voice and music.
  parameters:
  - name: subjectMode
    type: enum
    label: Subject mode
    default: Avatar
    required: false
    options:
    - Avatar
    - Product
    - Scene-only
  - name: duration
    type: enum
    label: Reel duration
    default: 5s
    required: false
    options:
    - 5s
    - 10s
  - name: script
    type: text
    label: Script or prompt
    required: true
  requirements:
  - slot: avatar_model
    kind: knowledge
    meaning: An identity-locked avatar model of a person to appear in the reel (used in Avatar mode)
    optional: true
  - slot: product_catalog
    kind: product_feed
    meaning: A catalog of products whose SKUs anchor the first frame of the reel (used in Product mode)
    optional: true
  - slot: background_scene
    kind: knowledge
    meaning: A background scene image or setting for the reel (optional)
    optional: true
  steps:
  - id: s1
    builds: video
    uses:
    - avatar_model
    - product_catalog
    - background_scene
    - subjectMode
    - duration
    - script
    instruction: Generate a short video reel using {subjectMode} mode and a {duration} duration, based on {script}. In Avatar
      mode, lock the {avatar_model} identity in the first frame. In Product mode, use the selected SKUs from {product_catalog}
      to anchor the first frame. In Scene-only mode, generate from text alone. Optionally place the subject in {background_scene}.
      Add voice narration and music.
---

# Short video reel

Slash command: /video-reel

## Step 1: Generate the reel

Generate a short video reel.
Inputs:
- subjectMode: Avatar | Product | Scene-only
- modelId (if Avatar): identity-locked Avatar
- productIds (if Product): catalog SKUs
- sceneId (optional): background scene
- script: script or prompt (rich text)
- duration: 5s or 10s
Pipeline: kling v2.1 i2v + elevenlabs-tts
Runner: video-reel (custom)
In Avatar mode, the Avatar is identity-locked in the first frame with voice + music. In Product mode, the catalog SKU anchors the first frame. Scene-only uses text-to-video.
