---
frontmatter_id: talking-avatar
slash_command: /talking-avatar
description: Turns a portrait still into a 5 second talking-head loop with subtle lip movement and eye contact.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Turns a single portrait photo into a 5-second looping talking-head video with subtle lip movement, gentle eye contact
    and a single blink.
  parameters:
  - name: clip_length
    type: duration
    label: Clip length
    default: 5 s
    required: false
  - name: camera_motion
    type: enum
    label: Camera motion
    default: fixed
    required: false
    options:
    - fixed
    - locked_off_slight_drift
  requirements:
  - slot: portrait_image
    kind: knowledge
    meaning: A portrait still photo of a person to animate
  steps:
  - id: s1
    builds: video
    uses:
    - portrait_image
    - clip_length
    - camera_motion
    instruction: Generate a talking avatar video from the {portrait_image} portrait still. Keep the camera fixed. Make a {clip_length}
      natural talking-head loop with subtle lip movement, gentle eye contact and a single blink. Preserve the identity of
      the person in the portrait exactly. Use an image-to-video pipeline with a camera-fixed talking-head setup.
---

# Talking head from a portrait

Slash command: /talking-avatar

## Step 1: Animate the portrait

Generate a talking avatar video from a portrait still.
Camera fixed. 5s natural talking-head loop: subtle lip movement, gentle eye contact, single blink. Identity preserved exactly.
Pipeline: image to video (camera-fixed, talking-head)
