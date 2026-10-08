---
description: Generates each shot in your shot list as a separate Kling v3 text-to-video clip. Use the merge-video workflow node to join clips into one reel.
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

# Multi-shot video from a shot list

Slash command: /multi-shot

## Step 1: Render and join the shots

Generate a multi-shot video from a shot list.
Inputs:
- shotList: one prompt per shot (multi-string)
- scene: shared scene/look across all shots
- durationPerShot: 3s or 5s per shot
Pipeline: kling v2.1 master t2v × N + concat
Render each shot with consistent visual style, then concatenate into a single reel.
