---
id: interior-staging
title: Virtual interior staging
slash_command: /interior-staging
group: Creative
owner: intempt
summary: Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as
  they were shot.
description: >-
  Empty room, finished room.
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
    - interior
    - staging
inputs:
  - input: Room photo
    what_the_installer_supplies: A photo of the empty room
    if_missing: The step is marked vague and waits until one is attached.
does_not_claim:
  - Which furniture and decor beyond the coffee table, vase and floor lamp is added is decided when the
    step runs.
touches:
  reads:
    - The room photo you supply when you run it
  writes:
    - A new image, from step 1 "Furnish the empty room"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Furnish the empty room
    summary: >-
      Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room
      geometry, walls, flooring, windows and daylight stay unchanged.
    builds: image
    description: |-
      Edit the photo of an empty room attached to this run.
      Furnish it with furniture, a coffee table, a vase, a floor lamp and other staging that suits the room.
      Keep the room geometry, walls, flooring, windows and daylight unchanged.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Staged interior image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Virtual interior staging

Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as they were shot.

## Steps

1. **Furnish the empty room** (builds image)

   Adds furniture, a coffee table, a vase, a floor lamp and other staging suited to the space. Room geometry, walls, flooring, windows and daylight stay unchanged.

## What you end up with

- **image** (image): Staged interior image.

## What this recipe touches

Reads:

- The room photo you supply when you run it

Writes:

- A new image, from step 1 "Furnish the empty room"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Room photo | A photo of the empty room | The step is marked vague and waits until one is attached. |

## What this recipe does not claim

- Which furniture and decor beyond the coffee table, vase and floor lamp is added is decided when the step runs.

## Availability

Install now: every step builds something the engine supports today.
