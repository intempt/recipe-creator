---
description: Generates spoken audio from your script and animates a portrait with subtle motion to accompany the voiceover.
author:
  first_name: Aurobind
  last_name: Venu
  job_title: Creative Director
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
  - ecommerce
  - media
  - social
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
