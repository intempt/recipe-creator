---
frontmatter_id: product-swap
slash_command: /product-swap
description: Replaces the product in a shot you already have with a different one, keeping the scene, lighting and shadow the same.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Replaces the product in an existing photo with a different one, keeping the scene, lighting, shadow and backdrop
    unchanged.
  parameters:
  - name: product_image
    type: attachment
    label: Product image to swap in
    required: true
  requirements:
  - slot: source_shot
    kind: knowledge
    meaning: An existing product photo of a scene that the new product will be placed into
  - slot: new_product
    kind: product_feed
    meaning: The new product chosen for this run that will replace the product in the shot
  steps:
  - id: s1
    builds: image
    uses:
    - source_shot
    - new_product
    - product_image
    instruction: Edit the image attached to this run. Replace only the product with {new_product} at identical size and position.
      Keep the scene, lighting, shadow and backdrop unchanged.
---

# Product swap in a scene

Slash command: /product-swap

## Step 1: Swap in the new product

Edit the image attached to this run.
Replace only the product with the new product chosen for this run, at identical size and position.
Keep the scene, lighting, shadow and backdrop unchanged.
