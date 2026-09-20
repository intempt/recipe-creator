---
name: mockup
description: |
  Use when a user mentions "mockup", "product mockup", "t-shirt mockup", "mug mockup", "billboard mockup", or asks to composite artwork onto a physical object. Apparel, print, packaging: mockup in one click.
arguments: []
intempt:
  id: mockup
  version: 1.0.0
  slashCommand: /mockup
  group: Creative
  title: 'Artwork on a mockup'
  shortDescription: 'Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective and material.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, mockup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Composite the artwork'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting, perspective warping and material-appropriate rendering.'
      prompt: |
        Generate a product mockup.

        Inputs:
        - artwork: artwork file (upload)
        - mockupScene: mockup scene preset (t-shirt, mug, billboard, packaging, etc.)

        Pipeline: restyle to nano-banana-pro/edit

        Composite the artwork onto the mockup scene with realistic lighting, perspective warping, and material-appropriate rendering.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Mockup image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Artwork on a mockup

Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective and material.

## What it does

1. **Composite the artwork** (`generate_image`)

   You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting, perspective warping and material-appropriate rendering.

## What you end up with

- **image** (image): Mockup image.
