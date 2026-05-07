---
name: Onboarding Flow Guided Vs Self Serve
description: Test whether a guided wizard or self-serve checklist or video-first onboarding produces faster time-to-value.
  Client experiment.
intempt:
  id: onboarding-flow-guided-vs-self-serve
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test whether a guided wizard or self-serve checklist or video-first onboarding produces faster time-to-value.
    Client experiment.
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

# Onboarding Flow Guided Vs Self Serve

Test whether a guided wizard or self-serve checklist or video-first onboarding produces faster time-to-value. Client experiment.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
