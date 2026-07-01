---
name: ad-variants
description: |
  Use when a user mentions "ad variants", "ad variations", "swap headline", "swap palette", "A/B ad creative", or asks for multiple versions of an existing ad. One ad in, six tested variants out.
arguments: []
intempt:
  id: ad-variants
  version: 1.0.0
  slashCommand: /ad-variants
  group: Creative
  shortDescription: "One ad in, six tested variants out."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, ad, variants]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Generate ad variants"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Upload an existing ad and select swap dimensions to fan out tested variants."
      prompt: |
        Generate ad variants from an existing ad.

        Inputs:
        - adImage: existing ad image (file upload)
        - swaps: dimensions to vary (headline, palette, background, model, CTA, aspect)

        Pipeline: restyle × N (one per swap dimension)

        Fan out one focused variation per swap dimension. Six variants total covering headline, palette, background, model, CTA, and aspect ratio.
  outputs:
    - { name: image, type: image, cardinality: list, description: "6 ad variants." }
---

# Ad Variants

## Procedure

1. **Generate ad variants** [`generate_image`] — Upload an existing ad and select swap dimensions to fan out tested variants. → produces: image

   ```text
   Swap dimensions: headline, palette, background, model, CTA, aspect
   Pipeline: restyle × N (one per swap)
   ```

## Notes

- fal.ai pipeline: restyle × N (one call per swap dimension).
- Produces up to 6 variants from a single ad input.
