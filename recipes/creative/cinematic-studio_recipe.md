---
name: cinematic-studio
description: |
  Use when a user mentions "cinematic", "cinematic looks", "film grade", "color grade", "Wes Anderson look", or asks for cinematic styling of an image. Nine cinematic looks from one frame.
arguments: []
intempt:
  id: cinematic-studio
  version: 1.0.0
  slashCommand: /cinematic-studio
  group: Creative
  shortDescription: "Generate a 3x3 board of nine cinematic color-graded restyles from one input image."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [design]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [image, cinematic]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - generate_image
  procedure:
    - step: 1
      title: "Generate cinematic board"
      command: generate_image
      produces: image
      bindsAs: image
      description: "Drop in any image and receive a 3×3 board of cinematic looks inspired by iconic cinematographers."
      prompt: |
        Generate a 3×3 board of cinematic looks from one input image.

        Inputs:
        - image: source image (file upload)

        Pipeline: restyle × 9 (parallel)

        Produce 9 cinematic looks (Wes Anderson, Roger Deakins, Lubezki, Christopher Doyle, Bradford Young, etc.). The user picks one to promote to the canvas.
  outputs:
    - { name: image, type: image, cardinality: list, description: "9 cinematic looks." }
---

# Cinematic Studio

## Procedure

1. **Generate cinematic board** [`generate_image`] — Drop in any image and receive a 3×3 board of cinematic looks. → produces: image

   ```text
   Input: any image
   Pipeline: restyle × 9 (parallel)
   Output: 3×3 board of cinematic grading options
   ```

## Notes

- fal.ai pipeline: restyle × 9 in parallel.
- Cinematic references: Wes Anderson, Roger Deakins, Lubezki, Christopher Doyle, Bradford Young, and more.
