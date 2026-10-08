---
description: Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene on its own, with voice and music.
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
