---
name: product-in-motion
description: |
  Use when a user mentions "product in motion", "turntable", "360 spin", "product rotation", or asks for a product spinning/rotating video. Packshot to turntable spin.
arguments: []
intempt:
  id: product-in-motion
  version: 1.0.0
  slashCommand: /product-in-motion
  group: Creative
  title: 'Turntable product spin'
  shortDescription: 'Turns a product packshot into a slow 360 degree turntable spin video on the same backdrop.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, product, turntable, 360]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Spin the product'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'Holds the camera fixed and rotates the product slowly on the same backdrop, in the style of a luxury e-commerce 360 spin. No text or logo is added.'
      prompt: |
        Generate a product turntable spin video.

        Camera fixed. Slow elegant turntable rotation of the product, same backdrop. Luxury e-commerce 360° spin. No text, no logo.

        Pipeline: image to video (camera-fixed, turntable)
  outputs:
    - { name: video, type: video, cardinality: single, description: "Product turntable video." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Turntable product spin

Turns a product packshot into a slow 360 degree turntable spin video on the same backdrop.

## What it does

1. **Spin the product** (`generate_video`)

   Holds the camera fixed and rotates the product slowly on the same backdrop, in the style of a luxury e-commerce 360 spin. No text or logo is added.

## What you end up with

- **video** (video): Product turntable video.
