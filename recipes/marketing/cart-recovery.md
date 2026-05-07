---
name: Cart Recovery
description: Recover abandoned carts with a 3-touch sequence — segment, content, journey, A/B variants, dashboard, alert workflow.
intempt:
  id: cart-recovery
  version: 1.0.0
  slashCommand: /cart-recovery
  shortDescription: Recover abandoned carts with a 3-touch sequence — segment, content, journey, A/B variants, dashboard,
    alert workflow.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - ecommerce
    complexity: advanced
    executionMode: live
    tags:
    - cart-recovery
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency
      + social proof. Touch 3: final reminder optionally with discount.'
    produces: content
  - id: build-journey
    describe: Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr,
      and 72hr after abandonment.
    produces: journey
  - id: build-experiment
    describe: Add A/B variants on subject lines and incentive levels for the recovery journey.
    produces: experiment
  - id: build-dashboard
    describe: Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey.
    produces: dashboard
  - id: build-alert-workflow
    describe: Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window.
    produces: workflow
---

# Cart Recovery

Recover abandoned carts with a 3-touch sequence — segment, content, journey, A/B variants, dashboard, alert workflow.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Generate 3-touch cart-recovery email content using brand voice. Touch 1: gentle reminder. Touch 2: urgency + social proof. Touch 3: final reminder optionally with discount.
2. Build a 3-touch journey wired to the cart-abandoners segment, sending the cart-recovery emails at 1hr, 24hr, and 72hr after abandonment.
3. Add A/B variants on subject lines and incentive levels for the recovery journey.
4. Compose a dashboard showing recovery rate, revenue recovered, and time-to-recover metrics for the journey.
5. Create a workflow that alerts the team if recovery rate drops below 15% over a 7-day window.
