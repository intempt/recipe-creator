---
name: image-remix
description: |
  Use when a user mentions "image remix", "remix", "reference-based variations", "pinboard variations", or asks for variations from reference images. Reference-anchored variations from your pinboard.
arguments: []
intempt:
  id: image-remix
  version: 1.0.0
  slashCommand: /image-remix
  group: Creative
  shortDescription: "Generate a list of image variations anchored to 1–4 reference images with Light/Medium/Strong weights."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, remix, reference]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Pin references and generate variations"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Pin 1–4 reference images each with Light/Medium/Strong weight, then fan out variations."
      prompt: |
        Generate image variations from reference pins.

        Inputs:
        - references: 1–4 reference images (canvas snapshot, scene, avatar, or upload) each with weight (Light/Medium/Strong)
        - fanout: number of variations to generate (default: 4)

        Pipeline: nano-banana-pro with reference_images[] and per-weight prompt directives
        Runner: image-remix (custom)

        Fan out on-brand variations anchored to the reference images. Each reference's weight controls how strongly it influences the output.
  outputs:
    - { name: image, type: image, cardinality: list, description: "Remixed image variations." }
---

# Image Remix

## Procedure

1. **Pin references and generate variations** [`generate_image`] — Pin 1–4 reference images each with Light/Medium/Strong weight, then fan out variations. → produces: image

   ```text
   Pin 1–4 reference images with per-pin weight (Light/Medium/Strong).
   Fan out N on-brand variations anchored to the references.
   Pipeline: nano-banana-pro + reference_images[]
   ```

## Notes

- Uses the `image-remix` custom runner.
- fal.ai pipeline: nano-banana-pro with reference_images[].
