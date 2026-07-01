---
name: multi-shot-video
description: |
  Use when a user mentions "multi-shot", "shot list", "story video", "multi-clip", or asks to create a video from multiple shots. Tell a story in six shots without an editor.
arguments: []
intempt:
  id: multi-shot-video
  version: 1.0.0
  slashCommand: /multi-shot
  group: Creative
  shortDescription: "Tell a story in six shots without an editor."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, multi-shot, story]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Render multi-shot video"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Write a shot list (one prompt per shot). Each shot is rendered with a consistent look and concatenated into one reel."
      prompt: |
        Generate a multi-shot video from a shot list.

        Inputs:
        - shotList: one prompt per shot (multi-string)
        - scene: shared scene/look across all shots
        - durationPerShot: 3s or 5s per shot

        Pipeline: kling v2.1 master t2v × N + concat

        Render each shot with consistent visual style, then concatenate into a single reel.
  outputs:
    - { name: video, type: video, cardinality: single, description: "Multi-shot reel." }
---

# Multi-Shot Video

## Procedure

1. **Render multi-shot video** [`generate_video`] — Write a shot list, each shot rendered consistently and concatenated. → produces: video

   ```text
   Inputs: shotList (prompts), scene, durationPerShot (3s/5s)
   Pipeline: kling v2.1 master t2v × N + concat
   ```

## Notes

- fal.ai pipeline: kling v2.1 master t2v × N shots + concat.
- Consistent visual style maintained across all shots.
