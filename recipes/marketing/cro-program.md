---
name: Cro Program
description: Find drop-off, design experiment, ship variants, analyze, kill or promote.
intempt:
  id: cro-program
  version: 1.0.1
  slashCommand: /cro-program
  shortDescription: Find drop-off, design experiment, ship variants, analyze, kill or promote.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: experience-optimizer
    mode:
    - all
    complexity: advanced
    executionMode: live
    tags:
    - cro-program
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: personalization
    type: personalization
    description: Personalization produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: find-dropoff
    describe: Build funnel report identifying highest-impact drop-off step in conversion path.
    produces: report
  - id: design-experiment
    describe: Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions.
    produces: experiment
  - id: build-personalization
    describe: Configure personalization rule that serves variant content to assigned cohort.
    produces: personalization
  - id: build-variants-content
    describe: Generate variant content (copy, layout, CTA changes) per the experiment design.
    produces: content
  - id: build-results-dashboard
    describe: Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance.
    produces: dashboard
---

# Cro Program

Find drop-off, design experiment, ship variants, analyze, kill or promote.

## Outputs

- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **content** (content): Content produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Build funnel report identifying highest-impact drop-off step in conversion path.
2. Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions.
3. Configure personalization rule that serves variant content to assigned cohort.
4. Generate variant content (copy, layout, CTA changes) per the experiment design.
5. Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance.
