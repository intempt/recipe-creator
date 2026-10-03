---
id: on-model-shoot
title: On-model product shot
slash_command: /on-model
group: Creative
owner: intempt
summary: Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle
  product photography.
description: >-
  Avatar wearing or holding your product in a scene.
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
    - avatar
    - on-model
inputs:
  - input: Product
    what_the_installer_supplies: One product from your catalog
    if_missing: The step is marked vague and waits until one is chosen.
  - input: Avatar
    what_the_installer_supplies: An identity-locked avatar from your Brand Kit
    if_missing: The step is marked vague and waits until one is chosen.
  - input: Scene
    what_the_installer_supplies: A scene that sets background and lighting
    if_missing: The step is marked vague and waits until one is chosen.
  - input: Pose references
    what_the_installer_supplies: Optional poses for the avatar
    if_missing: The pose is decided when the step runs.
touches:
  reads:
    - The product you supply when you run it
    - The avatar you supply when you run it
    - The scene you supply when you run it
    - The pose references you supply when you run it
  writes:
    - A new image, from step 1 "Compose the on-model shot"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Compose the on-model shot
    summary: >-
      Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the
      same identity across every generation.
    builds: image
    description: |-
      Generate one lifestyle product photo.
      Show the identity-locked avatar chosen for this run wearing or holding the catalog product chosen for this run, in the scene chosen for this run.
      If pose references are chosen for this run, match the avatar's pose to them.
      Keep the avatar's identity the same as in its earlier images.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: On-model lifestyle shot.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# On-model product shot

Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle product photography.

## Steps

1. **Compose the on-model shot** (builds image)

   Combines a catalog product, an avatar, a scene and optional pose references. The avatar keeps the same identity across every generation.

## What you end up with

- **image** (image): On-model lifestyle shot.

## What this recipe touches

Reads:

- The product you supply when you run it
- The avatar you supply when you run it
- The scene you supply when you run it
- The pose references you supply when you run it

Writes:

- A new image, from step 1 "Compose the on-model shot"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product | One product from your catalog | The step is marked vague and waits until one is chosen. |
| Avatar | An identity-locked avatar from your Brand Kit | The step is marked vague and waits until one is chosen. |
| Scene | A scene that sets background and lighting | The step is marked vague and waits until one is chosen. |
| Pose references | Optional poses for the avatar | The pose is decided when the step runs. |

## Availability

Install now: every step builds something the engine supports today.
