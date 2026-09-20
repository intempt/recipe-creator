---
name: reel-cut
description: |
  Use when a user mentions "reel cut", "vertical reformat", "16:9 to 9:16", "landscape to portrait", or asks to reformat a landscape video to vertical. 16:9 spot → 9:16 vertical.
arguments: []
intempt:
  id: reel-cut
  version: 1.0.0
  slashCommand: /reel-cut
  group: Creative
  shortDescription: '16:9 spot to 9:16 vertical.'
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
      title: "Reformat to vertical reel"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Take a 16:9 landscape frame and re-generate as a 9:16 vertical reel with subject re-framing and subtle motion."
      prompt: |
        Reformat a landscape still/clip to a 9:16 vertical reel.

        Subject re-framed vertical with subtle Ken Burns push and drifting motion particles. Social-ready short format.

        Pipeline: image→video at 9:16
  outputs:
    - { name: video, type: video, cardinality: single, description: "Vertical reel cut." }
---

# Reel Cut

## Procedure

1. **Reformat to vertical reel** [`generate_video`] — 16:9 → 9:16 with re-framing. → produces: video

## Notes

- Pipeline: fal.ai image→video at 9:16 aspect.
- Subtle Ken Burns push and motion particles for social-ready output.
