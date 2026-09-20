---
name: lifestyle-scene
description: |
  Use when a user mentions "lifestyle scene", "product in context", "real-world setting", "environmental shot", or asks to place a product in a real-world scene. Product in a real-world setting.
arguments: []
intempt:
  id: lifestyle-scene
  version: 1.0.0
  slashCommand: /lifestyle-scene
  group: Creative
  title: 'Product in a real setting'
  shortDescription: 'Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with natural light and depth of field.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, lifestyle, product]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: 'Place the product in a scene'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Re-renders the product in a real-world environment with natural ambient lighting and realistic depth of field. The product itself is unchanged.'
      prompt: |
        Place a product in a lifestyle scene.

        Take the studio packshot and re-render the product in a real-world environment (kitchen, office, outdoors, etc.). Product identity must remain unchanged. Apply natural ambient lighting and realistic depth of field.

        Pipeline: flux-pro/kontext (scene replacement with product identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Lifestyle scene image." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product in a real setting

Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with natural light and depth of field.

## What it does

1. **Place the product in a scene** (`generate_image`)

   Re-renders the product in a real-world environment with natural ambient lighting and realistic depth of field. The product itself is unchanged.

## What you end up with

- **image** (image): Lifestyle scene image.
