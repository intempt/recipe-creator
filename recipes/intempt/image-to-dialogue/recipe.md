---
frontmatter_id: image-to-dialogue
slash_command: /image-to-dialogue
description: Generates spoken audio from your script and animates a portrait with subtle motion to accompany the voiceover.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns a script and a portrait photo into a talking-portrait video, with spoken audio generated from the script
    and subtle motion that keeps the face recognisable.
  parameters:
  - name: voice_id
    type: string
    label: Voice preset
    required: true
  - name: portrait_image
    type: attachment
    label: Portrait photo
    required: true
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - portrait_image
    - voice_id
    instruction: Generate a talking-portrait video from the uploaded portrait photo and the dialogue script. Generate spoken
      audio from the script using the voice preset {voice_id}, then lip-sync the portrait to that speech and add subtle motion.
      Preserve the subject's identity and facial features.
---

# Talking portrait

Slash command: /image-to-dialogue

## Step 1: Make the portrait speak

Generate a talking-portrait video.
Inputs:
- image: portrait photo (file upload)
- script: dialogue script (rich text)
- voiceId: voice preset
Pipeline: kling-clip + elevenlabs-tts
Lip-sync the portrait (Avatar or any face) to the generated speech. Identity and facial features preserved.
