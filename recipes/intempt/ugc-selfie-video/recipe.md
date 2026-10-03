---
id: ugc-selfie-video
title: UGC selfie clip
slash_command: /ugc-selfie-video
group: Creative
owner: intempt
summary: Turns a handheld selfie still into a 5 second candid clip with a subtle head turn and a natural
  smile.
description: >-
  Handheld selfie still to candid clip.
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
    - ugc
    - selfie
    - candid
steps:
  - id: s1
    title: Animate the selfie
    summary: >-
      Uses the selfie still as the seed and produces a 5 second candid handheld clip with a subtle head
      turn, a natural smile, real kitchen light and slight handheld drift.
    builds: video
    description: |-
      Generate a UGC selfie video from a still.
      Seed on the selfie still. 5s candid handheld selfie clip: subtle head turn, natural smile, real kitchen light, slight handheld drift. Authentic, not glamour.
      Pipeline: image to video (candid motion)
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: UGC selfie video clip.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# UGC selfie clip

Turns a handheld selfie still into a 5 second candid clip with a subtle head turn and a natural smile.

## Steps

1. **Animate the selfie** (builds video)

   Uses the selfie still as the seed and produces a 5 second candid handheld clip with a subtle head turn, a natural smile, real kitchen light and slight handheld drift.

## What you end up with

- **video** (video): UGC selfie video clip.

## Availability

Coming soon: waiting on the engine to build video.
