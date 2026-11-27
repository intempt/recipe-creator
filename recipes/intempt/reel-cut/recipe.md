---
frontmatter_id: reel-cut
slash_command: /reel-cut
description: Cut a saved clip into a 9:16 vertical reel, or animate a still picture into one.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Cuts a saved clip to a 9:16 reel; only a still picture gets a subtle push-in and drifting particles.
  parameters:
  - name: aspect_ratio
    type: string
    label: Output aspect ratio
    default: '9:16'
    required: false
  - name: motion_style
    type: string
    label: Motion style (still pictures only)
    default: subtle Ken Burns push with drifting motion particles
    required: false
  - name: source_clip
    type: string
    label: Clip or still to reframe
    default: the newest saved video in the project (else the newest saved picture)
    required: false
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - source_clip
    - aspect_ratio
    - motion_style
    instruction: Reformat {source_clip} into a {aspect_ratio} vertical reel. When {source_clip} is a video, analyze that video
      and cut the video itself to {aspect_ratio} (its own frames and sound, at most 30 s, the subject re-framed vertically);
      no new clip is generated from a frame of it. Only when {source_clip} is a still picture, animate it by image-to-video
      generation with a {motion_style}. Keep the output short-form and social-ready.
---

# Vertical reel cut

Slash command: /reel-cut

## Step 1: Reframe to 9:16

Reformat the newest saved video in the project (else the newest saved picture) into a 9:16 vertical reel. When the newest saved video in the project (else the newest saved picture) is a video, analyze that video and cut the video itself to 9:16 (its own frames and sound, at most 30 s, the subject re-framed vertically); no new clip is generated from a frame of it. Only when the newest saved video in the project (else the newest saved picture) is a still picture, animate it by image-to-video generation with a subtle Ken Burns push with drifting motion particles. Keep the output short-form and social-ready.
