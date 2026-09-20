---
name: packaging-mockup
description: |
  Use when a user mentions "packaging mockup", "label mockup", "wrap label", "packaging design", or asks to wrap flat label artwork onto a 3D package. Flat label to wrapped on 3D pack.
arguments: []
intempt:
  id: packaging-mockup
  version: 1.0.0
  slashCommand: /packaging-mockup
  group: Creative
  title: 'Label wrapped on a package'
  shortDescription: 'Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label content unchanged.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, packaging, mockup, label]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Wrap the label'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop. Nothing on the label is redrawn.'
      prompt: |
        Wrap flat label artwork onto a 3D package.

        Take the SAME label artwork (identical wordmark, identical layout) and wrap it photorealistically around a 3D package on the same backdrop. Label content preserved exactly.

        Pipeline: flux-pro/kontext (label wrapping with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Packaging mockup image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Label wrapped on a package

Wraps your flat label artwork photorealistically around a 3D can, bottle or box, with the label content unchanged.

## What it does

1. **Wrap the label** (`generate_image`)

   Takes the same label artwork, wordmark and layout and wraps it around a 3D package on the same backdrop. Nothing on the label is redrawn.

## What you end up with

- **image** (image): Packaging mockup image.
