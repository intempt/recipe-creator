---
name: video-reel
description: |
  Use when a user mentions "video reel", "reel", "short video", "social reel", "avatar video", or asks for a short-form video combining avatar, product, and script. Script + Avatar + product = posted-ready reel.
arguments: []
intempt:
  id: video-reel
  version: 1.0.0
  slashCommand: /video-reel
  group: Creative
  shortDescription: "Script + Avatar + product = posted-ready reel."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, reel, avatar, product]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: "Generate video reel"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Choose a subject mode (Avatar, Product, or Scene-only), write a script, and generate a short reel."
      prompt: |
        Generate a short video reel.

        Inputs:
        - subjectMode: Avatar | Product | Scene-only
        - modelId (if Avatar): identity-locked Avatar
        - productIds (if Product): catalog SKUs
        - sceneId (optional): background scene
        - script: script or prompt (rich text)
        - duration: 5s or 10s

        Pipeline: kling v2.1 i2v + elevenlabs-tts
        Runner: video-reel (custom)

        In Avatar mode, the Avatar is identity-locked in the first frame with voice + music. In Product mode, the catalog SKU anchors the first frame. Scene-only uses text-to-video.
  outputs:
    - { name: video, type: video, cardinality: single, description: "Generated reel." }
---

# Video Reel

## Procedure

1. **Generate video reel** [`generate_video`] — Choose subject mode, write script, generate reel. → produces: video

   ```text
   Subject modes: Avatar (identity-locked), Product (SKU-anchored), Scene-only (t2v)
   Pipeline: kling v2.1 i2v + elevenlabs-tts
   ```

## Notes

- Uses the `video-reel` custom runner.
- fal.ai pipeline: kling v2.1 i2v + elevenlabs-tts for voiceover.
- Supports 5s and 10s durations.
