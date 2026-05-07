---
name: Meeting Scheduled Pre Meeting Prep Brief
description: When a meeting is scheduled, automatically prepare a research brief for the rep.
intempt:
  id: meeting-scheduled-pre-meeting-prep-brief
  version: 1.0.0
  slashCommand: /meeting-scheduled-pre-meeting-prep-brief
  shortDescription: When a meeting is scheduled, automatically prepare a research brief for the rep.
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
    - ai-powered-meeting-workflows
    - meeting
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
      Meeting scheduled — pre-meeting prep brief.)'
    produces: meeting
  - id: extract-tasks
    describe: 'Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates.
      (Tailored for: Meeting scheduled — pre-meeting prep brief.)'
    produces: task
  - id: update-deal-record
    describe: 'Update the linked deal with meeting notes, sentiment, and stage-progression signals. (Tailored for: Meeting
      scheduled — pre-meeting prep brief.)'
    produces: deal
  - id: build-followup-workflow
    describe: 'Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and
      notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending
      the message itself.) (Tailored for: Meeting scheduled — pre-meeting prep brief.)'
    produces: workflow
  - id: build-followup-journey
    describe: Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when
      fired by the followup workflow.
    produces: journey
  - id: build-meeting-dashboard
    describe: 'Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence. (Tailored
      for: Meeting scheduled — pre-meeting prep brief.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Meeting Scheduled Pre Meeting Prep Brief

When a meeting is scheduled, automatically prepare a research brief for the rep.

## Outputs

- **meeting** (meeting): Meeting produced by this recipe.
- **task** (task): Task produced by this recipe.
- **deal** (deal): Deal produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## Steps

1. Record and transcribe the meeting; produce a structured summary with key points and decisions. (Tailored for: Meeting scheduled — pre-meeting prep brief.)
2. Extract action items from the transcript and create CRM tasks assigned to the appropriate owners with due dates. (Tailored for: Meeting scheduled — pre-meeting prep brief.)
3. Update the linked deal with meeting notes, sentiment, and stage-progression signals. (Tailored for: Meeting scheduled — pre-meeting prep brief.)
4. Create a workflow firing on meeting-completed that triggers the followup journey, updates the CRM deal, and notifies the deal owner. (Email is journey-only per architecture; this workflow triggers the journey rather than sending the message itself.) (Tailored for: Meeting scheduled — pre-meeting prep brief.)
5. Build a 1-touch journey that sends a structured follow-up email to attendees with summary and action items when fired by the followup workflow.
6. Compose a dashboard tracking meeting volume by deal stage, talk-listen ratio, and follow-up cadence. (Tailored for: Meeting scheduled — pre-meeting prep brief.)

## Prerequisites

- Integration: **slack** (blocking)
