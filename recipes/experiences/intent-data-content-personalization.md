---
name: Intent Data Content Personalization
description: Show different content blocks based on the visitor's recent on-site behavioral signals (viewed pricing 2x → ROI
  calculator; downloaded security paper → security case study). Behavior-driven, not firmographic.
intempt:
  id: intent-data-content-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Show different content blocks based on the visitor's recent on-site behavioral signals (viewed pricing
    2x → ROI calculator; downloaded security paper → security case study). Behavior-driven, not firmographic.
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

# Intent Data Content Personalization

Show different content blocks based on the visitor's recent on-site behavioral signals (viewed pricing 2x → ROI calculator; downloaded security paper → security case study). Behavior-driven, not firmographic.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
