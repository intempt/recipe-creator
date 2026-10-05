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
  shortDescription: "Animate a portrait image into a lip-synced talking video speaking your script using text-to-speech."
  availability: available
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
      title: "Animate portrait with dialogue"
      command: generate_video
      produces: video
      bindsAs: video
      description: "Upload a portrait, pick a voice, write the script. The model lip-syncs the face to the generated speech."
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

# Image to Dialogue

## Procedure

1. **Animate portrait with dialogue** [`generate_video`] — Upload portrait, pick voice, write script. → produces: video

   ```text
   Inputs: portrait image, script, voiceId
   Pipeline: kling-clip + elevenlabs-tts
   ```

## Notes

- fal.ai pipeline: kling-clip for lip-sync + elevenlabs-tts for voice.
- Portrait identity preserved during animation.
