---
name: accessory-try-on
description: |
  Use when a user mentions "accessory try-on", "try on glasses", "try on jewelry", "try on watch", "virtual try-on", or asks to place an accessory on an AI model. Eyewear, jewelry, watches on model.
arguments: []
intempt:
  id: accessory-try-on
  version: 1.0.0
  slashCommand: /accessory-try-on
  group: Creative
  shortDescription: "Eyewear, jewelry, watches on model."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, accessory, try-on]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Place accessory on model"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take a packshot of an accessory (eyewear, jewelry, watch) and place it on an AI model."
      prompt: |
        Place the accessory on an AI model.

        Take the exact same accessory and place it on the face/wrist/body of an AI model, shoulders-up, candid, real skin. Soft window light, neutral backdrop. Accessory identity preserved exactly.

        Pipeline: flux-pro/kontext (accessory placement with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Accessory try-on image." }
---

# Accessory Try-On

## Procedure

1. **Place accessory on model** [`generate_image`] — Packshot → accessory worn by AI model. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Supports eyewear, jewelry, watches, and other wearable accessories.
