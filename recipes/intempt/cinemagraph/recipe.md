---
id: cinemagraph
title: Cinemagraph loop
slash_command: /cinemagraph
group: Creative
owner: intempt
curator: aurobind
summary: Turns a still photo into a looping clip where one element moves, such as steam or a pour, and
  everything else stays frozen.
description: >-
  Still photo, one element moves.
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
    - video
    - cinemagraph
    - loop
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Animate one element"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Animate one element
    summary: >-
      Holds the camera fixed and freezes the whole frame except one element, such as gentle steam, a leaf
      in the breeze or a liquid pour. The result is a subtle loop that repeats without a visible cut.
    builds: video
    description: |-
      Generate a cinemagraph from a still image.
      Camera stays fixed. Everything stays frozen except one element (gentle steam, single leaf in breeze, liquid pour). Subtle hypnotic loop with no visible cut.
      Pipeline: image to video (camera-fixed, loop)
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Cinemagraph loop.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Cinemagraph loop

Turns a still photo into a looping clip where one element moves, such as steam or a pour, and everything else stays frozen.

## Steps

1. **Animate one element** (builds video)

   Holds the camera fixed and freezes the whole frame except one element, such as gentle steam, a leaf in the breeze or a liquid pour. The result is a subtle loop that repeats without a visible cut.

## What you end up with

- **video** (video): Cinemagraph loop.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Animate one element"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
