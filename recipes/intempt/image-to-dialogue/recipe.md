---
id: image-to-dialogue
title: Talking portrait
slash_command: /image-to-dialogue
group: Creative
owner: intempt
curator: aurobind
summary: >-
  Generates spoken audio from your script and animates a portrait with subtle motion to accompany the
  voiceover.
description: >-
  Animate a portrait with subtle motion alongside voiceover generated from your script.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  industry:
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical: []
  complexity: standard
  executionMode: oneshot
  tags:
    - video
    - dialogue
    - avatar
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new video, from step 1 "Make the portrait speak"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Make the portrait speak
    summary: >-
      You upload a portrait, choose a voice preset and write the script. The face is lip-synced to the
      generated speech, with its identity and features preserved.
    builds: video
    description: |-
      Generate a talking-portrait video.
      Inputs:
      - image: portrait photo (file upload)
      - script: dialogue script (rich text)
      - voiceId: voice preset
      Pipeline: kling-clip + elevenlabs-tts
      Lip-sync the portrait (Avatar or any face) to the generated speech. Identity and facial features preserved.
outputs:
  - key: video
    producedByStep: s1
    type: video
    description: Talking-portrait clip.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Talking portrait

Generates spoken audio from your script and animates a portrait with subtle motion to accompany the voiceover.

## Steps

1. **Make the portrait speak** (builds video)

   You upload a portrait, choose a voice preset and write the script. The face is lip-synced to the generated speech, with its identity and features preserved.

## What you end up with

- **video** (video): Talking-portrait clip.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new video, from step 1 "Make the portrait speak"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build video.
