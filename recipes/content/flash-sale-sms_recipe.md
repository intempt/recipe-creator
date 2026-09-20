---
name: flash-sale-sms
description: |
  Use when a user mentions "flash sale SMS", "SMS blast", "urgency SMS", "text message campaign", or asks to create a flash sale text message. Urgency-driven short copy.
arguments: []
intempt:
  id: flash-sale-sms
  version: 1.0.0
  slashCommand: /flash-sale-sms
  group: Content
  title: "Flash sale text message"
  shortDescription: "Writes a short text message for a time-limited offer, inside SMS character limits, with a short link to the offer page."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [content]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [sms, flash-sale, urgency]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_content
  procedure:
    - step: 1
      title: "Write the flash sale SMS"
      command: create_content
      produces: content
      bindsAs: content
      description: "Direct, time-limited copy that fits SMS character limits, with a short link and preview card for the offer landing page."
      prompt: |
        Create a flash sale SMS message.

        Write urgency-driven short copy optimized for SMS character limits. Include a short.link preview card for the offer landing page. Tone: direct, time-limited, action-oriented.

        Output: SMS message with link preview
  outputs:
    - { name: content, type: content, cardinality: single, description: "Flash sale SMS message." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Flash sale text message

Writes a short text message for a time-limited offer, inside SMS character limits, with a short link to the offer page.

## What it does

1. **Write the flash sale SMS** (`create_content`)

   Direct, time-limited copy that fits SMS character limits, with a short link and preview card for the offer landing page.

## What you end up with

- **content** (content): Flash sale SMS message.
