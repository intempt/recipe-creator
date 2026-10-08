---
id: mockup
title: Artwork on a mockup
slash_command: /mockup
group: Creative
owner: intempt
curator: aurobind
summary: Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective
  and material.
description: >-
  Apparel, print, packaging: mockup in one click.
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
  vertical:
    - fashion
  complexity: standard
  executionMode: oneshot
  tags:
    - image
    - mockup
inputs:
  - input: Artwork
    what_the_installer_supplies: The artwork file
    if_missing: The step is marked vague and waits until one is attached.
  - input: Mockup scene
    what_the_installer_supplies: A t-shirt, a mug, a billboard or packaging
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The artwork you supply when you run it
    - The mockup scene you supply when you run it
  writes:
    - A new image, from step 1 "Composite the artwork"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Composite the artwork
    summary: >-
      You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting,
      perspective warping and material-appropriate rendering.
    builds: image
    description: |-
      Generate one mockup image.
      Composite the artwork attached to this run onto the mockup scene chosen for this run: a t-shirt, a mug, a billboard or packaging.
      Apply realistic lighting, perspective warping and rendering that suits the material.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Mockup image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Artwork on a mockup

Puts your artwork onto a t-shirt, mug, billboard or package with realistic lighting, perspective and material.

## Steps

1. **Composite the artwork** (builds image)

   You supply the artwork and pick a mockup scene. The artwork is composited on with realistic lighting, perspective warping and material-appropriate rendering.

## What you end up with

- **image** (image): Mockup image.

## What this recipe touches

Reads:

- The artwork you supply when you run it
- The mockup scene you supply when you run it

Writes:

- A new image, from step 1 "Composite the artwork"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Artwork | The artwork file | The step is marked vague and waits until one is attached. |
| Mockup scene | A t-shirt, a mug, a billboard or packaging | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
