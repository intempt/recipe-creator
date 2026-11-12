---
frontmatter_id: ad-builder
slash_command: /ad-builder
description: Turns a catalog product and a headline into a finished ad laid out in your Brand Kit colours, fonts and layout.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Turns a catalog product and a headline into one finished ad image laid out in your brand colours, fonts and layout.
  parameters:
  - name: headline
    type: text
    label: Ad headline text
    required: true
  - name: product
    type: string
    label: Catalog product for this run
    required: true
  - name: brand_layout
    type: string
    label: Brand Kit ad recipe to use for colours, fonts and layout
    required: true
  requirements:
  - slot: product_catalog
    kind: product_feed
    meaning: A product catalog containing the products to advertise
  - slot: brand_kit
    kind: brand
    meaning: A brand kit defining colours, fonts and ad layouts
  steps:
  - id: s1
    builds: image
    uses:
    - product_catalog
    - brand_kit
    - product
    - headline
    - brand_layout
    instruction: Generate one finished ad image. Show the product {product} from {product_catalog}. Use {headline} as the
      ad's headline text. Take the colours, fonts and layout from the Brand Kit ad recipe {brand_layout} in {brand_kit}.
---

# Branded ad from a product

Slash command: /ad-builder

## Step 1: Build the ad

Generate one finished ad image.
Show the catalog product chosen for this run.
Use the headline written for this run as the ad's headline text.
Take the colours, fonts and layout from the Brand Kit ad recipe chosen for this run.
