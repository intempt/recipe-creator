---
name: ugc-photo
description: |
  Use when a user mentions "UGC photo", "user-generated content", "candid photo", "handheld photo", "selfie with product", or asks for authentic-looking product photos. Studio packshot to candid handheld.
arguments: []
intempt:
  id: ugc-photo
  version: 1.0.0
  slashCommand: /ugc-photo
  group: Creative
  title: 'UGC-style product photo'
  shortDescription: 'Re-shoots a studio packshot as a candid handheld phone photo of a real person holding the product.'
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
      title: 'Reshoot as a candid photo'
      command: generate_image
      produces: image
      bindsAs: image
      description: 'Re-renders the same product as a handheld selfie: a real person holding it at arm''s length, a kitchen or bathroom counter behind, real skin texture and slightly underexposed. Authentic rather than glamour.'
      prompt: |
        Re-shoot a product as a candid UGC photo.

        Take the same product and re-render as a candid handheld selfie: real person holding the product at arm's length, kitchen/bathroom counter behind, real skin texture, half-face cropped, slightly underexposed. Authentic, not glamour.

        Pipeline: flux-pro/kontext (style transfer with product identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "UGC-style product photo." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# UGC-style product photo

Re-shoots a studio packshot as a candid handheld phone photo of a real person holding the product.

## What it does

1. **Reshoot as a candid photo** (`generate_image`)

   Re-renders the same product as a handheld selfie: a real person holding it at arm's length, a kitchen or bathroom counter behind, real skin texture and slightly underexposed. Authentic rather than glamour.

## What you end up with

- **image** (image): UGC-style product photo.
