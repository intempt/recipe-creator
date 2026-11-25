---
frontmatter_id: cold-outbound
slash_command: /cold-outbound
description: Builds a target list from your ICP, sends a two-touch cold email sequence with a booking link that stops on reply
  or booking, and emails a weekly digest of replies and meetings.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds an ICP prospect list, runs a two-touch cold email sequence with your booking link, and emails a weekly digest
    of replies and meetings booked.
  parameters:
  - name: target_industries
    type: string
    label: Industries that fit your ideal customer (comma separated)
    required: true
  - name: min_employees
    type: number
    label: Smallest company size that fits (employees)
    default: 50
    required: false
  - name: max_employees
    type: number
    label: Largest company size that fits (employees)
    default: 1000
    required: false
  - name: cadence_gap
    type: duration
    label: Gap between touches
    default: 3 d
    required: false
  - name: booking_link
    type: string
    label: Link where prospects book a meeting
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: company_industry
    kind: attribute
    meaning: The industry of the prospect's company
  - slot: company_employees
    kind: attribute
    meaning: The number of employees at the prospect's company
  - slot: outreach_sender
    kind: destination
    meaning: An email sending channel used to deliver outbound sequence messages
    channel: email
  - slot: outbound_reply
    kind: event
    meaning: A prospect replied to an outbound email
    properties:
    - name: prospect_id
      type: string
      meaning: Identifier of the replying prospect
      optional: false
  - slot: meeting_booked
    kind: event
    meaning: A prospect booked a meeting through the booking link
    properties:
    - name: prospect_id
      type: string
      meaning: Identifier of the prospect who booked
      optional: false
  steps:
  - id: s1
    builds: segment
    uses:
    - company_industry
    - company_employees
    - target_industries
    - min_employees
    - max_employees
    - outbound_reply
    - meeting_booked
    instruction: 'Build a new segment of users named "Cold Outbound Prospects". A user is in it when all of these are true:
      their {company_industry} is one of {target_industries}; their {company_employees} is between {min_employees} and {max_employees};
      they never did {outbound_reply}; they never did {meeting_booked}.'
  - id: s2
    builds: email
    uses:
    - booking_link
    instruction: Write a short plain cold email to a prospect at a company that fits our ideal customer. It names one problem
      companies in their industry have, says in one sentence how we solve it, and asks for a 30-minute call through {booking_link}.
      No attachments, no prices.
  - id: s3
    builds: email
    uses:
    - booking_link
    instruction: Write a short plain break-up email to a prospect who did not reply to our first cold email. It says this
      is the last note, restates the one problem we solve in one sentence, and leaves {booking_link} in case the timing changes.
      No prices.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - outreach_sender
    - cadence_gap
    - outbound_reply
    - meeting_booked
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation triggered when a user enters the segment from "Build the target list". It sends the email
      from "Write the first touch" through {outreach_sender}. Then it waits {cadence_gap}; if the user did not do {outbound_reply}
      or {meeting_booked} in that time, it sends the email from "Write the break-up email" through {outreach_sender}. It stops
      as soon as the user does {outbound_reply} or {meeting_booked}.
  - id: s5
    builds: automation
    uses:
    - s1
    - outbound_reply
    - meeting_booked
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered
      the segment from "Build the target list" in the last 7 days and the 28 days before, and writes these figures for both
      windows: prospects entered; share who did {outbound_reply}; share who did {meeting_booked}. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Cold outbound sequence

Slash command: /cold-outbound

## Step 1: Build the target list

Build a new segment of users named "Cold Outbound Prospects". A user is in it when all of these are true: their company industry is one of the industries that fit your ideal customer (comma separated); their company employees is between 50 and 1000; they never did outbound reply; they never did meeting booked.

## Step 2: Write the first touch

Write a short plain cold email to a prospect at a company that fits our ideal customer. It names one problem companies in their industry have, says in one sentence how we solve it, and asks for a 30-minute call through the link where prospects book a meeting. No attachments, no prices.

## Step 3: Write the break-up email

Write a short plain break-up email to a prospect who did not reply to our first cold email. It says this is the last note, restates the one problem we solve in one sentence, and leaves the link where prospects book a meeting in case the timing changes. No prices.

## Step 4: Run the touches, then break off

Build an automation triggered when a user enters the segment from "Build the target list". It sends the email from "Write the first touch" through outreach sender. Then it waits 3 d; if the user did not do outbound reply or meeting booked in that time, it sends the email from "Write the break-up email" through outreach sender. It stops as soon as the user does outbound reply or meeting booked.

## Step 5: Email the weekly outbound digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered the segment from "Build the target list" in the last 7 days and the 28 days before, and writes these figures for both windows: prospects entered; share who did outbound reply; share who did meeting booked. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
