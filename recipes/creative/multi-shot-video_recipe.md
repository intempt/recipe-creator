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
  title: 'Multi-shot video from a shot list'
  shortDescription: 'Renders every shot in your shot list with one consistent look and joins them into a single reel, with no editor involved.'
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
      title: 'Render and join the shots'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'You write one prompt per shot, pick a shared scene look, and set 3 or 5 seconds per shot. Each shot is rendered in the same visual style, then concatenated into one reel.'
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
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Multi-shot video from a shot list

Renders every shot in your shot list with one consistent look and joins them into a single reel, with no editor involved.

## What it does

1. **Render and join the shots** (`generate_video`)

   You write one prompt per shot, pick a shared scene look, and set 3 or 5 seconds per shot. Each shot is rendered in the same visual style, then concatenated into one reel.

## What you end up with

- **video** (video): Multi-shot reel.
