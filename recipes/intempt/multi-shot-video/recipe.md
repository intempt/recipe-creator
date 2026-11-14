---
frontmatter_id: multi-shot-video
slash_command: /multi-shot-video
description: Generates each shot in your shot list as its own text-to-video clip with a shared look, then joins the clips in order into one reel.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns a list of shot prompts into separate AI video clips with a shared look, then joins them into one finished
    reel.
  parameters:
  - name: shotList
    type: text
    label: Shot list (one prompt per shot)
    required: true
  - name: scene
    type: text
    label: Shared scene and look across all shots
    required: true
  - name: durationPerShot
    type: enum
    label: Duration per shot
    default: 5 s
    options:
    - 3 s
    - 5 s
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - shotList
    - scene
    - durationPerShot
    instruction: Generate one text-to-video clip for each prompt in {shotList}, using {scene} as the shared scene and visual
      style for every shot, with each clip set to {durationPerShot}. Render all shots with a consistent look, then concatenate
      the clips in shot-list order into a single reel.
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
