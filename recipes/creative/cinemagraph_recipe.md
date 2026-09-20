---
name: cinemagraph
description: |
  Use when a user mentions "cinemagraph", "living photo", "subtle motion", "one element moves", or asks for a photo where only one element is animated. Still photo, one element moves.
arguments: []
intempt:
  id: cinemagraph
  version: 1.0.0
  slashCommand: /cinemagraph
  group: Creative
  title: 'Cinemagraph loop'
  shortDescription: 'Turns a still photo into a seamless loop where one element moves, such as steam or a pour, and everything else stays frozen.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, cinemagraph, loop]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Animate one element'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Holds the camera fixed and freezes the whole frame except one element, such as gentle steam, a leaf in the breeze or a liquid pour. The result is a subtle seamless loop.'
      prompt: |
        Generate a cinemagraph from a still image.

        Camera stays fixed. Everything stays frozen except one element (gentle steam, single leaf in breeze, liquid pour). Subtle hypnotic seamless loop.

        Pipeline: image to video (camera-fixed, loop)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Cinemagraph loop." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cinemagraph loop

Turns a still photo into a seamless loop where one element moves, such as steam or a pour, and everything else stays frozen.

## What it does

1. **Animate one element** (`generate_video`)

   Holds the camera fixed and freezes the whole frame except one element, such as gentle steam, a leaf in the breeze or a liquid pour. The result is a subtle seamless loop.

## What you end up with

- **video** (video): Cinemagraph loop.
