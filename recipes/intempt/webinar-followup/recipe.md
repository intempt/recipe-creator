---
frontmatter_id: webinar-followup
slash_command: /webinar-followup
description: Sends attendees the recording and a next step, sends no shows the on demand link, and shows which webinars actually create deals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends webinar attendees the recording and a next step, sends no-shows the on-demand link, and reports which webinars
    actually create deals.
  parameters:
  - name: registration_window
    type: duration
    label: Registration lookback window after webinar ends
    default: 14 d
    required: false
  - name: attendee_followup_delay
    type: duration
    label: Attendee thank-you delay
    default: 2 h
    required: false
  - name: second_touch_delay
    type: duration
    label: Second touch delay
    default: 3 d
    required: false
  - name: third_touch_delay
    type: duration
    label: Third touch delay
    default: 7 d
    required: false
  - name: high_engagement_threshold
    type: number
    label: Engagement score for fast-track to AE outreach
    default: 70
    required: false
  - name: journey_max_duration
    type: duration
    label: Maximum journey duration
    default: 14 d
    required: false
  - name: deal_conversion_window
    type: duration
    label: Deal conversion window for dashboard
    default: 90 d
    required: false
  - name: top_webinar_count
    type: number
    label: Number of top webinars to surface
    default: 3
    required: false
  requirements:
  - slot: webinar_registration
    kind: event
    meaning: A customer registered for a webinar
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
    - name: webinar_topic
      type: string
      meaning: Topic of the webinar
      optional: true
    - name: webinar_end_date
      type: date
      meaning: When the webinar ended
      optional: false
    - name: source_channel
      type: string
      meaning: Channel that drove the registration (email, paid, organic)
      optional: true
  - slot: webinar_attended_event
    kind: event
    meaning: A customer attended a webinar
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
    - name: attendance_minutes
      type: number
      meaning: Minutes the customer stayed in the webinar
      optional: true
    - name: questions_asked
      type: number
      meaning: Number of questions asked during the webinar
      optional: true
    - name: poll_responses
      type: number
      meaning: Number of poll responses given during the webinar
      optional: true
  - slot: webinar_completed_event
    kind: event
    meaning: A webinar finished running
    properties:
    - name: webinar_id
      type: string
      meaning: Identifier of the webinar
      optional: false
  - slot: deal_created_event
    kind: event
    meaning: A deal was created for a customer
    properties:
    - name: webinar_id
      type: string
      meaning: Webinar associated with the deal, if any
      optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A customer scheduled a meeting with sales
  - slot: webinar_recording_link
    kind: attribute
    meaning: Link to the on-demand webinar recording
  - slot: ae_outreach_task
    kind: integration
    meaning: A connected CRM or task tool where account executive follow-up tasks are created
    channel: salesforce
  - slot: email_channel
    kind: destination
    meaning: Email sending channel used for follow-up messages
    channel: email
  - slot: recent_webinar_audience
    kind: segment
    meaning: Users registered for a webinar that ended within the lookback window
    creatable: true
    definition: users who did {webinar_registration} for a webinar that ended in the last {registration_window}
  - slot: last_webinar_attendance
    kind: attribute
    meaning: Per-user record of the latest webinar attendance, attendance flag, minutes and engagement score
  steps:
  - id: s1
    builds: segment
    uses:
    - webinar_registration
    - registration_window
    instruction: Build the segment {recent_webinar_audience} capturing users who registered for a webinar that ended within
      the last {registration_window}. Include both attendees and no-shows; the branching happens in the journey via the attendance
      attribute.
  - id: s2
    builds: attribute
    uses:
    - webinar_completed_event
    - webinar_attended_event
    - s1
    instruction: 'Create an AI-derived attribute on the User object called ''last_webinar_attendance'', computed at {webinar_completed_event}
      from {webinar_attended_event} events. Output an object with: webinar_id, attended (boolean), attendance_minutes, an
      engagement score combining attendance duration, {webinar_attended_event.questions_asked} and {webinar_attended_event.poll_responses},
      and the topic of interest based on the webinar. Apply it to users in {recent_webinar_audience}.'
  - id: s3
    builds: email
    uses:
    - webinar_recording_link
    - attendee_followup_delay
    - second_touch_delay
    - third_touch_delay
    - s1
    - s2
    instruction: 'Generate two parallel email content paths. Attendees path: touch 1 within {attendee_followup_delay} with
      a thank-you, the {webinar_recording_link} and 2-3 key takeaways; touch 2 after {second_touch_delay} with related content
      and a book-a-meeting call to action; touch 3 after {third_touch_delay} with an AE outreach email personalized from attendance
      signals, sent only if the user has not engaged. No-shows path: touch 1 within {attendee_followup_delay} with a ''sorry
      you missed it'' note and the {webinar_recording_link}; touch 2 after {second_touch_delay} with objection-handling content
      on competing priorities, positioning the content on time-saving; touch 3 after {third_touch_delay} with a next-webinar
      invite, sent only if the user has engaged.'
  - id: s4
    builds: automation
    uses:
    - recent_webinar_audience
    - last_webinar_attendance
    - meeting_scheduled_event
    - deal_created_event
    - ae_outreach_task
    - high_engagement_threshold
    - journey_max_duration
    - s1
    - s2
    - s3
    instruction: 'Build a branched journey on {recent_webinar_audience}. Top-level split on {last_webinar_attendance.attended}:
      TRUE routes to the attendee path from "Write both follow up paths", FALSE routes to the no-show path. Both paths exit
      on {meeting_scheduled_event}, {deal_created_event}, or after {journey_max_duration}. Attendees with {last_webinar_attendance.engagement_score}
      at or above {high_engagement_threshold} are fast-tracked: create an AE outreach task in {ae_outreach_task} at touch
      2 instead of touch 3.'
  - id: s5
    builds: dashboard
    uses:
    - webinar_registration
    - webinar_attended_event
    - meeting_scheduled_event
    - deal_created_event
    - deal_conversion_window
    - top_webinar_count
    - s2
    - s3
    - s4
    instruction: 'Compose a webinar performance dashboard showing: registration-to-attendance rate; attendance-minutes distribution;
      post-webinar email engagement by path (attendee vs no-show); webinar-to-meeting conversion; and webinar-to-deal-created
      conversion within {deal_conversion_window}. Break down by webinar topic and source channel (email, paid, organic). Surface
      the top {top_webinar_count} webinars by deal conversion as rerun candidates.'
---

# Webinar follow up

Slash command: /webinar-followup

## Step 1: Take everyone who registered

Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute.

## Step 2: Record who actually turned up

Create an AI-derived attribute on the User object called 'last_webinar_attendance'. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) Engagement score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar. Use the result of "Take everyone who registered".

## Step 3: Write both follow up paths

Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) 'sorry you missed it' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities: content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite. Use the result of "Take everyone who registered", "Record who actually turned up".

## Step 4: Split on whether they showed

Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE to attendee 3-touch path, FALSE to no-show 3-touch path. Both paths feed into the same exit conditions: Meeting scheduled, Deal created, or 14-day max duration. High-engagement attendees (Engagement score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3. Use the result of "Take everyone who registered", "Record who actually turned up", "Write both follow up paths".

## Step 5: See which webinars make deals

Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates). Use the result of "Take everyone who registered", "Record who actually turned up", "Write both follow up paths", "Split on whether they showed".
