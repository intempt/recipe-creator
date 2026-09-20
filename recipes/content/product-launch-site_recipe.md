---
name: product-launch-site
description: |
  Use when a user mentions "product launch site", "landing page", "microsite", "launch page", or asks to create a product launch landing page or microsite. One or more pages, deploy in a click.
arguments: []
intempt:
  id: product-launch-site
  version: 1.0.0
  slashCommand: /product-launch-site
  group: Content
  title: "Product launch microsite"
  shortDescription: "Builds a small launch site (hero, feature pages, call to action, footer) in your brand styling, ready to publish in one click."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [content]
    agent: creative-assistant
    mode: [all]
    complexity: standard
    executionMode: oneshot
    tags: [site, landing-page, product-launch]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_content
  procedure:
    - step: 1
      title: "Build the launch microsite"
      command: create_content
      produces: content
      bindsAs: content
      description: "A multi-page site with a hero, feature and benefit pages, a call to action and a footer, using your brand styling and deployable in one click."
      prompt: |
        Create a product launch microsite.

        Build a multi-page site with: hero section, feature/benefit pages, call-to-action, and footer. Apply project brand tokens. Deploy-ready in one click.

        Output: multi-page microsite
  outputs:
    - { name: content, type: content, cardinality: single, description: "Product launch microsite." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Product launch microsite

Builds a small launch site (hero, feature pages, call to action, footer) in your brand styling, ready to publish in one click.

## What it does

1. **Build the launch microsite** (`create_content`)

   A multi-page site with a hero, feature and benefit pages, a call to action and a footer, using your brand styling and deployable in one click.

## What you end up with

- **content** (content): Product launch microsite.
