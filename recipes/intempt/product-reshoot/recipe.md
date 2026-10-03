---
id: product-reshoot
title: Product relight
slash_command: /product-reshoot
group: Creative
owner: intempt
summary: Re-lights a product photo you already have, using a setting, lighting direction and camera angle
  that you choose.
description: >-
  Re-light any product without booking a studio.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: standard
  executionMode: oneshot
  tags:
    - image
    - product
    - lighting
steps:
  - id: s1
    title: Relight the product
    summary: >-
      You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically
      accurate light falloff and the product itself is unchanged.
    builds: image
    description: |-
      Re-shoot a product image with new lighting.
      Inputs:
      - productImage: uploaded product photo
      - setting: environment preset
      - lighting: lighting direction/style
      - angle: camera angle
      Pipeline: iclight-v2 relight to optional nano-banana-pro/edit
      Re-light the product with physically-accurate light falloff. The product identity must remain unchanged.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Re-lit product image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product relight

Re-lights a product photo you already have, using a setting, lighting direction and camera angle that you choose.

## Steps

1. **Relight the product** (builds image)

   You upload a product photo and pick the setting, lighting and angle. The shot is relit with physically accurate light falloff and the product itself is unchanged.

## What you end up with

- **image** (image): Re-lit product image.

## Availability

Install now: every step builds something the engine supports today.
