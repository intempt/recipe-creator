---
name: Meeting Intelligence
description: Recording, transcription, automation, post-meeting tasks and CRM updates.
intempt:
  id: meeting-intelligence
  version: 1.0.0
  slashCommand: /meeting-intelligence
  shortDescription: Recording, transcription, automation, post-meeting tasks and CRM updates.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: meeting-notetaker
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - meeting-intelligence
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: meeting
    type: meeting
    description: Meeting produced by this recipe.
  - name: task
    type: task
    description: Task produced by this recipe.
  - name: deal
    type: deal
    description: Deal produced by this recipe.
  - name: workflow
    type: workflow
    description: Workflow produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  steps:
  - id: capture-meeting
    describe: Record and transcribe the meeting; produce a structured summary with key points and decisions.
    produces: meeting
  - id: extract-tasks
    describe: Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates.
    produces: task
  - id: update-deal-record
    describe: Update the linked deal with meeting notes, sentiment, and stage-progression signals.
    produces: deal
  - id: build-followup-workflow
    describe: Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and
      notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending
      the message itself.)
    produces: workflow
  - id: build-followup-journey
    describe: Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when
      fired by the followup workflow.
    produces: journey
  - id: build-meeting-dashboard
    describe: Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence.
    produces: dashboard
---

# Meeting Intelligence

Recording, transcription, automation, post-meeting tasks and CRM updates.

## Outputs

- **meeting** (meeting): Meeting produced by this recipe.
- **task** (task): Task produced by this recipe.
- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## Steps

1. Record and transcribe the meeting; produce a structured summary with key points and decisions.
2. Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates.
3. Update the linked deal with meeting notes, sentiment, and stage-progression signals.
4. Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending the message itself.)
5. Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when fired by the followup workflow.
6. Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence.
