---
frontmatter_id: product-reshoot
slash_command: /product-reshoot
description: Re-lights a product photo you already have, using a setting, lighting direction and camera angle that you choose.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Relights a product photo you already have, using a chosen setting, lighting direction and camera angle, while keeping
    the product unchanged.
  parameters:
  - name: setting
    type: text
    label: Setting
    required: true
  - name: lighting_direction
    type: text
    label: Lighting direction
    required: true
  - name: camera_angle
    type: text
    label: Camera angle
    required: true
  requirements:
  - slot: product_photo
    kind: knowledge
    meaning: A product photo attached to this run that will be relit
  steps:
  - id: s1
    builds: image
    uses:
    - product_photo
    - setting
    - lighting_direction
    - camera_angle
    instruction: Edit the product photo attached to this run. Relight it with physically accurate light falloff, using the
      setting {setting}, lighting direction {lighting_direction} and camera angle {camera_angle} chosen for this run. Do not
      change the product itself.
---

# Product relight

Slash command: /product-reshoot

## Step 1: Relight the product

Edit the product photo attached to this run.
Relight it with physically accurate light falloff, using the setting, lighting direction and camera angle chosen for this run.
Do not change the product itself.
