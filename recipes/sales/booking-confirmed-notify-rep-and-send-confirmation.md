---
name: Booking Confirmed Notify Rep And Send Confirmation
description: When a prospect books a meeting, notify the assigned rep and send a confirmation to the prospect.
intempt:
  id: booking-confirmed-notify-rep-and-send-confirmation
  version: 1.0.0
  slashCommand: /booking-confirmed-notify-rep-and-send-confirmation
  shortDescription: When a prospect books a meeting, notify the assigned rep and send a confirmation to the prospect.
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
    - booking-flow-automation
    - booking
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
    describe: 'Configure the booking link with meeting types, durations, availability windows, and host assignment rules.
      (Tailored for: Booking confirmed — notify rep and send confirmation.)'
    produces: scheduling_link
  - id: build-postbooking-workflow
    describe: 'Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record,
      and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather
      than sending the message itself.) (Tailored for: Booking confirmed — notify rep and send confirmation.)'
    produces: workflow
  - id: build-confirmation-journey
    describe: Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking
      workflow.
    produces: journey
  - id: build-booking-dashboard
    describe: 'Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization. (Tailored for:
      Booking confirmed — notify rep and send confirmation.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: slack
      severity: blocking
---

# Booking Confirmed Notify Rep And Send Confirmation

When a prospect books a meeting, notify the assigned rep and send a confirmation to the prospect.

## Outputs

- **scheduling_link** (scheduling-link): Scheduling Link produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## Steps

1. Configure the booking link with meeting types, durations, availability windows, and host assignment rules. (Tailored for: Booking confirmed — notify rep and send confirmation.)
2. Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.) (Tailored for: Booking confirmed — notify rep and send confirmation.)
3. Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow.
4. Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization. (Tailored for: Booking confirmed — notify rep and send confirmation.)

## Prerequisites

- Integration: **slack** (blocking)
