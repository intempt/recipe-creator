---
name: image-to-dialogue
description: |
  Use when a user mentions "talking portrait", "lip sync", "make portrait speak", "dialogue video", or asks to animate a face with a script. Make any portrait speak your script.
arguments: []
intempt:
  id: image-to-dialogue
  version: 1.0.0
  slashCommand: /image-to-dialogue
  group: Creative
  title: 'Talking portrait'
  shortDescription: 'Makes any portrait speak a script you write, in a voice you pick, with the face lip-synced to the audio.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [video, dialogue, avatar]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_video
  procedure:
    - step: 1
      title: 'Make the portrait speak'
      command: generate_video
      produces: video
      bindsAs: video
      description: 'You upload a portrait, choose a voice preset and write the script. The face is lip-synced to the generated speech, with its identity and features preserved.'
      prompt: |
        Generate a talking-portrait video.

        Inputs:
        - image: portrait photo (file upload)
        - script: dialogue script (rich text)
        - voiceId: voice preset

        Pipeline: kling-clip + elevenlabs-tts

        Lip-sync the portrait (Avatar or any face) to the generated speech. Identity and facial features preserved.
  outputs:
    - { name: video, type: video, cardinality: single, description: "Talking-portrait clip." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Talking portrait

Makes any portrait speak a script you write, in a voice you pick, with the face lip-synced to the audio.

## What it does

1. **Make the portrait speak** (`generate_video`)

   You upload a portrait, choose a voice preset and write the script. The face is lip-synced to the generated speech, with its identity and features preserved.

## What you end up with

- **video** (video): Talking-portrait clip.
