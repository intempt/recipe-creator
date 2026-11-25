---
frontmatter_id: webinar-followup
slash_command: /webinar-followup
description: Sends attendees the recording and a next step, sends no shows the on demand link, alerts an AE about highly engaged
  attendees, and emails a weekly digest of which webinars create meetings and deals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Follows up each webinar with an attendee email or a no-show email, alerts AEs about engaged attendees, and emails
    a weekly webinar results digest.
  parameters:
  - name: followup_delay
    type: duration
    label: Wait after the webinar ends before the follow-up
    default: 2 h
    required: false
  - name: high_engagement_minutes
    type: number
    label: Minutes attended that make an attendee highly engaged
    default: 40
    required: false
  - name: deal_conversion_window
    type: duration
    label: Window a meeting or deal counts toward a webinar
    default: 90 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the AE team alerted about engaged attendees
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: webinar_registration
    kind: event
    meaning: A person registered for a webinar
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
    - name: webinar_topic
      type: string
      meaning: Topic of the webinar
      optional: false
  - slot: webinar_attended_event
    kind: event
    meaning: A person attended a webinar
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
    - name: attendance_minutes
      type: number
      meaning: Minutes the person attended
      optional: false
    - name: questions_asked
      type: number
      meaning: Number of questions the person asked
      optional: true
  - slot: webinar_completed_event
    kind: event
    meaning: A webinar the person registered for finished
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
  - slot: webinar_recording_link
    kind: attribute
    meaning: User attribute with the on-demand recording link of the last webinar they registered for
  - slot: meeting_scheduled_event
    kind: event
    meaning: A person scheduled a meeting with sales
  - slot: deal_created_event
    kind: event
    meaning: A deal was created for a person
  steps:
  - id: s1
    builds: email
    uses:
    - webinar_registration
    - webinar_recording_link
    instruction: Write a designed HTML email for people who attended a webinar. Thank them for joining the {webinar_registration.webinar_topic}
      session, give 3 short takeaways, one button to the recording at their {webinar_recording_link} attribute, and a second
      button to book a 20-minute call about applying it. Warm, concise, no pricing.
  - id: s2
    builds: email
    uses:
    - webinar_registration
    - webinar_recording_link
    instruction: Write a designed HTML email for people who registered for a webinar but did not attend. Open with "Sorry
      we missed you", say in two lines what the {webinar_registration.webinar_topic} session covered, and give one button
      to watch on demand at their {webinar_recording_link} attribute. Friendly, no guilt, no pricing.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - webinar_completed_event
    - webinar_attended_event
    - followup_delay
    - high_engagement_minutes
    - alert_recipients
    dependsOn:
    - s1
    - s2
    instruction: Build an automation that starts when a user does {webinar_completed_event}. It waits {followup_delay}. If
      the user did {webinar_attended_event} with the same webinar_id as {webinar_completed_event.webinar_id}, it sends the
      email from "Write the attendee follow up"; otherwise it sends the email from "Write the no show follow up". If {webinar_attended_event.attendance_minutes}
      is {high_engagement_minutes} or more, or {webinar_attended_event.questions_asked} is 1 or more, it also emails {alert_recipients}
      the user's name, email, minutes attended and questions asked so an AE can follow up.
  - id: s4
    builds: automation
    uses:
    - webinar_registration
    - webinar_attended_event
    - meeting_scheduled_event
    - deal_created_event
    - deal_conversion_window
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes webinars, grouped
      by {webinar_registration.webinar_topic}, whose registrations happened in the last {deal_conversion_window}, and writes
      these figures per topic: registrations ({webinar_registration}); attendees ({webinar_attended_event}) and the registration-to-attendance
      rate; registrants who did {meeting_scheduled_event} after registering; registrants who did {deal_created_event} after
      registering. It lists the 3 topics with the most deals first. Then it emails these figures as plain-text lines, each
      with its window, to {digest_recipients}. Nothing else is sent.'
---

# Webinar follow up

Slash command: /webinar-followup

## Step 1: Write the attendee follow up

Write a designed HTML email for people who attended a webinar. Thank them for joining the webinar topic session, give 3 short takeaways, one button to the recording at their webinar recording link attribute, and a second button to book a 20-minute call about applying it. Warm, concise, no pricing.

## Step 2: Write the no show follow up

Write a designed HTML email for people who registered for a webinar but did not attend. Open with "Sorry we missed you", say in two lines what the webinar topic session covered, and give one button to watch on demand at their webinar recording link attribute. Friendly, no guilt, no pricing.

## Step 3: Split on whether they showed

Build an automation that starts when a user does webinar completed event. It waits 2 h. If the user did webinar attended event with the same webinar_id as webinar id, it sends the email from "Write the attendee follow up"; otherwise it sends the email from "Write the no show follow up". If attendance minutes is 40 or more, or questions asked is 1 or more, it also emails the email addresses of the AE team alerted about engaged attendees the user's name, email, minutes attended and questions asked so an AE can follow up.

## Step 4: See which webinars make deals

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes webinars, grouped by webinar topic, whose registrations happened in the last 90 d, and writes these figures per topic: registrations (webinar registration); attendees (webinar attended event) and the registration-to-attendance rate; registrants who did meeting scheduled event after registering; registrants who did deal created event after registering. It lists the 3 topics with the most deals first. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
