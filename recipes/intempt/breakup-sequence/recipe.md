---
frontmatter_id: breakup-sequence
slash_command: /breakup-sequence
description: Finds prospects who got repeated outreach and never engaged, sends them one honest last email, alerts the owner
  when they reply, and emails a weekly digest of what the last email pulls.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Sends one honest last email to prospects who never replied, alerts the team on replies, and emails a weekly digest
    of replies and meetings it brings back.
  parameters:
  - name: outreach_threshold
    type: number
    label: Minimum outreach attempts in the lookback window
    default: 5
    required: false
  - name: lookback_window
    type: duration
    label: Lookback window for outreach attempts
    default: 60 d
    required: false
  - name: topic
    type: string
    label: What you have been reaching out about
    required: true
  - name: calendar_link
    type: string
    label: Calendar link for reconnecting
    required: true
  - name: email_subject
    type: string
    label: Email subject line
    default: Closing the loop
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get reply alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: prospect_outreach_event
    kind: event
    meaning: A prospect received an outreach attempt by email or call
  - slot: prospect_engagement_event
    kind: event
    meaning: A prospect opened an email, replied, or had a meeting scheduled
  - slot: open_deal
    kind: attribute
    meaning: True when the prospect's account has an open deal
  - slot: target_account
    kind: attribute
    meaning: True when the prospect's account is on the target-account list
    optional: true
  - slot: email_reply_event
    kind: event
    meaning: A prospect replied to an email
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a prospect
  - slot: unsubscribe_event
    kind: event
    meaning: A prospect unsubscribed from email
  - slot: ae_owner
    kind: attribute
    meaning: The account executive who owns the prospect
  steps:
  - id: s1
    builds: segment
    uses:
    - prospect_outreach_event
    - prospect_engagement_event
    - open_deal
    - target_account
    - unsubscribe_event
    - outreach_threshold
    - lookback_window
    instruction: 'Build a new segment of users named "Silent prospects". A user is in it when all of these are true: they
      did {prospect_outreach_event} {outreach_threshold} or more times in the last {lookback_window}; they did not do {prospect_engagement_event}
      in the last {lookback_window}; their {open_deal} is not true; their {target_account} is not true; they did not do {unsubscribe_event}
      at any time.'
  - id: s2
    builds: email
    uses:
    - topic
    - calendar_link
    - email_subject
    instruction: 'Write a plain break-up email from the sales rep with the subject "{email_subject}". Direct and honest, no
      urgency, no ''final chance''. Four or five sentences: I''ve reached out a few times about {topic}; I might have my timing
      wrong, or this might not be a priority right now; I''ll stop reaching out unless I hear back; if things change, here''s
      an easy way to reconnect: {calendar_link}. No images.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - email_reply_event
    - meeting_scheduled_event
    - ae_owner
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation triggered when a user enters the segment from "Find prospects who went quiet". It sends
      the email from "Write the closing the loop note" once. Then it waits up to 14 days for {email_reply_event} or {meeting_scheduled_event};
      when one happens it emails an alert to {alert_recipients} naming the prospect, their email, {ae_owner} and what happened,
      and stops. A user gets this email at most once.
  - id: s4
    builds: automation
    uses:
    - s3
    - email_reply_event
    - meeting_scheduled_event
    - unsubscribe_event
    - ae_owner
    - digest_recipients
    dependsOn:
    - s3
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users sent the email
      by "Send it once, then stop" and writes these figures: emails sent in the last 7 days; the share of users sent it in
      the last 30 days who did {email_reply_event}, {meeting_scheduled_event} or {unsubscribe_event} within 14 days; the meetings
      it brought back by {ae_owner}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Breakup email for silent prospects

Slash command: /breakup-sequence

## Step 1: Find prospects who went quiet

Build a new segment of users named "Silent prospects". A user is in it when all of these are true: they did prospect outreach event 5 or more times in the last 60 d; they did not do prospect engagement event in the last 60 d; their open deal is not true; their target account is not true; they did not do unsubscribe event at any time.

## Step 2: Write the closing the loop note

Write a plain break-up email from the sales rep with the subject "Closing the loop". Direct and honest, no urgency, no 'final chance'. Four or five sentences: I've reached out a few times about the what you have been reaching out about; I might have my timing wrong, or this might not be a priority right now; I'll stop reaching out unless I hear back; if things change, here's an easy way to reconnect: the calendar link for reconnecting. No images.

## Step 3: Send it once, then stop

Build an automation triggered when a user enters the segment from "Find prospects who went quiet". It sends the email from "Write the closing the loop note" once. Then it waits up to 14 days for email reply event or meeting scheduled event; when one happens it emails an alert to the email addresses that get reply alerts naming the prospect, their email, ae owner and what happened, and stops. A user gets this email at most once.

## Step 4: Email the weekly break-up digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users sent the email by "Send it once, then stop" and writes these figures: emails sent in the last 7 days; the share of users sent it in the last 30 days who did email reply event, meeting scheduled event or unsubscribe event within 14 days; the meetings it brought back by ae owner. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
