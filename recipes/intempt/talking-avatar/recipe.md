---
id: talking-avatar
title: Talking head from a portrait
slash_command: /talking-avatar
group: Creative
owner: intempt
summary: Turns a portrait still into a 5 second talking-head loop with subtle lip movement and eye contact.
description: >-
  Portrait still to spokesperson clip.
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
    - avatar
    - talking-head
steps:
  - id: s1
    title: Animate the portrait
    summary: >-
      Holds the camera fixed and produces a 5 second natural loop with subtle lip movement, gentle eye
      contact and a single blink. Identity is preserved exactly.
    builds: video
    description: |-
      Generate a talking avatar video from a portrait still.
      Camera fixed. 5s natural talking-head loop: subtle lip movement, gentle eye contact, single blink. Identity preserved exactly.
      Pipeline: image to video (camera-fixed, talking-head)
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Talking avatar clip.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Talking head from a portrait

Turns a portrait still into a 5 second talking-head loop with subtle lip movement and eye contact.

## Steps

1. **Animate the portrait** (builds video)

   Holds the camera fixed and produces a 5 second natural loop with subtle lip movement, gentle eye contact and a single blink. Identity is preserved exactly.

## What you end up with

- **video** (video): Talking avatar clip.

## Availability

Coming soon: waiting on the engine to build video.
