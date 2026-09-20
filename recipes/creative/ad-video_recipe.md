---
name: ad-video
description: |
  Use when a user mentions "ad video", "video ad", "product spot", "cinematic ad", or asks for a video ad from a product still. Product still to cinematic spot.
arguments: []
intempt:
  id: ad-video
  version: 1.0.0
  slashCommand: /ad-video
  group: Creative
  title: 'Cinematic ad spot'
  shortDescription: 'Turns one product still into a 5 second cinematic spot with slow camera drift and soft particles, no text or logo.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, ad, cinematic]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Animate the product still'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Uses the product still as the seed and produces a 5 second spot with smooth camera drift, soft dust particles and the same backdrop. No text or logo overlay is added.'
      prompt: |
        Generate a cinematic ad video from a product still.

        Seed on the product still. Produce a cinematic 5s product spot with smooth subtle camera drift, soft dust particles, same backdrop. No text, no logo overlay.

        Pipeline: image to video (kling/seedance)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Cinematic ad video." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cinematic ad spot

Turns one product still into a 5 second cinematic spot with slow camera drift and soft particles, no text or logo.

## What it does

1. **Animate the product still** (`generate_video`)

   Uses the product still as the seed and produces a 5 second spot with smooth camera drift, soft dust particles and the same backdrop. No text or logo overlay is added.

## What you end up with

- **video** (video): Cinematic ad video.
