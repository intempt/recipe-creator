---
name: ugc-selfie-video
description: |
  Use when a user mentions "UGC video", "selfie video", "candid video clip", "handheld video", or asks for an authentic selfie-style video. Handheld selfie still to candid clip.
arguments: []
intempt:
  id: ugc-selfie-video
  version: 1.0.0
  slashCommand: /ugc-selfie-video
  group: Creative
  title: 'UGC selfie clip'
  shortDescription: 'Turns a handheld selfie still into a 5 second candid clip with a subtle head turn and a natural smile.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, ugc, selfie, candid]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Animate the selfie'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Uses the selfie still as the seed and produces a 5 second candid handheld clip with a subtle head turn, a natural smile, real kitchen light and slight handheld drift.'
      prompt: |
        Generate a UGC selfie video from a still.

        Seed on the selfie still. 5s candid handheld selfie clip: subtle head turn, natural smile, real kitchen light, slight handheld drift. Authentic, not glamour.

        Pipeline: image to video (candid motion)
  outputs:
    - { name: video, type: video, cardinality: single, description: "UGC selfie video clip." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# UGC selfie clip

Turns a handheld selfie still into a 5 second candid clip with a subtle head turn and a natural smile.

## What it does

1. **Animate the selfie** (`generate_video`)

   Uses the selfie still as the seed and produces a 5 second candid handheld clip with a subtle head turn, a natural smile, real kitchen light and slight handheld drift.

## What you end up with

- **video** (video): UGC selfie video clip.
