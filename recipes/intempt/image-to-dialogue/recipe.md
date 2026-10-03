---
id: image-to-dialogue
title: Talking portrait
slash_command: /image-to-dialogue
group: Creative
owner: intempt
summary: Makes any portrait speak a script you write, in a voice you pick, with the face lip-synced to
  the audio.
description: >-
  Make any portrait speak your script.
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
    - dialogue
    - avatar
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

Makes any portrait speak a script you write, in a voice you pick, with the face lip-synced to the audio.

## Steps

1. **Make the portrait speak** (builds video)

   You upload a portrait, choose a voice preset and write the script. The face is lip-synced to the generated speech, with its identity and features preserved.

## What you end up with

- **video** (video): Talking-portrait clip.

## Availability

Coming soon: waiting on the engine to build video.
