---
frontmatter_id: on-model-shoot
slash_command: /on-model-shoot
description: Puts your identity-locked avatar in a scene wearing or holding a catalog product, for lifestyle product photography.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Creates one lifestyle product photo showing your identity-locked avatar wearing or holding a catalog product in
    a chosen scene, optionally matching a pose reference.
  parameters:
  - name: scene
    type: text
    label: Scene for this run
    default: chosen for this run
    required: false
  - name: poseReference
    type: attachment
    label: Pose reference (optional)
    required: false
  requirements:
  - slot: identity_avatar
    kind: knowledge
    meaning: An identity-locked avatar whose earlier images define the person's appearance
  - slot: product_catalog
    kind: product_feed
    meaning: A catalog of products that the avatar can wear or hold in a photo
  steps:
  - id: s1
    builds: image
    uses:
    - identity_avatar
    - product_catalog
    - scene
    - poseReference
    instruction: Generate one lifestyle product photo. Show the {identity_avatar} chosen for this run wearing or holding the
      {product_catalog} item chosen for this run, in the {scene}. If a {poseReference} is provided, match the avatar's pose
      to it. Keep the avatar's identity the same as in its earlier images.
---

# On-model product shot

Slash command: /on-model

## Step 1: Compose the on-model shot

Generate one lifestyle product photo.
Show the identity-locked avatar chosen for this run wearing or holding the catalog product chosen for this run, in the scene chosen for this run.
If pose references are chosen for this run, match the avatar's pose to them.
Keep the avatar's identity the same as in its earlier images.
