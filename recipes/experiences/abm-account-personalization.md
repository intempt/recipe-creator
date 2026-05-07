---
name: Abm Account Personalization
description: Personalize homepage hero (logo, industry-specific messaging) per identified target account. The canonical Mutiny/Demandbase
  pattern. Requires firmographic enrichment.
intempt:
  id: abm-account-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Personalize homepage hero (logo, industry-specific messaging) per identified target account. The canonical
    Mutiny/Demandbase pattern. Requires firmographic enrichment.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - b2b
    - saas
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

# Abm Account Personalization

Personalize homepage hero (logo, industry-specific messaging) per identified target account. The canonical Mutiny/Demandbase pattern. Requires firmographic enrichment.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
