---
name: reel-cut
description: |
  Use when a user mentions "reel cut", "vertical reformat", "16:9 to 9:16", "landscape to portrait", or asks to reformat a landscape video to vertical. 16:9 spot to 9:16 vertical.
arguments: []
intempt:
  id: reel-cut
  version: 1.0.0
  slashCommand: /reel-cut
  group: Creative
  title: 'Vertical reel cut'
  shortDescription: 'Re-frames a 16:9 landscape shot as a 9:16 vertical reel, ready to post.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, reel, reformat, vertical]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Reframe to 9:16'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Re-frames the subject for vertical and adds a subtle Ken Burns push with drifting motion particles, in a social-ready short format.'
      prompt: |
        Reformat a landscape still/clip to a 9:16 vertical reel.

        Subject re-framed vertical with subtle Ken Burns push and drifting motion particles. Social-ready short format.

        Pipeline: image to video at 9:16
  outputs:
    - { name: video, type: video, cardinality: single, description: "Vertical reel cut." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Vertical reel cut

Re-frames a 16:9 landscape shot as a 9:16 vertical reel, ready to post.

## What it does

1. **Reframe to 9:16** (`generate_video`)

   Re-frames the subject for vertical and adds a subtle Ken Burns push with drifting motion particles, in a social-ready short format.

## What you end up with

- **video** (video): Vertical reel cut.
