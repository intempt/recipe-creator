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
  summary: Creates a short video reel of your brand character presenting your script, with its voice and captions.
  parameters:
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
    label: Script (what the presenter says)
    required: true
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - duration
    - script
    instruction: Generate a short video reel of about {duration} with the brand's presenter character saying {script}.
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
