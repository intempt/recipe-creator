---
id: multi-shot-video
title: Multi-shot video from a shot list
slash_command: /multi-shot
group: Creative
owner: intempt
curator: aurobind
summary: >-
  Generates each shot in your shot list as a separate Kling v3 text-to-video clip. Use the merge-video
  workflow node to join clips into one reel.
description: >-
  Create multiple shots as separate Kling v3 text-to-video clips, then join them with the merge-video workflow
  node.
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
    - multi-shot
    - story
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Render and join the shots"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Render and join the shots
    summary: >-
      You write one prompt per shot, pick a shared scene look, and set 3 or 5 seconds per shot. Each shot
      is rendered in the same visual style, then concatenated into one reel.
    builds: video
    description: |-
      Generate a multi-shot video from a shot list.
      Inputs:
      - shotList: one prompt per shot (multi-string)
      - scene: shared scene/look across all shots
      - durationPerShot: 3s or 5s per shot
      Pipeline: kling v2.1 master t2v × N + concat
      Render each shot with consistent visual style, then concatenate into a single reel.
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Multi-shot reel.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Multi-shot video from a shot list

Generates each shot in your shot list as a separate Kling v3 text-to-video clip. Use the merge-video workflow node to join clips into one reel.

## Steps

1. **Render and join the shots** (builds video)

   You write one prompt per shot, pick a shared scene look, and set 3 or 5 seconds per shot. Each shot is rendered in the same visual style, then concatenated into one reel.

## What you end up with

- **video** (video): Multi-shot reel.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Render and join the shots"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
