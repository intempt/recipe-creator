---
name: Deal Won Customer Onboarding Kickoff
description: The moment a deal closes won, fire off CSM task creation, welcome email, kickoff scheduling, account stage update,
  and internal celebration — so onboarding starts immediately, not after manual...
intempt:
  id: deal-won-customer-onboarding-kickoff
  version: 1.0.0
  slashCommand: /deal-won-customer-onboarding-kickoff
  shortDescription: The moment a deal closes won, fire off CSM task creation, welcome email, kickoff scheduling, account stage
    update, and internal celebration — so onboarding starts immediately, not after manual...
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
    - deal
    - sales-automation
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: account
    type: account
    description: Account produced by this recipe.
  - name: task
    type: task
    description: Task produced by this recipe.
  - name: meeting
    type: meeting
    description: Meeting produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: report
    type: report
    description: Report produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  steps:
  - id: setup-account
    describe: 'Configure the new account record with onboarding fields, target go-live date, and CSM assignment. (Tailored
      for: Deal won — customer onboarding kickoff.)'
    produces: account
  - id: create-onboarding-tasks
    describe: 'Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: Deal won —
      customer onboarding kickoff.)'
    produces: task
  - id: schedule-kickoff
    describe: 'Create kickoff meeting calendar event with the account stakeholders. (Tailored for: Deal won — customer onboarding
      kickoff.)'
    produces: meeting
  - id: build-onboarding-journey
    describe: 'Build an email journey supporting the user through onboarding milestones with helpful resources at each step.
      (Tailored for: Deal won — customer onboarding kickoff.)'
    produces: journey
  - id: build-onboarding-funnel
    describe: 'Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live).
      (Tailored for: Deal won — customer onboarding kickoff.)'
    produces: report
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: slack
      severity: blocking
---

# Deal Won Customer Onboarding Kickoff

The moment a deal closes won, fire off CSM task creation, welcome email, kickoff scheduling, account stage update, and internal celebration — so onboarding starts immediately, not after manual...

## Outputs

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure the new account record with onboarding fields, target go-live date, and CSM assignment. (Tailored for: Deal won — customer onboarding kickoff.)
2. Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: Deal won — customer onboarding kickoff.)
3. Create kickoff meeting calendar event with the account stakeholders. (Tailored for: Deal won — customer onboarding kickoff.)
4. Build an email journey supporting the user through onboarding milestones with helpful resources at each step. (Tailored for: Deal won — customer onboarding kickoff.)
5. Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live). (Tailored for: Deal won — customer onboarding kickoff.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **slack** (blocking)
