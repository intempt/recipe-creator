---
id: editorial-model
title: Editorial lookbook shot
slash_command: /editorial-model
group: Creative
owner: intempt
curator: aurobind
summary: Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting
  while holding pose and framing.
description: >-
  Full-body model, on location.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical:
    - fashion
    - publishing
  complexity: quick
  executionMode: oneshot
  tags:
    - image
    - editorial
    - fashion
    - model
inputs:
  - input: Lookbook image
    what_the_installer_supplies: A full-body shot of a model in the outfit
    if_missing: The step is marked vague and waits until one is attached.
  - input: Lighting
    what_the_installer_supplies: The lighting to change to
    if_missing: Golden hour with long raking shadows is used.
touches:
  reads:
    - The lookbook image you supply when you run it
    - The lighting you supply when you run it
  writes:
    - A new image, from step 1 "Relight the lookbook shot"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Relight the lookbook shot
    summary: >-
      Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example
      golden hour with long raking shadows.
    builds: image
    description: |-
      Edit the editorial lookbook image attached to this run: a full-body AI model wearing the outfit on location.
      Change only the lighting, to golden hour with long raking shadows.
      Keep the model's identity, the outfit, the pose, the street and the framing identical.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Editorial lookbook image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Editorial lookbook shot

Produces a full-body editorial fashion photo of an AI model on location, then varies the lighting while holding pose and framing.

## Steps

1. **Relight the lookbook shot** (builds image)

   Keeps the same model, outfit, pose, street and framing, and changes only the lighting, for example golden hour with long raking shadows.

## What you end up with

- **image** (image): Editorial lookbook image.

## What this recipe touches

Reads:

- The lookbook image you supply when you run it
- The lighting you supply when you run it

Writes:

- A new image, from step 1 "Relight the lookbook shot"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Lookbook image | A full-body shot of a model in the outfit | The step is marked vague and waits until one is attached. |
| Lighting | The lighting to change to | Golden hour with long raking shadows is used. |

## Availability

Install now: every step builds something the engine supports today.
