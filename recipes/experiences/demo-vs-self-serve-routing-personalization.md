---
name: Demo Vs Self Serve Routing Personalization
description: Show enterprise visitors a demo CTA, smaller-company visitors a self-serve CTA. Client personalization with firmographic
  audience targeting (no random split).
intempt:
  id: demo-vs-self-serve-routing-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Show enterprise visitors a demo CTA, smaller-company visitors a self-serve CTA. Client personalization
    with firmographic audience targeting (no random split).
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

# Demo Vs Self Serve Routing Personalization

Show enterprise visitors a demo CTA, smaller-company visitors a self-serve CTA. Client personalization with firmographic audience targeting (no random split).

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
