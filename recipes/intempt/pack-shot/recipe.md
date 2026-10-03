---
id: pack-shot
title: Studio product shots
slash_command: /pack-shot
group: Creative
owner: intempt
summary: Generates clean studio stills of one catalog product, in a background and lighting you pick.
description: >-
  Studio-clean product stills from one SKU.
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
    - pack-shot
inputs:
  - input: Product
    what_the_installer_supplies: One product from your catalog
    if_missing: The step is marked vague and waits until one is chosen.
  - input: Scene
    what_the_installer_supplies: A scene that sets background and lighting
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The product you supply when you run it
    - The scene you supply when you run it
  writes:
    - A new image, from step 1 "Render the product"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Render the product
    summary: >-
      You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean
      studio shots: front, three-quarter, detail and lifestyle inserts.
    builds: image
    description: |-
      Generate four studio images of the catalog product chosen for this run: front, three-quarter, a detail close-up, and a lifestyle insert.
      Use the background and lighting of the scene chosen for this run.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Generated pack-shot image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Studio product shots

Generates clean studio stills of one catalog product, in a background and lighting you pick.

## Steps

1. **Render the product** (builds image)

   You pick a catalog product and a scene that sets background and lighting. Returns a kit of clean studio shots: front, three-quarter, detail and lifestyle inserts.

## What you end up with

- **image** (image): Generated pack-shot image.

## What this recipe touches

Reads:

- The product you supply when you run it
- The scene you supply when you run it

Writes:

- A new image, from step 1 "Render the product"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product | One product from your catalog | The step is marked vague and waits until one is chosen. |
| Scene | A scene that sets background and lighting | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
