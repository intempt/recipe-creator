---
name: pack-shot
description: |
  Use when a user mentions "pack shot", "product shot", "studio shot", "catalog photo", or asks for clean product photography. Studio-clean product stills from one SKU.
arguments: []
intempt:
  id: pack-shot
  version: 1.0.0
  slashCommand: /pack-shot
  group: Creative
  title: 'Studio product shots'
  shortDescription: 'Generates clean studio stills of one catalog product, in a background and lighting you pick.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, product, pack-shot]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Render the product'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean studio shots: front, three-quarter, detail and lifestyle inserts.'
      prompt: |
        Generate studio pack-shot images for the selected product.

        Inputs:
        - productId: catalog SKU to photograph
        - sceneId: background + lighting preset

        Pipeline: nano-banana-pro/edit
        Runner: pack-shot (custom)

        Produce a kit of clean studio shots (front, three-quarter, detail, lifestyle inserts) from the single catalog product using the chosen scene for background and lighting.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Generated pack-shot image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Studio product shots

Generates clean studio stills of one catalog product, in a background and lighting you pick.

## What it does

1. **Render the product** (`generate_image`)

   You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean studio shots: front, three-quarter, detail and lifestyle inserts.

## What you end up with

- **image** (image): Generated pack-shot image.
