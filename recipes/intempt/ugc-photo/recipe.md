---
id: ugc-photo
title: UGC-style product photo
slash_command: /ugc-photo
group: Creative
owner: intempt
summary: Re-shoots a studio packshot as a candid handheld phone photo of a real person holding the product.
description: >-
  Studio packshot to candid handheld.
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
    - ugc
    - candid
steps:
  - id: s1
    title: Reshoot as a candid photo
    summary: >-
      Re-renders the same product as a handheld selfie: a real person holding it at arm's length, a kitchen
      or bathroom counter behind, real skin texture and slightly underexposed. Authentic rather than glamour.
    builds: image
    description: |-
      Re-shoot a product as a candid UGC photo.
      Take the same product and re-render as a candid handheld selfie: real person holding the product at arm's length, kitchen/bathroom counter behind, real skin texture, half-face cropped, slightly underexposed. Authentic, not glamour.
      Pipeline: flux-pro/kontext (style transfer with product identity lock)
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: UGC-style product photo.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# UGC-style product photo

Re-shoots a studio packshot as a candid handheld phone photo of a real person holding the product.

## Steps

1. **Reshoot as a candid photo** (builds image)

   Re-renders the same product as a handheld selfie: a real person holding it at arm's length, a kitchen or bathroom counter behind, real skin texture and slightly underexposed. Authentic rather than glamour.

## What you end up with

- **image** (image): UGC-style product photo.

## Availability

Install now: every step builds something the engine supports today.
