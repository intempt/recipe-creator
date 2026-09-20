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
  title: "Product launch announcement email"
  shortDescription: "Writes a launch-day email in your brand colors and fonts, with the product hero image and a subject line written for opens and clicks."
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
      title: "Write the announcement email"
      command: create_content
      produces: content
      bindsAs: content
      description: "A ready-to-send email using your brand colors, fonts and logo, with a product hero block and a subject line written for open and click rate."
      prompt: |
        Create a product announcement email.

        Apply the project's brand tokens (colors, fonts, logo). Include a product hero block with the featured product image. Write an announcement subject line and body copy optimized for open rate and click-through.

        Output: ready-to-send email template
  outputs:
    - { name: content, type: content, cardinality: single, description: "Product announcement email." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product launch announcement email

Writes a launch-day email in your brand colors and fonts, with the product hero image and a subject line written for opens and clicks.

## What it does

1. **Write the announcement email** (`create_content`)

   A ready-to-send email using your brand colors, fonts and logo, with a product hero block and a subject line written for open and click rate.

## What you end up with

- **content** (content): Product announcement email.
