---
id: accessory-try-on
title: Accessory on a model
slash_command: /accessory-try-on
group: Creative
owner: intempt
summary: Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory
  itself unchanged.
description: >-
  Eyewear, jewelry, watches on model.
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
    - accessory
    - try-on
inputs:
  - input: Accessory photo
    what_the_installer_supplies: A packshot of the eyewear, jewelry or watch
    if_missing: The step is marked vague and waits until one is attached.
touches:
  reads:
    - The accessory photo you supply when you run it
  writes:
    - A new image, from step 1 "Put the accessory on a model"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Put the accessory on a model
    summary: >-
      Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop.
      The accessory itself is not redrawn.
    builds: image
    description: |-
      Generate one image from the accessory photo attached to this run.
      Show that exact accessory worn by an AI model, on the face, wrist or body, wherever that accessory is worn.
      Frame the model from the shoulders up, in a candid pose, with real skin texture.
      Use soft window light and a plain neutral backdrop.
      Do not change the accessory's shape, colour, material, markings or proportions.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Accessory try-on image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Accessory on a model

Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory itself unchanged.

## Steps

1. **Put the accessory on a model** (builds image)

   Places the same accessory on an AI model, shoulders up, in soft window light against a neutral backdrop. The accessory itself is not redrawn.

## What you end up with

- **image** (image): Accessory try-on image.

## What this recipe touches

Reads:

- The accessory photo you supply when you run it

Writes:

- A new image, from step 1 "Put the accessory on a model"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Accessory photo | A packshot of the eyewear, jewelry or watch | The step is marked vague and waits until one is attached. |

## Availability

Install now: every step builds something the engine supports today.
