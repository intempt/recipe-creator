---
name: Returning Vs New Visitor Personalization
description: Show new visitors a value proposition; show returning visitors continuation cues (recently viewed, abandoned
  cart). Client personalization based on prior session history.
intempt:
  id: returning-vs-new-visitor-personalization
  version: 1.0.1
  slashCommand: /personalization-recipe
  shortDescription: Show new visitors a value proposition; show returning visitors continuation cues (recently viewed, abandoned
    cart). Client personalization based on prior session history.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - ecommerce
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

# Returning Vs New Visitor Personalization

Show new visitors a value proposition; show returning visitors continuation cues (recently viewed, abandoned cart). Client personalization based on prior session history.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
