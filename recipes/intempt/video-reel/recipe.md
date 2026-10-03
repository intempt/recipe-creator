---
id: video-reel
title: Short video reel
slash_command: /video-reel
group: Creative
owner: intempt
summary: Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene
  on its own, with voice and music.
description: >-
  Script + Avatar + product = posted-ready reel.
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
    - reel
    - avatar
    - product
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Generate the reel"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Generate the reel
    summary: >-
      You pick a subject mode and write the script. With an avatar, the identity is locked into the first
      frame with voice and music. With a product, the catalog SKU anchors the first frame. Scene-only
      runs text to video.
    builds: video
    description: |-
      Generate a short video reel.
      Inputs:
      - subjectMode: Avatar | Product | Scene-only
      - modelId (if Avatar): identity-locked Avatar
      - productIds (if Product): catalog SKUs
      - sceneId (optional): background scene
      - script: script or prompt (rich text)
      - duration: 5s or 10s
      Pipeline: kling v2.1 i2v + elevenlabs-tts
      Runner: video-reel (custom)
      In Avatar mode, the Avatar is identity-locked in the first frame with voice + music. In Product mode, the catalog SKU anchors the first frame. Scene-only uses text-to-video.
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Generated reel.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Short video reel

Builds a 5 or 10 second reel from a script, using your avatar, a catalog product, or a scene on its own, with voice and music.

## Steps

1. **Generate the reel** (builds video)

   You pick a subject mode and write the script. With an avatar, the identity is locked into the first frame with voice and music. With a product, the catalog SKU anchors the first frame. Scene-only runs text to video.

## What you end up with

- **video** (video): Generated reel.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Generate the reel"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
