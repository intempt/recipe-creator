---
name: pack-shot
description: |
  Use when a user mentions "pack shot", "product shot", "studio shot", "catalog photo", or asks for clean product photography. Studio-clean product stills from one SKU.
arguments: []
intempt:
  id: pack-shot
  version: 1.0.0
  slashCommand: /pack-shot
  group: Creative
  shortDescription: "Generate one studio-clean product image from a catalog SKU and selected scene preset."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, product, pack-shot]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Select product and scene"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Pick a catalog product (SKU) and a scene for background and lighting, then render pack-shot variants."
      prompt: |
        Generate studio pack-shot images for the selected product.

        Inputs:
        - productId: catalog SKU to photograph
        - sceneId: background + lighting preset

        Pipeline: nano-banana-pro/edit
        Runner: pack-shot (custom)

        Produce a kit of clean studio shots (front, three-quarter, detail, lifestyle inserts) from the single catalog product using the chosen scene for background and lighting.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Generated pack-shot image." }
---

# Pack Shot

## Procedure

1. **Select product and scene** [`generate_image`] — Pick a catalog product (SKU) and a scene for background and lighting, then render pack-shot variants. → produces: image

   ```text
   Generate studio pack-shot images for the selected product.

   Inputs:
   - productId: catalog SKU to photograph
   - sceneId: background + lighting preset

   Pipeline: nano-banana-pro/edit
   Runner: pack-shot (custom)

   Produce a kit of clean studio shots (front, three-quarter, detail, lifestyle inserts)
   from the single catalog product using the chosen scene for background and lighting.
   ```

## Notes

- Uses the `pack-shot` custom runner in the content builder.
- fal.ai pipeline: nano-banana-pro/edit.
- Corresponds to the `packshot` tile on the Design Home page.
