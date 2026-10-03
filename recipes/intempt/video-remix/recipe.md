---
id: video-remix
title: Reference-anchored video remix
slash_command: /video-remix
group: Creative
owner: intempt
summary: Pin up to four video references and get back branded reel variants anchored to them (four by
  default).
description: >-
  Four references in, your branded reel out.
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
    - remix
    - reference
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Pin clips and fan out"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Pin clips and fan out
    summary: >-
      You pin one to four references, which can be a clip, scene, avatar or product. Returns branded reel
      variants anchored to those clips.
    builds: video
    description: |-
      Generate branded video variations from reference pins.
      Inputs:
      - references: 1: 4 video references (clip, scene, avatar, product)
      - fanout: number of variations (default: 4)
      Pipeline: kling v3 i2v multi-ref
      Runner: video-remix (custom)
      Fan out branded reel variants anchored to the reference clips.
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Remixed video variations.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Reference-anchored video remix

Pin up to four video references and get back branded reel variants anchored to them (four by default).

## Steps

1. **Pin clips and fan out** (builds video)

   You pin one to four references, which can be a clip, scene, avatar or product. Returns branded reel variants anchored to those clips.

## What you end up with

- **video** (video): Remixed video variations.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Pin clips and fan out"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
