---
name: mockup
description: |
  Use when a user mentions "mockup", "product mockup", "t-shirt mockup", "mug mockup", "billboard mockup", or asks to composite artwork onto a physical object. Apparel, print, packaging — mockup in one click.
arguments: []
intempt:
  id: mockup
  version: 1.0.0
  slashCommand: /mockup
  group: Creative
  shortDescription: "Generate a realistic product mockup compositing artwork onto apparel, packaging, or print items."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, mockup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Composite artwork onto mockup"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Drop in artwork and a mockup scene (t-shirt, mug, billboard, packaging) to composite with realistic lighting and warping."
      prompt: |
        Generate a product mockup.

        Inputs:
        - artwork: artwork file (upload)
        - mockupScene: mockup scene preset (t-shirt, mug, billboard, packaging, etc.)

        Pipeline: restyle → nano-banana-pro/edit

        Composite the artwork onto the mockup scene with realistic lighting, perspective warping, and material-appropriate rendering.
  outputs:
    - { name: image, type: image, cardinality: single, description: "Mockup image." }
---

# Mockup

## Procedure

1. **Composite artwork onto mockup** [`generate_image`] — Drop in artwork and a mockup scene to composite with realistic lighting and warping. → produces: image

   ```text
   Inputs: artwork (file upload), mockupScene (preset)
   Pipeline: restyle → nano-banana-pro/edit
   ```

## Notes

- fal.ai pipeline: restyle → nano-banana-pro/edit.
- Supports apparel, print, packaging, and billboard mockup scenes.
