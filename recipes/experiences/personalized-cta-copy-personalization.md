---
name: Personalized Cta Copy Personalization
description: 'Show personalized CTA copy per audience segment (first-time: "Start your free trial"; returning: "Continue where
  you left off"; existing customer: "Upgrade to Pro"). 202% lift cited.'
intempt:
  id: personalized-cta-copy-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: 'Show personalized CTA copy per audience segment (first-time: "Start your free trial"; returning: "Continue
    where you left off"; existing customer: "Upgrade to Pro"). 202% lift cited.'
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

# Personalized Cta Copy Personalization

Show personalized CTA copy per audience segment (first-time: "Start your free trial"; returning: "Continue where you left off"; existing customer: "Upgrade to Pro"). 202% lift cited.

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
