---
frontmatter_id: talking-avatar
slash_command: /talking-avatar
description: Makes a talking-head video of your brand character saying the words you write.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Makes a 5-second talking-head video of your brand character saying the words you write, with subtle lip
    movement, gentle eye contact and a single blink.
  parameters:
  - name: script
    type: text
    label: What the presenter says (at least a sentence or two)
    required: true
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
  requirements: []
  steps:
  - id: s1
    builds: video
    uses:
    - script
    - clip_length
    - camera_motion
    instruction: Make a talking avatar video of the brand's presenter character saying {script}. Keep the camera {camera_motion}.
      Make a {clip_length} natural talking-head clip with subtle lip movement, gentle eye contact and a single blink.
---

# Talking head from a portrait

Slash command: /talking-avatar

## Step 1: Animate the portrait

Make a talking-head video of the brand character (the brand's own avatar; never an uploaded photo of a real person) saying the words you write.
Camera fixed. 5s natural talking-head clip: subtle lip movement, gentle eye contact, single blink.
Pipeline: brand character + catalog voice → avatar video
