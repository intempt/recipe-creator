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
  title: "Meeting booking and follow-up"
  shortDescription: "Sets up your booking link, routes each request to the right host, confirms it by email, and tracks how many of the people who booked actually show up."
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
      title: "Set up the booking link"
      command: get_booking_link
      produces: scheduling_link
      bindsAs: scheduling_link
      description: "Meeting types, durations, the hours you are available, and the rules that decide which host gets each booking."
      prompt: "Configure the booking link with meeting types, durations, availability windows, and host assignment rules."
    - step: 2
      title: "Trigger follow-up on booking"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [scheduling_link]
      description: "When a booking completes, start the confirmation email, create the meeting record in your CRM, and notify the host."
      prompt: "Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.)"
    - step: 3
      title: "Send the confirmation email"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [scheduling_link, workflow]
      description: "A single confirmation email to the person who booked, sent when the booking workflow fires."
      prompt: "Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow."
    - step: 4
      title: "Track bookings and show rate"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [scheduling_link, workflow, journey]
      description: "Bookings made, how many showed up, how long people take to book, and how loaded each host is."
      prompt: "Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization."
  outputs:
    - { name: scheduling_link, type: scheduling_link, cardinality: single, description: "Scheduling Link produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Meeting booking and follow-up

Sets up your booking link, routes each request to the right host, confirms it by email, and tracks how many of the people who booked actually show up.

## What it does

1. **Set up the booking link** (`get_booking_link`)

   Meeting types, durations, the hours you are available, and the rules that decide which host gets each booking.

2. **Trigger follow-up on booking** (`create_workflow`)

   When a booking completes, start the confirmation email, create the meeting record in your CRM, and notify the host.

3. **Send the confirmation email** (`create_journey`)

   A single confirmation email to the person who booked, sent when the booking workflow fires.

4. **Track bookings and show rate** (`create_dashboard`)

   Bookings made, how many showed up, how long people take to book, and how loaded each host is.

## What you end up with

- **scheduling_link** (scheduling_link): Scheduling Link produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
