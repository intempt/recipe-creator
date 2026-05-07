---
name: Source Based Personalization
description: Match landing page hero / messaging to the ad source the visitor came from (utm_source, utm_campaign, referrer).
  Cited as "the simplest high-impact personalization implementation."
intempt:
  id: source-based-personalization
  version: 1.0.0
  slashCommand: /personalization-recipe
  shortDescription: Match landing page hero / messaging to the ad source the visitor came from (utm_source, utm_campaign,
    referrer). Cited as "the simplest high-impact personalization implementation."
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

# Source Based Personalization

Match landing page hero / messaging to the ad source the visitor came from (utm_source, utm_campaign, referrer). Cited as "the simplest high-impact personalization implementation."

## Outputs

- **experience** (experience): Website personalization created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
