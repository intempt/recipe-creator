---
name: Testing Retrospective
description: Quarterly experiment review and roadmap for next testing cycle.
intempt:
  id: testing-retrospective
  version: 1.0.1
  slashCommand: /testing-retrospective
  shortDescription: Quarterly experiment review and roadmap for next testing cycle.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: experience-optimizer
    mode:
    - all
    complexity: standard
    executionMode: live
    tags:
    - testing-retrospective
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: compile-experiment-results
    describe: Compile results across all experiments run in the period — winners, losers, inconclusive.
    produces: experiment
  - id: build-insights-report
    describe: 'Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed,
      best surfaces.'
    produces: report
  - id: build-retrospective-dashboard
    describe: Compose a dashboard summarizing testing cadence, win rate, and revenue impact.
    produces: dashboard
---

# Testing Retrospective

Quarterly experiment review and roadmap for next testing cycle.

## Outputs

- **experiment** (experiment): Experiment produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Compile results across all experiments run in the period — winners, losers, inconclusive.
2. Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces.
3. Compose a dashboard summarizing testing cadence, win rate, and revenue impact.
