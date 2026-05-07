---
name: Experiment Ship Decision Framework
description: Methodology playbook for evaluating whether an experiment result is ready to ship — statistical significance,
  guardrail metrics, sample-ratio mismatch checks.
intempt:
  id: experiment-ship-decision-framework
  version: 1.0.0
  slashCommand: /experiment-methodology-recipe
  shortDescription: Methodology playbook for evaluating whether an experiment result is ready to ship — statistical significance,
    guardrail metrics, sample-ratio mismatch checks.
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

# Experiment Ship Decision Framework

Methodology playbook for evaluating whether an experiment result is ready to ship — statistical significance, guardrail metrics, sample-ratio mismatch checks.

## Outputs

- **methodology** (methodology): Experiment methodology configuration template.

## Steps

1. Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2).
