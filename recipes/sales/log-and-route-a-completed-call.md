---
name: Log And Route A Completed Call
description: Automatically log call outcomes, update CRM records, and create follow-up tasks after a call is completed.
intempt:
  id: log-and-route-a-completed-call
  version: 1.0.0
  slashCommand: /log-and-route-a-completed-call
  shortDescription: Automatically log call outcomes, update CRM records, and create follow-up tasks after a call is completed.
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
    - sales-call-workflows
    - log
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
    describe: 'Record and transcribe the meeting; produce a structured summary with key points and decisions. (Tailored for:
      Log and route a completed call.)'
    produces: meeting
  - id: extract-tasks
    describe: 'Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates.
      (Tailored for: Log and route a completed call.)'
    produces: task
  - id: update-deal-record
    describe: 'Update the linked deal with meeting notes, sentiment, and stage-progression signals. (Tailored for: Log and
      route a completed call.)'
    produces: deal
  - id: build-followup-workflow
    describe: 'Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and
      notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending
      the message itself.) (Tailored for: Log and route a completed call.)'
    produces: workflow
  - id: build-followup-journey
    describe: Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when
      fired by the followup workflow.
    produces: journey
  - id: build-meeting-dashboard
    describe: 'Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence. (Tailored
      for: Log and route a completed call.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
    - value: slack
      severity: blocking
---

# Log And Route A Completed Call

Automatically log call outcomes, update CRM records, and create follow-up tasks after a call is completed.

## Outputs

- **meeting** (meeting): Meeting produced by this recipe.
- **task** (task): Task produced by this recipe.
- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## Steps

1. Record and transcribe the meeting; produce a structured summary with key points and decisions. (Tailored for: Log and route a completed call.)
2. Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates. (Tailored for: Log and route a completed call.)
3. Update the linked deal with meeting notes, sentiment, and stage-progression signals. (Tailored for: Log and route a completed call.)
4. Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending the message itself.) (Tailored for: Log and route a completed call.)
5. Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when fired by the followup workflow.
6. Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence. (Tailored for: Log and route a completed call.)

## Prerequisites

- Integration: **hubspot** (blocking)
- Integration: **slack** (blocking)
