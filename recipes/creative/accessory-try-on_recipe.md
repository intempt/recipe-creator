---
name: accessory-try-on
description: |
  Use when a user mentions "accessory try-on", "try on glasses", "try on jewelry", "try on watch", "virtual try-on", or asks to place an accessory on an AI model. Eyewear, jewelry, watches on model.
arguments: []
intempt:
  id: accessory-try-on
  version: 1.0.0
  slashCommand: /accessory-try-on
  group: Creative
  title: 'Accessory on a model'
  shortDescription: 'Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory itself unchanged.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, accessory, try-on]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Put the accessory on a model'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop. The accessory itself is not redrawn.'
      prompt: |
        Place the accessory on an AI model.

        Take the exact same accessory and place it on the face/wrist/body of an AI model, shoulders-up, candid, real skin. Soft window light, neutral backdrop. Accessory identity preserved exactly.

        Pipeline: flux-pro/kontext (accessory placement with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Accessory try-on image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Accessory on a model

Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory itself unchanged.

## What it does

1. **Put the accessory on a model** (`generate_image`)

   Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop. The accessory itself is not redrawn.

## What you end up with

- **image** (image): Accessory try-on image.
