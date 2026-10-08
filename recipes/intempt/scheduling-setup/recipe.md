---
description: Creates a booking link, routes requests to the right host, and supports post-booking journeys and workflows.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
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
