---
id: ad-builder
title: Branded ad from a product
slash_command: /ad-builder
group: Creative
owner: intempt
curator: aurobind
summary: Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours,
  fonts and layout.
description: >-
  One-click on-brand ad from product + concept.
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
    - ad
    - brand
inputs:
  - input: Product
    what_the_installer_supplies: One product from your catalog
    if_missing: The step is marked vague and waits until one is chosen.
  - input: Headline
    what_the_installer_supplies: The headline or creative concept for the ad
    if_missing: The step is marked vague and waits until one is written.
  - input: Brand Kit ad recipe
    what_the_installer_supplies: The ad recipe in your Brand Kit that sets colours, fonts and layout
    if_missing: The step is marked vague and waits until one is chosen.
touches:
  reads:
    - The product you supply when you run it
    - The headline you supply when you run it
    - The brand Kit ad recipe you supply when you run it
  writes:
    - A new image, from step 1 "Build the ad"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the ad
    summary: >-
      Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout
      come from your design system. The output is a finished ad ready to run.
    builds: image
    description: |-
      Generate one finished ad image.
      Show the catalog product chosen for this run.
      Use the headline written for this run as the ad's headline text.
      Take the colours, fonts and layout from the Brand Kit ad recipe chosen for this run.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Finished ad image.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Branded ad from a product

Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours, fonts and layout.

## Steps

1. **Build the ad** (builds image)

   Combines the product, your headline concept and a Brand Kit ad recipe, so colours, fonts and layout come from your design system. The output is a finished ad ready to run.

## What you end up with

- **image** (image): Finished ad image.

## What this recipe touches

Reads:

- The product you supply when you run it
- The headline you supply when you run it
- The brand Kit ad recipe you supply when you run it

Writes:

- A new image, from step 1 "Build the ad"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| Product | One product from your catalog | The step is marked vague and waits until one is chosen. |
| Headline | The headline or creative concept for the ad | The step is marked vague and waits until one is written. |
| Brand Kit ad recipe | The ad recipe in your Brand Kit that sets colours, fonts and layout | The step is marked vague and waits until one is chosen. |

## Availability

Install now: every step builds something the engine supports today.
