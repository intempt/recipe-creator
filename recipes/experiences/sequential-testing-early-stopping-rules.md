---
name: Sequential Testing Early Stopping Rules
description: Methodology playbook for configuring a sequential test that can stop early if results are clear, saving time
  and traffic without inflating false-positive rate.
intempt:
  id: sequential-testing-early-stopping-rules
  version: 1.0.0
  slashCommand: /experiment-methodology-recipe
  shortDescription: Methodology playbook for configuring a sequential test that can stop early if results are clear, saving
    time and traffic without inflating false-positive rate.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - experiences
    agent: experiment-strategist
    mode:
    - all
    complexity: standard
    executionMode: live
    tags:
    - methodology
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: methodology
    type: methodology
    description: Experiment methodology configuration template.
  steps:
  - id: apply-experiment-methodology
    describe: 'Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content
      (Path 2).'
    produces: experience
---

# Sequential Testing Early Stopping Rules

Methodology playbook for configuring a sequential test that can stop early if results are clear, saving time and traffic without inflating false-positive rate.

## Outputs

- **methodology** (methodology): Experiment methodology configuration template.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
