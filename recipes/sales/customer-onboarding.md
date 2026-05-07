---
name: Customer Onboarding
description: Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.
intempt:
  id: customer-onboarding
  version: 1.0.0
  slashCommand: /customer-onboarding
  shortDescription: Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.
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
    - customer-onboarding
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
    describe: Configure the new account record with onboarding fields, target go-live date, and CSM assignment.
    produces: account
  - id: create-onboarding-tasks
    describe: Create the onboarding task checklist for the assigned CSM with default due dates.
    produces: task
  - id: schedule-kickoff
    describe: Create kickoff meeting calendar event with the account stakeholders.
    produces: meeting
  - id: build-onboarding-journey
    describe: Build an email journey supporting the user through onboarding milestones with helpful resources at each step.
    produces: journey
  - id: build-onboarding-funnel
    describe: Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live).
    produces: report
---

# Customer Onboarding

Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.

## Outputs

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure the new account record with onboarding fields, target go-live date, and CSM assignment.
2. Create the onboarding task checklist for the assigned CSM with default due dates.
3. Create kickoff meeting calendar event with the account stakeholders.
4. Build an email journey supporting the user through onboarding milestones with helpful resources at each step.
5. Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live).
