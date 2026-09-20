---
name: customer-onboarding
description: |
  Use when a user mentions "customer onboarding", or asks for related help. Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.
arguments: []
intempt:
  id: customer-onboarding
  title: "Customer onboarding"
  version: 1.0.1
  slashCommand: /customer-onboarding
  group: Journeys
  shortDescription: "Sets up a new account, gives the CSM a dated checklist, books the kickoff, and walks the customer through to go live."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [customer-onboarding]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - update_account
    - create_task
    - book_meeting
    - create_journey
    - build_funnel_report
  procedure:
    - step: 1
      title: "Set up the account record"
      command: update_account
      produces: account
      bindsAs: account
      description: "Onboarding fields, the target go live date, and the CSM who owns it."
      prompt: "Configure the new account record with onboarding fields, target go-live date, and CSM assignment."
    - step: 2
      title: "Give the CSM a checklist"
      command: create_task
      produces: task
      bindsAs: task
      dependsOn: [account]
      description: "The onboarding tasks, each with a default due date."
      prompt: "Create the onboarding task checklist for the assigned CSM with default due dates."
    - step: 3
      title: "Book the kickoff call"
      command: book_meeting
      produces: meeting
      bindsAs: meeting
      dependsOn: [account, task]
      description: "A calendar invite with the stakeholders at the account."
      prompt: "Create kickoff meeting calendar event with the account stakeholders."
    - step: 4
      title: "Email through each milestone"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [account, task, meeting]
      description: "Emails that carry the customer from step to step, with the resources they need at each one."
      prompt: "Build an email journey supporting the user through onboarding milestones with helpful resources at each step."
    - step: 5
      title: "Track progress to go live"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [account, task, meeting, journey]
      description: "A funnel from kickoff through setup and first value to go live."
      prompt: "Compose a funnel report tracking onboarding milestone completion (kickoff to setup to first-value to go-live)."
  outputs:
    - { name: account, type: account, cardinality: single, description: "Account produced by this recipe." }
    - { name: task, type: task, cardinality: single, description: "Task produced by this recipe." }
    - { name: meeting, type: meeting, cardinality: single, description: "Meeting produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Customer onboarding

Sets up a new account, gives the CSM a dated checklist, books the kickoff, and walks the customer through to go live.

## What it does

1. **Set up the account record** (`update_account`)

   Onboarding fields, the target go live date, and the CSM who owns it.

2. **Give the CSM a checklist** (`create_task`)

   The onboarding tasks, each with a default due date.

3. **Book the kickoff call** (`book_meeting`)

   A calendar invite with the stakeholders at the account.

4. **Email through each milestone** (`create_journey`)

   Emails that carry the customer from step to step, with the resources they need at each one.

5. **Track progress to go live** (`build_funnel_report`)

   A funnel from kickoff through setup and first value to go live.

## What you end up with

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
