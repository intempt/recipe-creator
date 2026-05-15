---
name: scheduling-setup
description: |
  Use when a user mentions "scheduling & booking setup", or asks for related help. Booking types, availability, routing rules, post-booking automation.
arguments: []
intempt:
  id: scheduling-setup
  version: 1.0.1
  slashCommand: /scheduling-setup
  group: Meetings
  shortDescription: "Booking types, availability, routing rules, post-booking automation."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: scheduling-assistant
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [scheduling-setup]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - get_booking_link
    - create_workflow
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Configure Booking Link"
      command: get_booking_link
      produces: scheduling_link
      bindsAs: scheduling_link
      description: "Configure the booking link with meeting types, durations, availability windows, and host assignment rules."
      prompt: "Configure the booking link with meeting types, durations, availability windows, and host assignment rules."
    - step: 2
      title: "Build Postbooking Workflow"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [scheduling_link]
      description: "Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.)"
      prompt: "Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.)"
    - step: 3
      title: "Build Confirmation Journey"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [scheduling_link, workflow]
      description: "Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow."
      prompt: "Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow."
    - step: 4
      title: "Build Booking Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [scheduling_link, workflow, journey]
      description: "Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization."
      prompt: "Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization."
  outputs:
    - { name: scheduling_link, type: scheduling_link, cardinality: single, description: "Scheduling Link produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
---

# Scheduling & Booking Setup

## Procedure

1. **Configure Booking Link** [`get_booking_link`] — Configure the booking link with meeting types, durations, availability windows, and host assignment rules. → produces: scheduling_link
2. **Build Postbooking Workflow** [`create_workflow`] — Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.) → produces: workflow
3. **Build Confirmation Journey** [`create_journey`] — Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow. → produces: journey
4. **Build Booking Dashboard** [`create_dashboard`] — Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization. → produces: dashboard
