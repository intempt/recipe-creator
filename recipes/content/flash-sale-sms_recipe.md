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
  shortDescription: "Urgency-driven short copy."
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
      title: "Compose flash sale SMS"
      command: create_content
      produces: content
      bindsAs: content
      description: "Generate urgency-driven SMS copy with flash sale messaging and short link preview card."
      prompt: |
        Create a flash sale SMS message.

        Write urgency-driven short copy optimized for SMS character limits. Include a short.link preview card for the offer landing page. Tone: direct, time-limited, action-oriented.

        Output: SMS message with link preview
  outputs:
    - { name: content, type: content, cardinality: single, description: "Flash sale SMS message." }
---

# Flash Sale SMS

## Procedure

1. **Compose flash sale SMS** [`create_content`] — Generate urgency-driven SMS copy. → produces: content

## Notes

- Routes to: /content-builder?type=sms&recipe=sms/sms-flash-sale-blast
- Optimized for SMS character limits and urgency conversion.
