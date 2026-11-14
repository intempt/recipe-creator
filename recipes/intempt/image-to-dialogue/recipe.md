---
frontmatter_id: image-to-dialogue
slash_command: /image-to-dialogue
description: Turns a script into a talking-portrait video of your brand character.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns a script into a talking-portrait video of your brand character, with spoken audio generated from the
    script and subtle motion that keeps the face recognisable.
  parameters:
  - name: script
    type: text
    label: Dialogue script (what the character says)
    required: true
  - name: voice_id
    type: string
    label: Voice preset (optional; the character's own voice otherwise)
    required: false
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - script
    - voice_id
    instruction: Make a talking-portrait dialogue video of the brand's presenter character saying {script}, spoken in the
      voice preset {voice_id} when one is given. Add subtle motion and keep the character's face and features exact.
---

# Talking portrait

Slash command: /image-to-dialogue

## Step 1: Make the portrait speak

Generate a talking-portrait video of the brand character (never an uploaded photo of a real person).
Inputs:
- script: dialogue script (rich text)
- voiceId: voice preset (optional)
Pipeline: kling-clip + elevenlabs-tts
Lip-sync the portrait (Avatar or any face) to the generated speech. Identity and facial features preserved.
