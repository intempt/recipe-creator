---
id: webinar-followup
title: Webinar follow up
slash_command: /webinar-followup
group: Journeys
owner: intempt
summary: Sends attendees the recording and a next step, sends no shows the on demand link, and shows which
  webinars actually create deals.
description: >-
  When a webinar ends, fire branched follow-ups: attendees get the recording + next-step CTA + thank-you,
  no-shows get the on-demand link + objection-handling content: both feeding into a unified post-webinar
  conversion dashboard.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - webinar-followup
    - event-marketing
prerequisites:
  events:
    - value: webinar_completed
      severity: blocking
    - value: webinar_attended
      severity: blocking
touches:
  reads:
    - The webinar_completed event in your project
    - The webinar_attended event in your project
  writes:
    - A new segment, from step 1 "Take everyone who registered"
    - A new attribute, from step 2 "Record who actually turned up"
    - A new designed email, from step 3 "Write both follow up paths"
    - A new journey, from step 4 "Split on whether they showed"
    - A new dashboard, from step 5 "See which webinars make deals"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Take everyone who registered
    summary: >-
      Everyone registered for a webinar that ended in the last 14 days, attendees and no shows alike.
      The split happens inside the journey.
    builds: segment
    description: >-
      Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar
      that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens
      inside the journey via the attendance attribute.
  - id: s2
    title: Record who actually turned up
    summary: >-
      Per person: which webinar, whether they attended, how many minutes they watched, an engagement score
      from that plus questions asked and polls answered, and the topic they came for.
    builds: attribute
    description: >-
      Create an AI-derived attribute on the User object called 'last_webinar_attendance'. Computed at
      webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended
      (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions
      asked + poll responses, (e) topic of interest based on the webinar. Use the result of "Take everyone
      who registered".
    dependsOn:
      - s1
  - id: s3
    title: Write both follow up paths
    summary: >-
      Attendees get a thank you with the recording and the key takeaways within two hours, related content
      and a meeting invitation on day 3, and AE outreach on day 7 if nothing has landed. No shows get
      the on demand link within two hours, content answering the usual reason for missing it on day 3,
      and an invitation to the next one on day 7 if they engaged.
    builds: email_html
    description: >-
      Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you +
      recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting
      CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance
      signals. No-shows path: touch 1 (within 2 hours) 'sorry you missed it' + on-demand recording link;
      touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing
      priorities: content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite.
      Use the result of "Take everyone who registered", "Record who actually turned up".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Split on whether they showed
    summary: >-
      Attendees take one three touch path and no shows the other. Attendees scoring 70 or more on engagement
      skip ahead to an AE task at the second touch. Both paths end on a booked meeting, a new deal, or
      after 14 days.
    builds: journey
    description: >-
      Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended:
      TRUE to attendee 3-touch path, FALSE to no-show 3-touch path. Both paths feed into the same exit
      conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score
      >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3. Use the result
      of "Take everyone who registered", "Record who actually turned up", "Write both follow up paths".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: See which webinars make deals
    summary: >-
      Registration to attendance, minutes watched, engagement per path, and webinar to meeting and webinar
      to deal conversion over 90 days, broken out by topic and channel, with the top three for deal conversion
      called out as rerun candidates.
    builds: dashboard
    description: >-
      Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution,
      post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate,
      and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel
      (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun
      candidates). Use the result of "Take everyone who registered", "Record who actually turned up",
      "Write both follow up paths", "Split on whether they showed".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: attribute
    producedByStep: s2
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Webinar follow up

Sends attendees the recording and a next step, sends no shows the on demand link, and shows which webinars actually create deals.

## Steps

1. **Take everyone who registered** (builds segment)

   Everyone registered for a webinar that ended in the last 14 days, attendees and no shows alike. The split happens inside the journey.

2. **Record who actually turned up** (builds attribute)

   Per person: which webinar, whether they attended, how many minutes they watched, an engagement score from that plus questions asked and polls answered, and the topic they came for.

3. **Write both follow up paths** (builds email_html)

   Attendees get a thank you with the recording and the key takeaways within two hours, related content and a meeting invitation on day 3, and AE outreach on day 7 if nothing has landed. No shows get the on demand link within two hours, content answering the usual reason for missing it on day 3, and an invitation to the next one on day 7 if they engaged.

4. **Split on whether they showed** (builds journey)

   Attendees take one three touch path and no shows the other. Attendees scoring 70 or more on engagement skip ahead to an AE task at the second touch. Both paths end on a booked meeting, a new deal, or after 14 days.

5. **See which webinars make deals** (builds dashboard)

   Registration to attendance, minutes watched, engagement per path, and webinar to meeting and webinar to deal conversion over 90 days, broken out by topic and channel, with the top three for deal conversion called out as rerun candidates.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The webinar_completed event in your project
- The webinar_attended event in your project

Writes:

- A new segment, from step 1 "Take everyone who registered"
- A new attribute, from step 2 "Record who actually turned up"
- A new designed email, from step 3 "Write both follow up paths"
- A new journey, from step 4 "Split on whether they showed"
- A new dashboard, from step 5 "See which webinars make deals"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
