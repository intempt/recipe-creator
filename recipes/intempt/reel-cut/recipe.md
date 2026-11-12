---
frontmatter_id: reel-cut
slash_command: /reel-cut
description: Generate a new 9:16 vertical clip for a reel. This creates a vertical video rather than reframing an existing landscape clip.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Creates a new 9:16 vertical reel clip from a landscape still or clip, with the subject reframed, a subtle push-in,
    and drifting motion particles.
  parameters:
  - name: aspect_ratio
    type: string
    label: Output aspect ratio
    default: '9:16'
    required: false
  - name: motion_style
    type: string
    label: Motion style
    default: subtle Ken Burns push with drifting motion particles
    required: false
  requirements:
  - slot: source_clip
    kind: knowledge
    meaning: A landscape still image or video clip to reformat into a vertical reel
  steps:
  - id: s1
    builds: video
    uses:
    - source_clip
    - aspect_ratio
    - motion_style
    instruction: Reformat {source_clip} into a {aspect_ratio} vertical reel by image-to-video generation. Re-frame the subject
      vertically, apply a {motion_style}, and keep the output short-form and social-ready.
---

# Vertical reel cut

Slash command: /reel-cut

## Step 1: Reframe to 9:16

Reformat a landscape still/clip to a 9:16 vertical reel.
Subject re-framed vertical with subtle Ken Burns push and drifting motion particles. Social-ready short format.
Pipeline: image to video at 9:16
