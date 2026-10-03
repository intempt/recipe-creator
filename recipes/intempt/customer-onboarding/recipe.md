---
id: customer-onboarding
title: Customer onboarding
slash_command: /customer-onboarding
group: Journeys
owner: intempt
summary: Sets up a new account, gives the CSM a dated checklist, books the kickoff, and walks the customer
  through to go live.
description: >-
  Account setup, kickoff tasks, calendar coordination, onboarding journey, completion funnel.
version: 2.0.0
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
steps:
  - id: s1
    title: Set up the account record
    summary: >-
      Onboarding fields, the target go live date, and the CSM who owns it.
    builds: account
    description: >-
      Configure the new account record with onboarding fields, target go-live date, and CSM assignment.
  - id: s2
    title: Give the CSM a checklist
    summary: >-
      The onboarding tasks, each with a default due date.
    builds: task
    description: >-
      Create the onboarding task checklist for the assigned CSM with default due dates. Use the result
      of "Set up the account record".
    dependsOn:
      - s1
  - id: s3
    title: Book the kickoff call
    summary: >-
      A calendar invite with the stakeholders at the account.
    builds: meeting
    description: >-
      Create kickoff meeting calendar event with the account stakeholders. Use the result of "Set up the
      account record", "Give the CSM a checklist".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Email through each milestone
    summary: >-
      Emails that carry the customer from step to step, with the resources they need at each one.
    builds: journey
    description: >-
      Build an email journey supporting the user through onboarding milestones with helpful resources
      at each step. Use the result of "Set up the account record", "Give the CSM a checklist", "Book the
      kickoff call".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Track progress to go live
    summary: >-
      A funnel from kickoff through setup and first value to go live.
    builds: report
    description: >-
      Compose a funnel report tracking onboarding milestone completion (kickoff to setup to first-value
      to go-live). Use the result of "Set up the account record", "Give the CSM a checklist", "Book the
      kickoff call", "Email through each milestone".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: account
    producedByStep: s1
    type: account
    description: Account produced by this recipe.
  - key: task
    producedByStep: s2
    type: task
    description: Task produced by this recipe.
  - key: meeting
    producedByStep: s3
    type: meeting
    description: Meeting produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: report
    producedByStep: s5
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Customer onboarding

Sets up a new account, gives the CSM a dated checklist, books the kickoff, and walks the customer through to go live.

## Steps

1. **Set up the account record** (builds account)

   Onboarding fields, the target go live date, and the CSM who owns it.

2. **Give the CSM a checklist** (builds task)

   The onboarding tasks, each with a default due date.

3. **Book the kickoff call** (builds meeting)

   A calendar invite with the stakeholders at the account.

4. **Email through each milestone** (builds journey)

   Emails that carry the customer from step to step, with the resources they need at each one.

5. **Track progress to go live** (builds report)

   A funnel from kickoff through setup and first value to go live.

## What you end up with

- **account** (account): Account produced by this recipe.
- **task** (task): Task produced by this recipe.
- **meeting** (meeting): Meeting produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build account, journey, meeting, report, task.
