---
name: Upgrade Prompt Optimization
description: 'Combined test of upgrade prompt placement (where) and timing (when) for free SaaS users. Two creation flows:
  client variants for placement, server payload for timing.'
intempt:
  id: upgrade-prompt-optimization
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: 'Combined test of upgrade prompt placement (where) and timing (when) for free SaaS users. Two creation
    flows: client variants for placement, server payload for timing.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - saas
    complexity: standard
    executionMode: live
    tags:
    - experiment
    - client
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: experience
    type: experience
    description: Website experiment created on /experiences.
  steps:
  - id: configure-website-experiment
    describe: 'Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content
      (Path 2).'
    produces: experience
---

# Upgrade Prompt Optimization

Combined test of upgrade prompt placement (where) and timing (when) for free SaaS users. Two creation flows: client variants for placement, server payload for timing.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
