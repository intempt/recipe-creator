---
id: meeting-prep-brief
title: Meeting prep brief
slash_command: /meeting-prep-brief
group: Workflows
owner: intempt
curator: trishik
summary: 'Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every
  prior touch, and what to talk about.'
description: >-
  When a meeting is scheduled, auto-generate an AE prep brief 24 hours before the meeting (stakeholder
  map, prior touches, account health, suggested talking points) delivered to the host via email or Slack.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
  vertical:
    - sales-led
  complexity: standard
  executionMode: live
  tags:
    - meeting-prep
    - ae-enablement
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: meeting_scheduled
      severity: blocking
touches:
  reads:
    - The meeting_scheduled event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Assemble the brief"
    - A new designed email, from step 2 "Lay it out to be skimmed"
    - A new workflow, from step 3 "Send it a day before"
    - A new journey, from step 4 "Deliver it to the host"
    - A new dashboard, from step 5 "Check every meeting got one"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Assemble the brief
    summary: >-
      Built when the meeting is booked: the attendees with their titles, their role on the deal and their
      recent activity, the account's revenue, plan, health score and open opportunities, the last five
      interactions across email, meetings and support, talking points drawn from the deal stage, recent
      product usage and any open tickets, and any competitive flags. It rebuilds if an attendee is added
      within an hour of the meeting.
    builds: attribute
    description: >-
      Create an AI-derived attribute on the Meeting object called 'prep_brief'. Computed at meeting_scheduled
      time. Output: a structured brief with sections: (a) attendees: name, title, role on deal, recent
      activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history:
      last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from
      deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag
      exists. Refreshes if a new attendee is added within 1 hour of meeting time.
  - id: s2
    title: Lay it out to be skimmed
    summary: >-
      An email with the meeting details at the top, then sections for the account, previous touches, talking
      points and competitive notes, plus a button to open the brief in the app. Plain and useful, not
      marketing.
    builds: email_html
    description: >-
      Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout.
      Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for
      account, prior touches, talking points, competitive intel. Include a CTA button to view the brief
      in the app. Tone: utilitarian, not marketing. Use the result of "Assemble the brief".
    dependsOn:
      - s1
  - id: s3
    title: Send it a day before
    summary: >-
      On booking, delivery is scheduled for 24 hours before the meeting, or straight away if the meeting
      is sooner than that. The brief is rebuilt just before it goes, so late changes are included. A reschedule
      moves the delivery and a cancellation stops it.
    builds: workflow
    description: >-
      Create a workflow firing on meeting_scheduled. Schedule a delayed step to fire 24 hours before the
      meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief
      attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host.
      If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress
      delivery. Use the result of "Assemble the brief", "Lay it out to be skimmed".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Deliver it to the host
    summary: >-
      One message to the host, not the attendees. Email by default, or a Slack message with a link if
      Slack is connected and the host has an ID there.
    builds: journey
    description: >-
      Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the
      prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default;
      if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to
      the brief. Use the result of "Assemble the brief", "Lay it out to be skimmed", "Send it a day before".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Check every meeting got one
    summary: >-
      The share of meetings where a brief was actually delivered, how long before the meeting it went,
      and how often hosts open it, broken out by meeting type. Any meeting where the brief could not be
      built, for missing data or an error, is flagged.
    builds: dashboard
    description: >-
      Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median
      time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting
      type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed
      (missing data, attribute compute error). Use the result of "Assemble the brief", "Lay it out to
      be skimmed", "Send it a day before", "Deliver it to the host".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
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

# Meeting prep brief

Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every prior touch, and what to talk about.

## Steps

1. **Assemble the brief** (builds attribute)

   Built when the meeting is booked: the attendees with their titles, their role on the deal and their recent activity, the account's revenue, plan, health score and open opportunities, the last five interactions across email, meetings and support, talking points drawn from the deal stage, recent product usage and any open tickets, and any competitive flags. It rebuilds if an attendee is added within an hour of the meeting.

2. **Lay it out to be skimmed** (builds email_html)

   An email with the meeting details at the top, then sections for the account, previous touches, talking points and competitive notes, plus a button to open the brief in the app. Plain and useful, not marketing.

3. **Send it a day before** (builds workflow)

   On booking, delivery is scheduled for 24 hours before the meeting, or straight away if the meeting is sooner than that. The brief is rebuilt just before it goes, so late changes are included. A reschedule moves the delivery and a cancellation stops it.

4. **Deliver it to the host** (builds journey)

   One message to the host, not the attendees. Email by default, or a Slack message with a link if Slack is connected and the host has an ID there.

5. **Check every meeting got one** (builds dashboard)

   The share of meetings where a brief was actually delivered, how long before the meeting it went, and how often hosts open it, broken out by meeting type. Any meeting where the brief could not be built, for missing data or an error, is flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The meeting_scheduled event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Assemble the brief"
- A new designed email, from step 2 "Lay it out to be skimmed"
- A new workflow, from step 3 "Send it a day before"
- A new journey, from step 4 "Deliver it to the host"
- A new dashboard, from step 5 "Check every meeting got one"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
