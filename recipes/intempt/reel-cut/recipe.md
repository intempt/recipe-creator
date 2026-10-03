---
id: reel-cut
title: Vertical reel cut
slash_command: /reel-cut
group: Creative
owner: intempt
summary: Re-frames a 16:9 landscape shot as a 9:16 vertical reel, ready to post.
description: >-
  16:9 spot to 9:16 vertical.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: standard
  executionMode: oneshot
  tags:
    - video
    - reel
    - reformat
    - vertical
steps:
  - id: s1
    title: Reframe to 9:16
    summary: >-
      Re-frames the subject for vertical and adds a subtle Ken Burns push with drifting motion particles,
      in a social-ready short format.
    builds: video
    description: |-
      Reformat a landscape still/clip to a 9:16 vertical reel.
      Subject re-framed vertical with subtle Ken Burns push and drifting motion particles. Social-ready short format.
      Pipeline: image to video at 9:16
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Vertical reel cut.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Vertical reel cut

Re-frames a 16:9 landscape shot as a 9:16 vertical reel, ready to post.

## Steps

1. **Reframe to 9:16** (builds video)

   Re-frames the subject for vertical and adds a subtle Ken Burns push with drifting motion particles, in a social-ready short format.

## What you end up with

- **video** (video): Vertical reel cut.

## Availability

Coming soon: waiting on the engine to build video.
