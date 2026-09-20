---
name: ugc-photo
description: |
  Use when a user mentions "UGC photo", "user-generated content", "candid photo", "handheld photo", "selfie with product", or asks for authentic-looking product photos. Studio packshot → candid handheld.
arguments: []
intempt:
  id: ugc-photo
  version: 1.0.0
  slashCommand: /ugc-photo
  group: Creative
  shortDescription: 'Studio packshot to candid handheld.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, ugc, candid]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Generate UGC photo"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Re-shoot a studio packshot as a candid handheld iPhone selfie with the product."
      prompt: |
        Re-shoot a product as a candid UGC photo.

        Take the same product and re-render as a candid handheld selfie: real person holding the product at arm's length, kitchen/bathroom counter behind, real skin texture, half-face cropped, slightly underexposed. Authentic, not glamour.

        Pipeline: flux-pro/kontext (style transfer with product identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "UGC-style product photo." }
---

# UGC Photo

## Procedure

1. **Generate UGC photo** [`generate_image`] — Packshot → candid handheld selfie. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Authentic candid feel — not glamour photography.
