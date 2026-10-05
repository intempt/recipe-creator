---
id: scheduling-setup
title: Meeting booking and follow-up
slash_command: /scheduling-setup
group: Meetings
owner: intempt
curator: sid
summary: >-
  Creates a booking link, routes requests to the right host, and supports post-booking journeys and workflows.
description: >-
  Configure booking types, availability, host routing, and post-booking journeys or workflows.
version: 2.0.0
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
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A meeting action, from step 1 "Set up the booking link"
    - A new workflow, from step 2 "Trigger follow-up on booking"
    - A new journey, from step 3 "Send the confirmation email"
    - A new dashboard, from step 4 "Track bookings and show rate"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the booking link
    summary: >-
      Meeting types, durations, the hours you are available, and the rules that decide which host gets
      each booking.
    builds: meeting
    description: >-
      Configure the booking link with meeting types, durations, availability windows, and host assignment
      rules.
  - id: s2
    title: Trigger follow-up on booking
    summary: >-
      When a booking completes, start the confirmation email, create the meeting record in your CRM, and
      notify the host.
    builds: workflow
    description: >-
      Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting
      record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow
      triggers the journey rather than sending the message itself.) Use the result of "Set up the booking
      link".
    dependsOn:
      - s1
  - id: s3
    title: Send the confirmation email
    summary: >-
      A single confirmation email to the person who booked, sent when the booking workflow fires.
    builds: journey
    description: >-
      Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by
      the postbooking workflow. Use the result of "Set up the booking link", "Trigger follow-up on booking".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Track bookings and show rate
    summary: >-
      Bookings made, how many showed up, how long people take to book, and how loaded each host is.
    builds: dashboard
    description: >-
      Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization. Use
      the result of "Set up the booking link", "Trigger follow-up on booking", "Send the confirmation
      email".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: scheduling_link
    producedByStep: s1
    type: scheduling_link
    description: Scheduling Link produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Meeting booking and follow-up

Creates a booking link, routes requests to the right host, and supports post-booking journeys and workflows.

## Steps

1. **Set up the booking link** (builds meeting)

   Meeting types, durations, the hours you are available, and the rules that decide which host gets each booking.

2. **Trigger follow-up on booking** (builds workflow)

   When a booking completes, start the confirmation email, create the meeting record in your CRM, and notify the host.

3. **Send the confirmation email** (builds journey)

   A single confirmation email to the person who booked, sent when the booking workflow fires.

4. **Track bookings and show rate** (builds dashboard)

   Bookings made, how many showed up, how long people take to book, and how loaded each host is.

## What you end up with

- **scheduling_link** (scheduling_link): Scheduling Link produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
- **journey** (journey): Journey produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A meeting action, from step 1 "Set up the booking link"
- A new workflow, from step 2 "Trigger follow-up on booking"
- A new journey, from step 3 "Send the confirmation email"
- A new dashboard, from step 4 "Track bookings and show rate"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, meeting, workflow.
