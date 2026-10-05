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
  shortDescription: "Build and deploy a product launch landing page or microsite using the content builder."
  availability: available
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
      title: "Build product launch site"
      command: create_content
      produces: content
      bindsAs: content
      description: "Generate a multi-page microsite with hero, feature pages, CTA, and footer for a product launch."
      prompt: |
        Create a product launch microsite.

        Build a multi-page site with: hero section, feature/benefit pages, call-to-action, and footer. Apply project brand tokens. Deploy-ready in one click.

        Output: multi-page microsite
  outputs:
    - { name: content, type: content, cardinality: single, description: "Product launch microsite." }
---

# Product Launch Site

## Procedure

1. **Build product launch site** [`create_content`] — Generate multi-page microsite. → produces: content

## Notes

- Routes to: /content-builder?type=landing_page&microsite=1&recipe=site/product-launch
- Multi-page with hero, features, CTA, footer.
