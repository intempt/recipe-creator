---
frontmatter_id: sunset-hygiene
slash_command: /sunset-hygiene
description: Gives subscribers who have ignored six months of email one chance to say they still want it, then stops mailing them to protect deliverability.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives subscribers who ignored six months of email one final chance to confirm they still want it, then stops mailing
    non-responders to protect deliverability.
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
  - slot: subscriber_list
    kind: attribute
    meaning: Email subscriber status and suppression list membership
  - slot: email_channel
    kind: destination
    meaning: An email sending destination for marketing messages
    channel: email
  - slot: inactive_subscribers
    kind: segment
    meaning: Subscribers who have not opened or clicked any email within the inactivity window
    creatable: true
    definition: users who have not opened or clicked any email in the last {inactivity_window}
  steps:
  - id: s1
    builds: segment
    uses:
    - email_opened_or_clicked
    - inactivity_window
    instruction: Identify subscribers who have not opened or clicked any email in the last {inactivity_window}. Build this
      as the segment {inactive_subscribers}.
  - id: s2
    builds: email
    uses:
    - s1
    - inactive_subscribers
    instruction: Write a final-attempt email to the subscribers in {inactive_subscribers} asking them to confirm they still
      want to receive email. Include a clear opt-in call to action.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - response_window
    - email_channel
    instruction: Build a two-touch journey that sends the final-attempt email from "Write the last chance email" to the segment
      from "Find who stopped reading", then waits {response_window} for a response.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - response_window
    - subscriber_list
    instruction: Create a workflow that, after the {response_window} window from "Send it, then wait 14 days", automatically
      adds subscribers from "Find who stopped reading" who did not respond to the suppression list.
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    instruction: 'Compose a dashboard tracking deliverability metrics for the sends in "Send it, then wait 14 days": send
      rate, open rate, complaint rate, bounce rate, and inbox placement, scoped to the segment from "Find who stopped reading"
      and the suppressions from "Suppress anyone who ignores it".'
---

# Sunset inactive subscribers

Slash command: /sunset-hygiene

## Step 1: Find who stopped reading

This step builds a segment.
Identify subscribers who have not opened or clicked any email in 180+ days.

## Step 2: Write the last chance email

Generate a final-attempt email asking the user to confirm interest with a clear opt-in CTA. Use the result of "Find who stopped reading".

## Step 3: Send it, then wait 14 days

Build a 2-touch journey sending the final-attempt email and waiting 14 days for response. Use the result of "Find who stopped reading", "Write the last chance email".

## Step 4: Suppress anyone who ignores it

Create a workflow automatically adding non-responders to the suppression list after the 14-day window. Use the result of "Find who stopped reading", "Write the last chance email", "Send it, then wait 14 days".

## Step 5: Watch your deliverability

Compose a dashboard tracking deliverability metrics: send rate, open rate, complaint rate, bounce rate, inbox-placement. Use the result of "Find who stopped reading", "Write the last chance email", "Send it, then wait 14 days", "Suppress anyone who ignores it".
