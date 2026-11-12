---
frontmatter_id: flatlay
slash_command: /flatlay
description: Arranges your product in a top-down flatlay with complementary props styled around it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a top-down product photo into a styled flatlay by adding complementary props around the product while keeping
    its position, angle and lighting.
  parameters: []
  requirements:
  - slot: product_image
    kind: knowledge
    meaning: A top-down product image attached to the run to be edited
  steps:
  - id: s1
    builds: image
    uses:
    - product_image
    instruction: Edit the top-down flatlay product image {product_image}. Add complementary props arranged around the product.
      Keep the product in the same position, and keep the top-down angle and the lighting unchanged.
---

# Styled flatlay

Slash command: /flatlay

## Step 1: Style the flatlay

Edit the top-down flatlay product image attached to this run.
Add complementary props arranged around the product.
Keep the product in the same position, and keep the top-down angle and the lighting unchanged.
