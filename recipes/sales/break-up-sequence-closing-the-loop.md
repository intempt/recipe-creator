---
name: Break Up Sequence Closing The Loop
description: Final 2-email close-out cadence for unresponsive prospects after 14-21 days of outreach. Gives the prospect permission
  to say no. Often the highest-responding email in a sequence.
intempt:
  id: break-up-sequence-closing-the-loop
  version: 1.0.0
  slashCommand: /break-up-sequence-closing-the-loop
  shortDescription: Final 2-email close-out cadence for unresponsive prospects after 14-21 days of outreach. Gives the prospect
    permission to say no. Often the highest-responding email in a sequence.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - lead-qualification-and-outbound
    - break
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: attribute
    type: attribute
    description: Attribute produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: compute-qualification-score
    describe: 'Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Break-up
      sequence — closing the loop.)'
    produces: attribute
  - id: build-routing-workflow
    describe: 'Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context.
      (Tailored for: Break-up sequence — closing the loop.)'
    produces: workflow
  - id: build-nurture-journey
    describe: 'Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Break-up sequence —
      closing the loop.)'
    produces: journey
  - id: build-dashboard
    describe: 'Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity.
      (Tailored for: Break-up sequence — closing the loop.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# Break Up Sequence Closing The Loop

Final 2-email close-out cadence for unresponsive prospects after 14-21 days of outreach. Gives the prospect permission to say no. Often the highest-responding email in a sequence.

## Outputs

- **attribute** (attribute): Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Define a Qualification attribute weighting firmographic fit, intent, and engagement. (Tailored for: Break-up sequence — closing the loop.)
2. Create a workflow assigning hot leads to sales reps (round-robin within team) and creating tasks with context. (Tailored for: Break-up sequence — closing the loop.)
3. Build nurture journeys for warm and cold leads with appropriate cadence. (Tailored for: Break-up sequence — closing the loop.)
4. Compose a dashboard tracking lead volume, score distribution, handoff rate, and conversion to opportunity. (Tailored for: Break-up sequence — closing the loop.)

## Prerequisites

- Integration: **hubspot** (blocking)
