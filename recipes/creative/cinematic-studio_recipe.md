---
name: cinematic-studio
description: |
  Use when a user mentions "cinematic", "cinematic looks", "film grade", "color grade", "Wes Anderson look", or asks for cinematic styling of an image. Nine cinematic looks from one frame.
arguments: []
intempt:
  id: cinematic-studio
  version: 1.0.0
  slashCommand: /cinematic-studio
  group: Creative
  title: 'Cinematic look board'
  shortDescription: 'Returns a board of nine cinematic looks from one image, so you can pick the grade you want.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, cinematic]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Render nine cinematic looks'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Renders nine looks from your image in parallel, each in the style of a different cinematographer. You promote the one you want to the canvas.'
      prompt: |
        Generate a 3×3 board of cinematic looks from one input image.

        Inputs:
        - image: source image (file upload)

        Pipeline: restyle × 9 (parallel)

        Produce 9 cinematic looks (Wes Anderson, Roger Deakins, Lubezki, Christopher Doyle, Bradford Young, etc.). The user picks one to promote to the canvas.
  outputs:
    - { name: image, type: image, cardinality: list, description: "9 cinematic looks." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cinematic look board

Returns a board of nine cinematic looks from one image, so you can pick the grade you want.

## What it does

1. **Render nine cinematic looks** (`generate_image`)

   Renders nine looks from your image in parallel, each in the style of a different cinematographer. You promote the one you want to the canvas.

## What you end up with

- **image** (image): 9 cinematic looks.
