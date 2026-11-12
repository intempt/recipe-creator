---
frontmatter_id: interior-staging
slash_command: /interior-staging
description: Furnishes a photo of an empty room, leaving the walls, floor, windows and daylight exactly as they were shot.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - marketplaces
portable:
  summary: Adds staged furniture and decor to a photo of an empty room while keeping its walls, floor, windows and natural
    daylight exactly as shot.
  parameters:
  - name: room_photo
    type: attachment
    label: Photo of the empty room
    required: true
  - name: staging_style
    type: text
    label: Staging style or room use
    default: suits the room
    required: false
  requirements:
  - slot: empty_room_photo
    kind: knowledge
    meaning: A photo of an empty room to be virtually staged
  steps:
  - id: s1
    builds: image
    uses:
    - empty_room_photo
    - room_photo
    - staging_style
    instruction: Edit the photo of an empty room attached to this run ({room_photo}). Furnish it with furniture, a coffee
      table, a vase, a floor lamp and other staging that suits the room, in the style {staging_style}. Keep the room geometry,
      walls, flooring, windows and daylight unchanged.
---

# Virtual interior staging

Slash command: /interior-staging

## Step 1: Furnish the empty room

Edit the photo of an empty room attached to this run.
Furnish it with furniture, a coffee table, a vase, a floor lamp and other staging that suits the room.
Keep the room geometry, walls, flooring, windows and daylight unchanged.
