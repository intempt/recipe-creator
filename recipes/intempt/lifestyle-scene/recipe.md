---
id: lifestyle-scene
title: Product in a real setting
slash_command: /lifestyle-scene
group: Creative
owner: intempt
summary: Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with
  natural light and depth of field.
description: >-
  Product in a real-world setting.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - lifestyle
    - product
steps:
  - id: s1
    title: Place the product in a scene
    summary: >-
      Re-renders the product in a real-world environment with natural ambient lighting and realistic depth
      of field. The product itself is unchanged.
    builds: image
    description: |-
      Place a product in a lifestyle scene.
      Take the studio packshot and re-render the product in a real-world environment (kitchen, office, outdoors, etc.). Product identity must remain unchanged. Apply natural ambient lighting and realistic depth of field.
      Pipeline: flux-pro/kontext (scene replacement with product identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Lifestyle scene image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product in a real setting

Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with natural light and depth of field.

## Steps

1. **Place the product in a scene** (builds image)

   Re-renders the product in a real-world environment with natural ambient lighting and realistic depth of field. The product itself is unchanged.

## What you end up with

- **image** (image): Lifestyle scene image.

## Availability

Install now: every step builds something the engine supports today.
