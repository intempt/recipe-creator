---
name: Onboarding Checklist Length
description: Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment.
intempt:
  id: onboarding-checklist-length
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment.
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

# Onboarding Checklist Length

Test whether shorter or longer in-app onboarding checklists improve 7-day activation. Client experiment.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
