---
name: Scheduling Setup
description: Booking types, availability, routing rules, post-booking automation.
intempt:
  id: scheduling-setup
  version: 1.0.0
  slashCommand: /scheduling-setup
  shortDescription: Booking types, availability, routing rules, post-booking automation.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - sales
    agent: scheduling-assistant
    mode:
    - b2b
    complexity: standard
    executionMode: live
    tags:
    - scheduling-setup
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: scheduling_link
    type: scheduling-link
    description: Scheduling Link produced by this recipe.
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
  - id: configure-booking-link
    describe: Configure the booking link with meeting types, durations, availability windows, and host assignment rules.
    produces: scheduling_link
  - id: build-postbooking-workflow
    describe: 'Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record,
      and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather
      than sending the message itself.)'
    produces: workflow
  - id: build-confirmation-journey
    describe: Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking
      workflow.
    produces: journey
  - id: build-booking-dashboard
    describe: Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization.
    produces: dashboard
---

# Scheduling Setup

Booking types, availability, routing rules, post-booking automation.

## Outputs

- **scheduling_link** (scheduling-link): Scheduling Link produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## Steps

1. Configure the booking link with meeting types, durations, availability windows, and host assignment rules.
2. Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.)
3. Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow.
4. Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization.
