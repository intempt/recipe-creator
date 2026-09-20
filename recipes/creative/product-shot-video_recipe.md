---
name: product-shot-video
description: |
  Use when a user mentions "product video", "product clip", "SKU video", "product animation", or asks for a video from a static product image. Every SKU becomes a thumb-stopping clip.
arguments: []
intempt:
  id: product-shot-video
  version: 1.0.0
  slashCommand: /product-shot-video
  group: Creative
  title: 'Product clip from a still'
  shortDescription: 'Turns a static product image into a 5 second clip with a 360 spin, a dolly-in or a floating reveal, plus an optional music bed.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, product, i2v]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Animate the product'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'You pick a catalog product and a motion style: 360 rotation, dolly-in or floating reveal. Returns a 5 second clip, with the music bed on by default.'
      prompt: |
        Generate a product shot video from a static image.

        Inputs:
        - productId: catalog product
        - scene: motion style (360° rotation, dolly-in, floating reveal)
        - script (optional): additional direction
        - music: enable music bed (default: true)

        Pipeline: kling i2v + mmaudio-v2

        Produce a 5-second clip (360° rotation, dolly-in, or floating reveal) with optional music bed.
  outputs:
    - { name: video, type: video, cardinality: single, description: "Product shot video." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product clip from a still

Turns a static product image into a 5 second clip with a 360 spin, a dolly-in or a floating reveal, plus an optional music bed.

## What it does

1. **Animate the product** (`generate_video`)

   You pick a catalog product and a motion style: 360 rotation, dolly-in or floating reveal. Returns a 5 second clip, with the music bed on by default.

## What you end up with

- **video** (video): Product shot video.
