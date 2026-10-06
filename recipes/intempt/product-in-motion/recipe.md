---
id: product-in-motion
title: Turntable product spin
slash_command: /product-in-motion
group: Creative
owner: intempt
curator: aurobind
summary: Turns a product packshot into a slow 360 degree turntable spin video on the same backdrop.
description: >-
  Packshot to turntable spin.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  industry:
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical: []
  complexity: standard
  executionMode: oneshot
  tags:
    - video
    - product
    - turntable
    - 360
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Spin the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Spin the product
    summary: >-
      Holds the camera fixed and rotates the product slowly on the same backdrop, in the style of a luxury
      e-commerce 360 spin. No text or logo is added.
    builds: video
    description: |-
      Generate a product turntable spin video.
      Camera fixed. Slow elegant turntable rotation of the product, same backdrop. Luxury e-commerce 360° spin. No text, no logo.
      Pipeline: image to video (camera-fixed, turntable)
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Product turntable video.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Turntable product spin

Turns a product packshot into a slow 360 degree turntable spin video on the same backdrop.

## Steps

1. **Spin the product** (builds video)

   Holds the camera fixed and rotates the product slowly on the same backdrop, in the style of a luxury e-commerce 360 spin. No text or logo is added.

## What you end up with

- **video** (video): Product turntable video.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Spin the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
