---
name: packaging-mockup
description: |
  Use when a user mentions "packaging mockup", "label mockup", "wrap label", "packaging design", or asks to wrap flat label artwork onto a 3D package. Flat label → wrapped on 3D pack.
arguments: []
intempt:
  id: packaging-mockup
  version: 1.0.0
  slashCommand: /packaging-mockup
  group: Creative
  shortDescription: 'Flat label to wrapped on 3D pack.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [image, packaging, mockup, label]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Wrap label onto package"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Take flat 2D label artwork and wrap it photorealistically around a 3D package (can, bottle, box)."
      prompt: |
        Wrap flat label artwork onto a 3D package.

        Take the SAME label artwork (identical wordmark, identical layout) and wrap it photorealistically around a 3D package on the same backdrop. Label content preserved exactly.

        Pipeline: flux-pro/kontext (label wrapping with identity lock)
  outputs:
    - { name: image, type: image, cardinality: single, description: "Packaging mockup image." }
---

# Packaging Mockup

## Procedure

1. **Wrap label onto package** [`generate_image`] — Flat artwork → 3D package render. → produces: image

## Notes

- Pipeline: flux-pro/kontext.
- Label content and branding preserved exactly during 3D wrapping.
- Related to but distinct from the general `mockup` recipe (which handles apparel, print, billboard).
