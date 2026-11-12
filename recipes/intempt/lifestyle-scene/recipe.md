---
frontmatter_id: lifestyle-scene
slash_command: /lifestyle-scene
description: Moves a studio packshot into a real-world setting such as a kitchen, office or outdoors, with natural light and depth of field.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Moves a studio product packshot into a realistic setting such as a kitchen, office or outdoors, with natural light
    and depth of field, leaving the product unchanged.
  parameters:
  - name: setting
    type: enum
    label: Real-world setting
    default: kitchen
    required: false
    options:
    - kitchen
    - office
    - outdoors
  - name: lighting
    type: string
    label: Lighting style
    default: natural ambient light
    required: false
  - name: depth_of_field
    type: string
    label: Depth of field style
    default: realistic depth of field
    required: false
  requirements:
  - slot: product_packshot
    kind: knowledge
    meaning: A studio packshot image of the product to be placed in a scene
  steps:
  - id: s1
    builds: image
    uses:
    - product_packshot
    - setting
    - lighting
    - depth_of_field
    instruction: Edit the studio packshot {product_packshot}. Re-render the product in a real-world {setting} with {lighting}
      and {depth_of_field}. Do not change the product itself.
---

# Product in a real setting

Slash command: /lifestyle-scene

## Step 1: Place the product in a scene

Edit the studio packshot attached to this run.
Re-render the product in a real-world kitchen, with natural ambient light and realistic depth of field.
Do not change the product itself.
