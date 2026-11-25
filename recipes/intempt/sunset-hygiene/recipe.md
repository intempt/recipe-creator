---
frontmatter_id: sunset-hygiene
slash_command: /sunset-hygiene
description: Gives subscribers who have ignored six months of email one chance to say they still want it, then lists the ones
  who stayed silent so you stop mailing them and protect deliverability.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends subscribers who ignored six months of email one last-chance email, then builds the segment of non-responders
    to leave out of every send.
  parameters:
  - name: inactivity_window
    type: duration
    label: Inactivity window (no opens or clicks)
    default: 180 d
    required: false
  - name: response_window
    type: duration
    label: Response window after the final email
    default: 14 d
    required: false
  requirements:
  - slot: email_opened_or_clicked
    kind: event
    meaning: A subscriber opened or clicked an email
  - slot: email_received
    kind: event
    meaning: A subscriber was sent a marketing email
  - slot: subscribed
    kind: attribute
    meaning: True when the user is subscribed to marketing email
  steps:
  - id: s1
    builds: segment
    uses:
    - email_opened_or_clicked
    - email_received
    - subscribed
    - inactivity_window
    instruction: Build a new segment of users named "Inactive subscribers". A user is in it when their {subscribed} is true,
      they did {email_received} 3 or more times in the last {inactivity_window}, and they did not do {email_opened_or_clicked}
      in the last {inactivity_window}.
  - id: s2
    builds: email
    instruction: Write a short final-attempt email for subscribers who have not opened our email in six months. It asks whether
      they still want to hear from us, has one clear 'Yes, keep me subscribed' button, and says that if we do not hear back
      we will stop emailing them.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    dependsOn:
    - s1
    - s2
    instruction: Build an automation triggered when a user enters the segment from "Find who stopped reading". It sends the
      email from "Write the last chance email" once. A user gets it at most once every 180 days.
  - id: s4
    builds: segment
    uses:
    - s1
    - s3
    - email_opened_or_clicked
    - response_window
    dependsOn:
    - s1
    - s3
    instruction: 'Build a new segment of users named "Sunset: stop mailing". A user is in it when they are in the segment
      from "Find who stopped reading", were sent the email by "Send it once, then wait" more than {response_window} ago, and
      did not do {email_opened_or_clicked} since that email.'
---

# Sunset inactive subscribers

Slash command: /sunset-hygiene

## Step 1: Find who stopped reading

Build a new segment of users named "Inactive subscribers". A user is in it when their subscribed is true, they did email received 3 or more times in the last 180 d, and they did not do email opened or clicked in the last 180 d.

## Step 2: Write the last chance email

Write a short final-attempt email for subscribers who have not opened our email in six months. It asks whether they still want to hear from us, has one clear 'Yes, keep me subscribed' button, and says that if we do not hear back we will stop emailing them.

## Step 3: Send it once, then wait

Build an automation triggered when a user enters the segment from "Find who stopped reading". It sends the email from "Write the last chance email" once. A user gets it at most once every 180 days.

## Step 4: List who ignored it

Build a new segment of users named "Sunset: stop mailing". A user is in it when they are in the segment from "Find who stopped reading", were sent the email by "Send it once, then wait" more than 14 d ago, and did not do email opened or clicked since that email.
