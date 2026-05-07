---
name: Paid User Onboarding Sequence
description: Post-conversion onboarding for newly paid customers — distinct from trial. Focus shifts from 'discover value'
  to 'maximize what you're paying for' and drives advanced feature adoption.
intempt:
  id: paid-user-onboarding-sequence
  version: 1.0.0
  slashCommand: /paid-user-onboarding-sequence
  shortDescription: Post-conversion onboarding for newly paid customers — distinct from trial. Focus shifts from 'discover
    value' to 'maximize what you're paying for' and drives advanced feature adoption.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: revops-automator
    mode:
    - saas
    complexity: advanced
    executionMode: live
    tags:
    - paid
    - trial-and-activation
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
      for: Paid user onboarding sequence.)'
    produces: account
  - id: create-onboarding-tasks
    describe: 'Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: Paid user
      onboarding sequence.)'
    produces: task
  - id: schedule-kickoff
    describe: 'Create kickoff meeting calendar event with the account stakeholders. (Tailored for: Paid user onboarding sequence.)'
    produces: meeting
  - id: build-onboarding-journey
    describe: 'Build an email journey supporting the user through onboarding milestones with helpful resources at each step.
      (Tailored for: Paid user onboarding sequence.)'
    produces: journey
  - id: build-onboarding-funnel
    describe: 'Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live).
      (Tailored for: Paid user onboarding sequence.)'
    produces: report
  prerequisites:
    integrations:
    - value: stripe
      severity: blocking
    - value: segment
      severity: blocking
---

# Paid User Onboarding Sequence

Post-conversion onboarding for newly paid customers — distinct from trial. Focus shifts from 'discover value' to 'maximize what you're paying for' and drives advanced feature adoption.

## Outputs

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Steps

1. Configure the new account record with onboarding fields, target go-live date, and CSM assignment. (Tailored for: Paid user onboarding sequence.)
2. Create the onboarding task checklist for the assigned CSM with default due dates. (Tailored for: Paid user onboarding sequence.)
3. Create kickoff meeting calendar event with the account stakeholders. (Tailored for: Paid user onboarding sequence.)
4. Build an email journey supporting the user through onboarding milestones with helpful resources at each step. (Tailored for: Paid user onboarding sequence.)
5. Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live). (Tailored for: Paid user onboarding sequence.)

## Prerequisites

- Integration: **stripe** (blocking)
- Integration: **segment** (blocking)
