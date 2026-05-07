---
name: Lifecycle Stage Homepage Personalization
description: Show different homepage hero content based on the visitor's canonical lifecycle_score (At risk, Champions, etc.).
  Client personalization for ecommerce.
intempt:
  id: lifecycle-stage-homepage-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Show different homepage hero content based on the visitor's canonical lifecycle_score (At risk, Champions,
    etc.). Client personalization for ecommerce.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - personalization
    - client
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: experience
    type: experience
    description: Website personalization created on /experiences.
  steps:
  - id: configure-website-personalization
    describe: 'Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content
      (Path 2).'
    produces: experience
---

# Lifecycle Stage Homepage Personalization

Show different homepage hero content based on the visitor's canonical lifecycle_score (At risk, Champions, etc.). Client personalization for ecommerce.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
