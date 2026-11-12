---
frontmatter_id: accessory-try-on
slash_command: /accessory-try-on
description: Takes a packshot of eyewear, jewelry or a watch and shows it worn by an AI model, with the accessory itself unchanged.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a packshot of eyewear, jewelry or a watch into an image of an AI model wearing it, with the accessory left
    unchanged.
  parameters:
  - name: framing
    type: string
    label: Model framing
    default: shoulders up
    required: false
  - name: pose
    type: string
    label: Model pose
    default: candid
    required: false
  - name: lighting
    type: string
    label: Lighting
    default: soft window light
    required: false
  - name: backdrop
    type: string
    label: Backdrop
    default: plain neutral
    required: false
  requirements:
  - slot: accessory_photo
    kind: knowledge
    meaning: A packshot photo of an eyewear, jewelry or watch accessory attached to the run
  steps:
  - id: s1
    builds: image
    uses:
    - accessory_photo
    - framing
    - pose
    - lighting
    - backdrop
    instruction: Generate one image from {accessory_photo}. Show that exact accessory worn by an AI model, on the face, wrist
      or body, wherever that accessory is worn. Frame the model {framing}, in a {pose} pose, with real skin texture. Use {lighting}
      and a {backdrop} backdrop. Do not change the accessory's shape, colour, material, markings or proportions.
---

# Accessory on a model

Slash command: /accessory-try-on

## Step 1: Put the accessory on a model

Generate one image from the accessory photo attached to this run.
Show that exact accessory worn by an AI model, on the face, wrist or body, wherever that accessory is worn.
Frame the model from the shoulders up, in a candid pose, with real skin texture.
Use soft window light and a plain neutral backdrop.
Do not change the accessory's shape, colour, material, markings or proportions.
