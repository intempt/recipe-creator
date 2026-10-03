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
inputs:
  - input: Packshot
    what_the_installer_supplies: A studio photo of the product
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The packshot you supply when you run it
  writes:
    - A new image, from step 1 "Reshoot as a candid photo"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Reshoot as a candid photo
    summary: >-
      Re-renders the same product as a handheld selfie: a real person holding it at arm's length, a kitchen
      or bathroom counter behind, real skin texture and slightly underexposed. Authentic rather than glamour.
    builds: image
    description: |-
      Edit the studio packshot attached to this run.
      Re-render it as a candid handheld selfie: a real person holding the same product at arm's length, a kitchen or bathroom counter behind them, real skin texture, the face cropped at half, and slightly underexposed.
      Make it look authentic, not glamorous, and do not change the product.
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

## What this recipe touches

Reads:

- The packshot you supply when you run it

Writes:

- A new image, from step 1 "Reshoot as a candid photo"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Packshot | A studio photo of the product | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
