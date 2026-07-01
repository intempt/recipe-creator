---
name: video-remix
description: |
  Use when a user mentions "video remix", "remix video", "video variations", "video references", or asks for branded video variants from reference clips. Four references in, your branded reel out.
arguments: []
intempt:
  id: video-remix
  version: 1.0.0
  slashCommand: /video-remix
  group: Creative
  shortDescription: "Four references in, your branded reel out."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, remix, reference]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Remix video from references"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Pin 1–4 video references (clip, scene, avatar, product) and fan out branded variants."
      prompt: |
        Generate branded video variations from reference pins.

        Inputs:
        - references: 1–4 video references (clip, scene, avatar, product)
        - fanout: number of variations (default: 4)

        Pipeline: kling v3 i2v multi-ref
        Runner: video-remix (custom)

        Fan out branded reel variants anchored to the reference clips.
  outputs:
    - { name: video, type: video, cardinality: list, description: "Remixed video variations." }
---

# Video Remix

## Procedure

1. **Remix video from references** [`generate_video`] — Pin 1–4 video references and fan out branded variants. → produces: video

   ```text
   Inputs: 1–4 references, fanout count
   Pipeline: kling v3 i2v multi-ref
   ```

## Notes

- Uses the `video-remix` custom runner.
- fal.ai pipeline: kling v3 i2v multi-ref for multi-reference generation.
