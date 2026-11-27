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
    default: the chosen catalog product's own image when it is a real product photo, else the product drawn from its catalog
      title and description
    required: false
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
    instruction: 'Edit the scene picture attached to this run; when none is attached, use the newest saved scene picture in
      the project''s assets. Replace only the product with {new_product} (an in-stock catalog product: its catalog image when
      the catalog holds a real product photo for it; otherwise draw it from its catalog title and description in an image
      edit of the scene) at identical size and position. Keep the scene, lighting, shadow and backdrop unchanged.'
---

# Product swap in a scene

Slash command: /product-swap

## Step 1: Swap in the new product

Edit the scene picture attached to this run; when none is attached, use the newest saved scene picture in the project's assets. Replace only the product with new product (an in-stock catalog product: its catalog image when the catalog holds a real product photo for it; otherwise draw it from its catalog title and description in an image edit of the scene) at identical size and position. Keep the scene, lighting, shadow and backdrop unchanged.
