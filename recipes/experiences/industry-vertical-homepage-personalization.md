---
name: Industry Vertical Homepage Personalization
description: Show different homepage hero, social proof, and messaging based on the visitor's detected industry (4-5 segments).
  Demandbase pattern; distinct from per-account ABM.
intempt:
  id: industry-vertical-homepage-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Show different homepage hero, social proof, and messaging based on the visitor's detected industry (4-5
    segments). Demandbase pattern; distinct from per-account ABM.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - saas
    - b2b
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

# Industry Vertical Homepage Personalization

Show different homepage hero, social proof, and messaging based on the visitor's detected industry (4-5 segments). Demandbase pattern; distinct from per-account ABM.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
