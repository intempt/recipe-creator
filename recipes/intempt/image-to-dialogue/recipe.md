---
frontmatter_id: image-to-dialogue
slash_command: /image-to-dialogue
description: Generates spoken audio from your script and animates a portrait with subtle motion to accompany the voiceover.
author:
  name: Aurobind Venu
  first_name: Aurobind
  last_name: Venu
  company: Intempt
  job_title: Creative Director
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
