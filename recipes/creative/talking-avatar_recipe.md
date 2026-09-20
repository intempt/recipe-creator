---
name: talking-avatar
description: |
  Use when a user mentions "talking avatar", "spokesperson video", "talking head", "avatar clip", or asks for a portrait that speaks. Portrait still to spokesperson clip.
arguments: []
intempt:
  id: talking-avatar
  version: 1.0.0
  slashCommand: /talking-avatar
  group: Creative
  title: 'Talking head from a portrait'
  shortDescription: 'Turns a portrait still into a 5 second talking-head loop with subtle lip movement and eye contact.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, avatar, talking-head]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Animate the portrait'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Holds the camera fixed and produces a 5 second natural loop with subtle lip movement, gentle eye contact and a single blink. Identity is preserved exactly.'
      prompt: |
        Generate a talking avatar video from a portrait still.

        Camera fixed. 5s natural talking-head loop: subtle lip movement, gentle eye contact, single blink. Identity preserved exactly.

        Pipeline: image to video (camera-fixed, talking-head)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Talking avatar clip." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Talking head from a portrait

Turns a portrait still into a 5 second talking-head loop with subtle lip movement and eye contact.

## What it does

1. **Animate the portrait** (`generate_video`)

   Holds the camera fixed and produces a 5 second natural loop with subtle lip movement, gentle eye contact and a single blink. Identity is preserved exactly.

## What you end up with

- **video** (video): Talking avatar clip.
