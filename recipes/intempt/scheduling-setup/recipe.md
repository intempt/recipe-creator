---
frontmatter_id: scheduling-setup
slash_command: /scheduling-setup
description: Creates a booking link, routes requests to the right host, and supports post-booking journeys and workflows.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives prospects a booking link that routes them to the right host, then sends a confirmation, logs the meeting
    in the CRM, and tracks bookings and show rate.
  parameters:
  - name: meeting_types
    type: text
    label: Meeting types, durations and availability windows
    default: Meeting types, durations, and availability windows as configured in the booking link
  - name: host_assignment_rule
    type: text
    label: Host assignment rule
    default: Route each booking request to the right host according to the configured assignment rules
  - name: notify_host
    type: boolean
    label: Prepare a notification to the host on booking
    default: true
  requirements:
  - slot: booking_tool
    kind: integration
    meaning: A booking scheduling tool that can host a booking link with meeting types and host routing
    channel: hubspot
  - slot: booking_completed
    kind: event
    meaning: A prospect completed a meeting booking
    properties:
    - name: meeting_type
      type: string
      meaning: The type of meeting booked
      optional: false
    - name: host
      type: string
      meaning: The host assigned to the meeting
      optional: false
    - name: start_time
      type: date
      meaning: When the meeting starts
      optional: false
  - slot: prospect_email
    kind: attribute
    meaning: The prospect's email address used to send the confirmation
  - slot: crm_meeting_record
    kind: destination
    meaning: A CRM where meeting records are created
    channel: hubspot
  - slot: sms_connection
    kind: integration
    channel: sms
    meaning: The SMS sender the text goes out from
  steps:
  - id: s1
    builds: account
    uses:
    - booking_tool
    - meeting_types
    - host_assignment_rule
    instruction: Configure the booking link with the meeting types, durations and availability windows in {meeting_types}.
      Apply the host assignment rule in {host_assignment_rule} so each request is routed to the right host, using {booking_tool}.
  - id: s2
    builds: automation
    uses:
    - booking_completed
    - crm_meeting_record
    - notify_host
    - s1
    instruction: Create a workflow that fires on {booking_completed}. Trigger the confirmation journey for the prospect, create
      a meeting record in {crm_meeting_record} from the booking details including {booking_completed.meeting_type}, {booking_completed.host}
      and {booking_completed.start_time}. If {notify_host} is true, prepare a notification to the host {booking_completed.host}.
      Do not send email or SMS directly from this workflow; it only triggers the journey.
  - id: s3
    builds: automation
    uses:
    - prospect_email
    - s1
    - s2
    instruction: Build a one-touch journey that sends the booking confirmation email to the prospect at {prospect_email} when
      fired by the workflow in "Trigger follow-up on booking". Use the booking details from "Set up the booking link".
  - id: s4
    builds: dashboard
    uses:
    - booking_completed
    - s1
    - s2
    - s3
    instruction: Create a dashboard tracking booking volume, show rate, time to book, and host utilization. Use data from
      "Set up the booking link", "Trigger follow-up on booking" and "Send the confirmation email".
---

# Meeting booking and follow-up

Slash command: /scheduling-setup

## Step 1: Set up the booking link

Configure the booking link with meeting types, durations, availability windows, and host assignment rules.

## Step 2: Trigger follow-up on booking

Create a workflow firing on booking-completed: trigger the confirmation journey, create CRM meeting record, and prep notification to host. (Email/SMS are journey-only per architecture; this workflow triggers the journey rather than sending the message itself.) Use the result of "Set up the booking link".

## Step 3: Send the confirmation email

Build a 1-touch journey that sends the booking confirmation email to the prospect when fired by the postbooking workflow. Use the result of "Set up the booking link", "Trigger follow-up on booking".

## Step 4: Track bookings and show rate

Compose a dashboard tracking booking volume, show-rate, time-to-book, and host utilization. Use the result of "Set up the booking link", "Trigger follow-up on booking", "Send the confirmation email".
