---
name: image-remix
description: |
  Use when a user mentions "image remix", "remix", "reference-based variations", "pinboard variations", or asks for variations from reference images. Reference-anchored variations from your pinboard.
arguments: []
intempt:
  id: image-remix
  version: 1.0.0
  slashCommand: /image-remix
  group: Creative
  title: 'Reference-anchored remix'
  shortDescription: 'Pin up to four reference images with a weight on each, and get back variations anchored to them (four by default).'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, remix, reference]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Pin references and fan out'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light, Medium or Strong. The weight decides how strongly that reference pulls the output.'
      prompt: |
        Generate image variations from reference pins.

        Inputs:
        - references: 1: 4 reference images (canvas snapshot, scene, avatar, or upload) each with weight (Light/Medium/Strong)
        - fanout: number of variations to generate (default: 4)

        Pipeline: nano-banana-pro with reference_images[] and per-weight prompt directives
        Runner: image-remix (custom)

        Fan out on-brand variations anchored to the reference images. Each reference's weight controls how strongly it influences the output.
  outputs:
    - { name: image, type: image, cardinality: list, description: "Remixed image variations." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Reference-anchored remix

Pin up to four reference images with a weight on each, and get back variations anchored to them (four by default).

## What it does

1. **Pin references and fan out** (`generate_image`)

   You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light, Medium or Strong. The weight decides how strongly that reference pulls the output.

## What you end up with

- **image** (image): Remixed image variations.
