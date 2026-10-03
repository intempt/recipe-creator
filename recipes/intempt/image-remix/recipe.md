---
id: image-remix
title: Reference-anchored remix
slash_command: /image-remix
group: Creative
owner: intempt
summary: Pin up to four reference images with a weight on each, and get back variations anchored to them
  (four by default).
description: >-
  Reference-anchored variations from your pinboard.
version: 2.0.0
classification:
  product:
    - design
  agent: creative-assistant
  mode:
    - all
  complexity: standard
  executionMode: oneshot
  tags:
    - image
    - remix
    - reference
inputs:
  - input: References
    what_the_installer_supplies: One to four images (a canvas snapshot, scene, avatar or upload), each
      with a weight of Light, Medium or Strong
    if_missing: The step is marked vague and waits until at least one is pinned.
  - input: Number of variations
    what_the_installer_supplies: How many variations to generate
    if_missing: Four are generated.
touches:
  reads:
    - The weight attribute on users
    - The references you supply when you run it
    - The number of variations you supply when you run it
  writes:
    - A new image, from step 1 "Pin references and fan out"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Pin references and fan out
    summary: >-
      You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light,
      Medium or Strong. The weight decides how strongly that reference pulls the output.
    builds: image
    description: |-
      Generate four image variations from the reference images pinned to this run.
      Use between one and four references, each with a weight of Light, Medium or Strong.
      A Strong reference shapes each variation most, Medium less, and Light least.
outputs:
  - key: image
    producedByStep: s1
    type: image
    description: Remixed image variations.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Reference-anchored remix

Pin up to four reference images with a weight on each, and get back variations anchored to them (four by default).

## Steps

1. **Pin references and fan out** (builds image)

   You pin one to four references (a canvas snapshot, scene, avatar or upload) and set each to Light, Medium or Strong. The weight decides how strongly that reference pulls the output.

## What you end up with

- **image** (image): Remixed image variations.

## What this recipe touches

Reads:

- The weight attribute on users
- The references you supply when you run it
- The number of variations you supply when you run it

Writes:

- A new image, from step 1 "Pin references and fan out"

Never:

- Nothing runs until you approve the plan in Blu.

## Declared inputs

| Input | What the installer supplies | If missing |
|---|---|---|
| References | One to four images (a canvas snapshot, scene, avatar or upload), each with a weight of Light, Medium or Strong | The step is marked vague and waits until at least one is pinned. |
| Number of variations | How many variations to generate | Four are generated. |

## Availability

Install now: every step builds something the engine supports today.
