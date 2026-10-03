---
id: lifestyle-scene
title: Product in a real setting
slash_command: /lifestyle-scene
group: Creative
owner: intempt
curator: aurobind
summary: Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with
  natural light and depth of field.
description: >-
  Product in a real-world setting.
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
    - lifestyle
    - product
inputs:
  - input: Packshot
    what_the_installer_supplies: A studio photo of the product
    if_missing: The step is marked vague and waits until one is attached.
  - input: Setting
    what_the_installer_supplies: The real-world setting, for example a kitchen, an office or outdoors
    if_missing: A kitchen is used.
touches:
  reads:
    - The packshot you supply when you run it
    - The setting you supply when you run it
  writes:
    - A new image, from step 1 "Place the product in a scene"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Place the product in a scene
    summary: >-
      Re-renders the product in a real-world environment with natural ambient lighting and realistic depth
      of field. The product itself is unchanged.
    builds: image
    description: |-
      Edit the studio packshot attached to this run.
      Re-render the product in a real-world kitchen, with natural ambient light and realistic depth of field.
      Do not change the product itself.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Lifestyle scene image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product in a real setting

Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with natural light and depth of field.

## Steps

1. **Place the product in a scene** (builds image)

   Re-renders the product in a real-world environment with natural ambient lighting and realistic depth of field. The product itself is unchanged.

## What you end up with

- **image** (image): Lifestyle scene image.

## What this recipe touches

Reads:

- The packshot you supply when you run it
- The setting you supply when you run it

Writes:

- A new image, from step 1 "Place the product in a scene"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Packshot | A studio photo of the product | The step is marked vague and waits until one is attached. |
| Setting | The real-world setting, for example a kitchen, an office or outdoors | A kitchen is used. |

## Availability

Install now: every step builds something the engine supports today.
