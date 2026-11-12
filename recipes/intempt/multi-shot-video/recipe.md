---
frontmatter_id: multi-shot-video
slash_command: /multi-shot-video
description: Generates each shot in your shot list as a separate Kling v3 text-to-video clip. Use the merge-video workflow node to join clips into one reel.
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
  requirements:
  - slot: video_generation_integration
    kind: integration
    meaning: A connected AI text-to-video generation service capable of rendering clips from text prompts
    channel: email
  - slot: video_merge_destination
    kind: destination
    meaning: A destination where the joined final reel can be delivered or stored
    optional: true
    channel: email
  steps:
  - id: s1
    builds: video
    uses:
    - shotList
    - scene
    - durationPerShot
    - video_generation_integration
    - video_merge_destination
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
