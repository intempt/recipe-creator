---
description: Pin one image reference and get back a branded reel variant anchored to it.
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
