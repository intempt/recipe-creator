---
name: Search Results Ranking Test
description: Optimize product search ranking — relevance vs. popularity-weighted vs. margin-weighted. Server experiment with
  JSON payload controlling search backend.
intempt:
  id: search-results-ranking-test
  version: 1.0.1
  slashCommand: /experiment-recipe
  shortDescription: Optimize product search ranking — relevance vs. popularity-weighted vs. margin-weighted. Server experiment
    with JSON payload controlling search backend.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - ecommerce
    complexity: standard
    executionMode: live
    tags:
    - experiment
    - server
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

# Search Results Ranking Test

Optimize product search ranking — relevance vs. popularity-weighted vs. margin-weighted. Server experiment with JSON payload controlling search backend.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
