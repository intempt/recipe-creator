---
frontmatter_id: pack-shot
slash_command: /pack-shot
description: Generates clean studio stills of one catalog product, in a background and lighting you pick.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Generates four clean studio product images of one catalog item in a background and lighting of your choice.
  parameters:
  - name: background
    type: string
    label: Studio background
    default: <UNKNOWN>
    required: true
  - name: lighting
    type: string
    label: Studio lighting
    default: <UNKNOWN>
    required: true
  requirements:
  - slot: product_catalog
    kind: product_feed
    meaning: The product catalog containing the item to be photographed
  steps:
  - id: s1
    builds: image
    uses:
    - product_catalog
    - background
    - lighting
    instruction: 'Generate four studio images of {product_catalog} for the product chosen for this run: front view, three-quarter
      view, a detail close-up, and a lifestyle insert. Use {background} as the background and {lighting} as the lighting for
      all four images.'
---

# Studio product shots

Slash command: /pack-shot

## Step 1: Render the product

Generate four studio images of the catalog product chosen for this run: front, three-quarter, a detail close-up, and a lifestyle insert.
Use the background and lighting of the scene chosen for this run.
