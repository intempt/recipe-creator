---
id: flash-sale-sms
title: Flash sale text message
slash_command: /flash-sale-sms
group: Content
owner: intempt
summary: Writes a short text message for a time-limited offer, inside SMS character limits, with a short
  link to the offer page.
description: >-
  Urgency-driven short copy.
version: 2.0.0
classification:
  product:
    - content
  agent: creative-assistant
  mode:
    - all
  complexity: quick
  executionMode: oneshot
  tags:
    - sms
    - flash-sale
    - urgency
steps:
  - id: s1
    title: Write the flash sale SMS
    summary: >-
      Direct, time-limited copy that fits SMS character limits, with a short link and preview card for
      the offer landing page.
    builds: content
    description: |-
      Create a flash sale SMS message.
      Write urgency-driven short copy optimized for SMS character limits. Include a short.link preview card for the offer landing page. Tone: direct, time-limited, action-oriented.
      Output: SMS message with link preview
outputs:
  - key: content
    producedByStep: s1
    type: content
    description: Flash sale SMS message.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Flash sale text message

Writes a short text message for a time-limited offer, inside SMS character limits, with a short link to the offer page.

## Steps

1. **Write the flash sale SMS** (builds content)

   Direct, time-limited copy that fits SMS character limits, with a short link and preview card for the offer landing page.

## What you end up with

- **content** (content): Flash sale SMS message.

## Availability

Coming soon: waiting on the engine to build content.
