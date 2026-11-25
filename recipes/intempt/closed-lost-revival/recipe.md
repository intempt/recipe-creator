---
frontmatter_id: closed-lost-revival
slash_command: /closed-lost-revival
description: Goes back to contacts on deals lost 90 to 180 days ago for timing or budget reasons, sends a soft two-email revival,
  alerts the owner on any reply and emails a monthly revival digest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds contacts on deals lost 90 to 180 days ago for reasons that may have expired, sends a soft two-email revival,
    and alerts the team when one comes back.
  parameters:
  - name: lookback_start
    type: duration
    label: Earliest days since loss
    default: 90 d
    required: false
  - name: lookback_end
    type: duration
    label: Latest days since loss
    default: 180 d
    required: false
  - name: max_closed_lost_count
    type: number
    label: Maximum closed-lost count before excluding a contact
    default: 2
    required: false
  - name: followup_delay
    type: duration
    label: Delay before the second email
    default: 14 d
    required: false
  - name: tone
    type: enum
    label: Email tone
    default: warm
    required: false
    options:
    - warm
    - neutral
    - formal
  - name: alert_recipients
    type: string
    label: Email addresses alerted when a lost deal replies
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: deal_lost_event
    kind: event
    meaning: A deal the contact was on was marked closed lost
    properties:
    - name: lost_reason
      type: string
      meaning: Reason the deal was lost, such as timing, budget, no-decision, wrong-fit
      optional: false
  - slot: ae_owner
    kind: attribute
    meaning: Name of the account executive who owned the original deal
  - slot: revival_signal_event
    kind: event
    meaning: The contact replied or booked a meeting after the deal was lost
  steps:
  - id: s1
    builds: segment
    uses:
    - deal_lost_event
    - lookback_start
    - lookback_end
    - max_closed_lost_count
    instruction: 'Build a new segment of users named "Closed-lost revival candidates". A user is in it when all of these are
      true: they did {deal_lost_event} between {lookback_start} and {lookback_end} ago with {deal_lost_event.lost_reason}
      equal to timing, budget, no-decision, internal-resourcing or postponed; they did not do {deal_lost_event} in the last
      {lookback_start}; they did {deal_lost_event} no more than {max_closed_lost_count} times at any time.'
  - id: s2
    builds: email
    uses:
    - s1
    - deal_lost_event
    - ae_owner
    - tone
    dependsOn:
    - s1
    instruction: 'Write a short plain-looking email for users in the segment from "Find losses worth revisiting", signed with
      the name in their {ae_owner} attribute. Open with: it has been a few months, and last time the timing or budget did
      not work out (use their latest {deal_lost_event.lost_reason}). Ask whether anything has changed and offer a 15-minute
      catch-up. A soft re-open, not a pitch. Use a {tone} tone that acknowledges the earlier no.'
  - id: s3
    builds: email
    uses:
    - s1
    - ae_owner
    - tone
    dependsOn:
    - s1
    instruction: Write a short follow-up email for users in the segment from "Find losses worth revisiting" who did not reply
      to the first one, signed with the name in their {ae_owner} attribute. Share one recent product improvement or a story
      from a similar customer that answers a timing or budget concern, and invite a reply if it is worth a fresh look. Use
      a {tone} tone, no pressure, no pricing.
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - revival_signal_event
    - followup_delay
    - ae_owner
    - alert_recipients
    dependsOn:
    - s1
    - s2
    - s3
    instruction: Build an automation that starts when a user enters the segment from "Find losses worth revisiting". It sends
      the email from "Write the first revival email", waits {followup_delay}, and sends the email from "Write the second revival
      email" only if the user did not do {revival_signal_event} since entering. Whenever the user does {revival_signal_event}
      during the automation, it stops sending and emails {alert_recipients} the user's name, email and {ae_owner} so the owner
      can pick it up.
  - id: s5
    builds: automation
    uses:
    - s1
    - deal_lost_event
    - revival_signal_event
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes the
      users who entered the segment from "Find losses worth revisiting" in the last 30 days and writes these figures: how
      many entered; how many did {revival_signal_event} within 30 days of entering; that reply rate; and both counts split
      by {deal_lost_event.lost_reason}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Closed lost revival

Slash command: /closed-lost-revival

## Step 1: Find losses worth revisiting

Build a new segment of users named "Closed-lost revival candidates". A user is in it when all of these are true: they did deal lost event between 90 d and 180 d ago with lost reason equal to timing, budget, no-decision, internal-resourcing or postponed; they did not do deal lost event in the last 90 d; they did deal lost event no more than 2 times at any time.

## Step 2: Write the first revival email

Write a short plain-looking email for users in the segment from "Find losses worth revisiting", signed with the name in their ae owner attribute. Open with: it has been a few months, and last time the timing or budget did not work out (use their latest lost reason). Ask whether anything has changed and offer a 15-minute catch-up. A soft re-open, not a pitch. Use a warm tone that acknowledges the earlier no.

## Step 3: Write the second revival email

Write a short follow-up email for users in the segment from "Find losses worth revisiting" who did not reply to the first one, signed with the name in their ae owner attribute. Share one recent product improvement or a story from a similar customer that answers a timing or budget concern, and invite a reply if it is worth a fresh look. Use a warm tone, no pressure, no pricing.

## Step 4: Send at day 0 and after the wait

Build an automation that starts when a user enters the segment from "Find losses worth revisiting". It sends the email from "Write the first revival email", waits 14 d, and sends the email from "Write the second revival email" only if the user did not do revival signal event since entering. Whenever the user does revival signal event during the automation, it stops sending and emails the email addresses alerted when a lost deal replies the user's name, email and ae owner so the owner can pick it up.

## Step 5: Email the monthly revival digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes the users who entered the segment from "Find losses worth revisiting" in the last 30 days and writes these figures: how many entered; how many did revival signal event within 30 days of entering; that reply rate; and both counts split by lost reason. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
