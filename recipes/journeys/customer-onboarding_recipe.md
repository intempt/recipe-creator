---
name: customer-onboarding
description: |
  Use when a user mentions "customer onboarding", or asks for related help. Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.
arguments: []
intempt:
  id: customer-onboarding
  version: 1.0.1
  slashCommand: /customer-onboarding
  group: Journeys
  shortDescription: "Create an onboarding task checklist and milestone email journey for a new account."
  availability: coming-soon
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
      title: "Setup Account"
      command: update_account
      produces: account
      bindsAs: account
      description: "Configure the new account record with onboarding fields, target go-live date, and CSM assignment."
      prompt: "Configure the new account record with onboarding fields, target go-live date, and CSM assignment."
    - step: 2
      title: "Create Onboarding Tasks"
      command: create_task
      produces: task
      bindsAs: task
      dependsOn: [account]
      description: "Create the onboarding task checklist for the assigned CSM with default due dates."
      prompt: "Create the onboarding task checklist for the assigned CSM with default due dates."
    - step: 3
      title: "Schedule Kickoff"
      command: book_meeting
      produces: meeting
      bindsAs: meeting
      dependsOn: [account, task]
      description: "Create kickoff meeting calendar event with the account stakeholders."
      prompt: "Create kickoff meeting calendar event with the account stakeholders."
    - step: 4
      title: "Build Onboarding Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [account, task, meeting]
      description: "Build an email journey supporting the user through onboarding milestones with helpful resources at each step."
      prompt: "Build an email journey supporting the user through onboarding milestones with helpful resources at each step."
    - step: 5
      title: "Build Onboarding Funnel"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [account, task, meeting, journey]
      description: "Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live)."
      prompt: "Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live)."
  outputs:
    - { name: account, type: account, cardinality: single, description: "Account produced by this recipe." }
    - { name: task, type: task, cardinality: single, description: "Task produced by this recipe." }
    - { name: meeting, type: meeting, cardinality: single, description: "Meeting produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Customer Onboarding

## Procedure

1. **Setup Account** [`update_account`] — Configure the new account record with onboarding fields, target go-live date, and CSM assignment. → produces: account
2. **Create Onboarding Tasks** [`create_task`] — Create the onboarding task checklist for the assigned CSM with default due dates. → produces: task
3. **Schedule Kickoff** [`book_meeting`] — Create kickoff meeting calendar event with the account stakeholders. → produces: meeting
4. **Build Onboarding Journey** [`create_journey`] — Build an email journey supporting the user through onboarding milestones with helpful resources at each step. → produces: journey
5. **Build Onboarding Funnel** [`build_funnel_report`] — Compose a funnel report tracking onboarding milestone completion (kickoff → setup → first-value → go-live). → produces: report
