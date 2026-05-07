---
name: Form Length Test
description: Test 3-field vs. 5-field vs. 7-field demo-request form. Universal CRO test; 10-15% conversion drop per added
  field cited.
intempt:
  id: form-length-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  shortDescription: Test 3-field vs. 5-field vs. 7-field demo-request form. Universal CRO test; 10-15% conversion drop per
    added field cited.
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

# Form Length Test

Test 3-field vs. 5-field vs. 7-field demo-request form. Universal CRO test; 10-15% conversion drop per added field cited.

## Outputs

- **experience** (experience): Website experiment created on /experiences.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
