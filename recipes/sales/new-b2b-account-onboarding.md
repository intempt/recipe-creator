---
name: New B2B Account Onboarding
description: Multi-stakeholder B2B onboarding that accounts for buying committees of 6-13+ people. Routes role-specific content
  to each contact type and schedules CS kickoff.
intempt:
  id: new-b2b-account-onboarding
  version: 1.0.0
  slashCommand: /new-b2b-account-onboarding
  shortDescription: Multi-stakeholder B2B onboarding that accounts for buying committees of 6-13+ people. Routes role-specific
    content to each contact type and schedules CS kickoff.
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
    - customer-success-and-renewal
    - new
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
      for: New B2B account onboarding.)'
    produces: account
  - id: create-onboarding-tasks
    describe: 'Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: New B2B account
      onboarding.)'
    produces: task
  - id: schedule-kickoff
    describe: 'Create kickoff meeting calendar event with the account stakeholders. (Tailored for: New B2B account onboarding.)'
    produces: meeting
  - id: build-onboarding-journey
    describe: 'Build an email journey supporting the user through onboarding milestones with helpful resources at each step.
      (Tailored for: New B2B account onboarding.)'
    produces: journey
  - id: build-onboarding-funnel
    describe: 'Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live).
      (Tailored for: New B2B account onboarding.)'
    produces: report
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: salesforce
      severity: blocking
---

# New B2B Account Onboarding

Multi-stakeholder B2B onboarding that accounts for buying committees of 6-13+ people. Routes role-specific content to each contact type and schedules CS kickoff.

## Outputs

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure the new account record with onboarding fields, target go-live date, and CSM assignment. (Tailored for: New B2B account onboarding.)
2. Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: New B2B account onboarding.)
3. Create kickoff meeting calendar event with the account stakeholders. (Tailored for: New B2B account onboarding.)
4. Build an email journey supporting the user through onboarding milestones with helpful resources at each step. (Tailored for: New B2B account onboarding.)
5. Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live). (Tailored for: New B2B account onboarding.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **salesforce** (blocking)
