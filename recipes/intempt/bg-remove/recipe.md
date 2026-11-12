---
frontmatter_id: bg-remove
slash_command: /bg-remove
description: Strips the backdrop and shadow from a product image and returns a transparent cutout you can drop anywhere.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Removes the backdrop and shadow from a product image and returns a transparent cutout that can be placed anywhere.
  parameters: []
  requirements:
  - slot: product_image
    kind: knowledge
    meaning: A product image attached to the run that needs its backdrop removed
  steps:
  - id: s1
    builds: image
    uses:
    - product_image
    instruction: Edit {product_image}. Remove the backdrop and the shadow and replace them with a transparent background.
      Keep the product in exactly the same position, and do not re-render or alter it.
---

# Background removal

Slash command: /bg-remove

## Step 1: Cut out the product

Edit the product image attached to this run.
Remove the backdrop and the shadow and replace them with a transparent background.
Keep the product in exactly the same position, and do not re-render or alter it.
