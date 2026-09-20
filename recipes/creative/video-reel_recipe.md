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
  title: 'Short video reel'
  shortDescription: 'Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene on its own, with voice and music.'
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
      title: 'Generate the reel'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'You pick a subject mode and write the script. With an avatar, the identity is locked into the first frame with voice and music. With a product, the catalog SKU anchors the first frame. Scene-only runs text to video.'
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
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Short video reel

Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene on its own, with voice and music.

## What it does

1. **Generate the reel** (`generate_video`)

   You pick a subject mode and write the script. With an avatar, the identity is locked into the first frame with voice and music. With a product, the catalog SKU anchors the first frame. Scene-only runs text to video.

## What you end up with

- **video** (video): Generated reel.
