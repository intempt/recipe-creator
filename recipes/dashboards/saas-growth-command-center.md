---
name: Saas Growth Command Center
description: 'Founder-level SaaS growth view: WAU, MRR, trial conversion, retention, activation, and feature adoption on one
  canvas.'
intempt:
  id: saas-growth-command-center
  version: 1.0.0
  slashCommand: /saas-growth-command-center
  shortDescription: 'Founder-level SaaS growth view: WAU, MRR, trial conversion, retention, activation, and feature adoption
    on one canvas.'
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - saas
    complexity: standard
    executionMode: live
    tags:
    - dashboard
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: dashboard
    type: dashboard
    description: Dash board (composition canvas) produced by this recipe.
  steps:
  - id: build-dashboard
    describe: Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes
      per the spec below.
    produces: dashboard
---

# Saas Growth Command Center

Founder-level SaaS growth view: WAU, MRR, trial conversion, retention, activation, and feature adoption on one canvas.

## Outputs

- **dashboard** (dashboard): Dash board (composition canvas) produced by this recipe.

## Steps

1. Create a Dash board (composition canvas) and populate it with linked cards sourced from existing report recipes per the spec below.
