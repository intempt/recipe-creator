---
id: cinematic-studio
title: Cinematic look board
slash_command: /cinematic-studio
group: Creative
owner: intempt
summary: Returns a board of nine cinematic looks from one image, so you can pick the grade you want.
description: >-
  Nine cinematic looks from one frame.
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
    - cinematic
inputs:
  - input: Source image
    what_the_installer_supplies: The image to grade
    if_missing: The step is marked vague and waits until one is attached.
does_not_claim:
  - Five of the nine looks are named. The other four are chosen when the step runs.
touches:
  reads:
    - The source image you supply when you run it
  writes:
    - A new image, from step 1 "Render nine cinematic looks"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Render nine cinematic looks
    summary: >-
      Renders nine looks from your image in parallel, each in the style of a different cinematographer.
      You promote the one you want to the canvas.
    builds: image
    description: |-
      Generate nine images from the image attached to this run, laid out as a 3 by 3 board.
      Give each image the look of a different cinematographer: Wes Anderson, Roger Deakins, Emmanuel Lubezki, Christopher Doyle, Bradford Young, and four others, with no cinematographer used twice.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: 9 cinematic looks.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cinematic look board

Returns a board of nine cinematic looks from one image, so you can pick the grade you want.

## Steps

1. **Render nine cinematic looks** (builds image)

   Renders nine looks from your image in parallel, each in the style of a different cinematographer. You promote the one you want to the canvas.

## What you end up with

- **image** (image): 9 cinematic looks.

## What this recipe touches

Reads:

- The source image you supply when you run it

Writes:

- A new image, from step 1 "Render nine cinematic looks"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Source image | The image to grade | The step is marked vague and waits until one is attached. |

## What this recipe does not claim

- Five of the nine looks are named. The other four are chosen when the step runs.

## Availability

Install now: every step builds something the engine supports today.
