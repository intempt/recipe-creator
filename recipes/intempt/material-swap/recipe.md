---
frontmatter_id: material-swap
slash_command: /material-swap
description: Changes the material, finish or colour of a product while the shape, pose, camera angle and shadow stay exactly as shot.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
  - marketplaces
portable:
  summary: Changes a product's material, finish or colour in its image while keeping the shape, pose, camera angle and shadow
    exactly as shot.
  parameters:
  - name: new_material
    type: string
    label: New material, finish or colour
    required: true
  requirements:
  - slot: product_image
    kind: knowledge
    meaning: A product image attached to the run that will be edited
  steps:
  - id: s1
    builds: image
    uses:
    - product_image
    - new_material
    instruction: Edit the product image {product_image}. Change only the product's surface material to {new_material}. Keep
      the frame, the pose, the camera angle and the shadow identical.
---

# Material and finish swap

Slash command: /material-swap

## Step 1: Swap the material

Edit the product image attached to this run.
Change only the product's surface material to the new material chosen for this run.
Keep the frame, the pose, the camera angle and the shadow identical.
