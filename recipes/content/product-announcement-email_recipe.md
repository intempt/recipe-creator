---
name: product-announcement-email
description: |
  Use when a user mentions "product announcement email", "launch email", "email announcement", or asks to create a product launch email. Launch-day email with hero.
arguments: []
intempt:
  id: product-announcement-email
  version: 1.0.0
  slashCommand: /product-announcement-email
  group: Content
  shortDescription: "Launch-day email with hero."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [content]
    agent: creative-assistant
    mode: [all]
    complexity: quick
    executionMode: oneshot
    tags: [email, announcement, product-launch]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_content
  procedure:
    - step: 1
      title: "Compose product announcement email"
      command: create_content
      produces: content
      bindsAs: content
      description: "Generate a product announcement email with brand tokens, product hero block, and announcement subject line."
      prompt: |
        Create a product announcement email.

        Apply the project's brand tokens (colors, fonts, logo). Include a product hero block with the featured product image. Write an announcement subject line and body copy optimized for open rate and click-through.

        Output: ready-to-send email template
  outputs:
    - { name: content, type: content, cardinality: single, description: "Product announcement email." }
---

# Product Announcement Email

## Procedure

1. **Compose product announcement email** [`create_content`] — Generate email with brand tokens and product hero. → produces: content

## Notes

- Routes to: /content-builder?type=email&recipe=email/product-announcement
- Applies project brand tokens automatically.
