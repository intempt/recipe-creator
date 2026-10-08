---
description: 'Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every prior touch, and what to talk about.'
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Meeting prep brief

Slash command: /meeting-prep-brief

## Step 1: Assemble the brief

Create an AI-derived attribute on the Meeting object called 'prep_brief'. Computed at meeting_scheduled time. Output: a structured brief with sections: (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time.

## Step 2: Lay it out to be skimmed

Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing. Use the result of "Assemble the brief".

## Step 3: Send it a day before

Create a workflow firing on meeting_scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery. Use the result of "Assemble the brief", "Lay it out to be skimmed".

## Step 4: Deliver it to the host

Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief. Use the result of "Assemble the brief", "Lay it out to be skimmed", "Send it a day before".

## Step 5: Check every meeting got one

Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed (missing data, attribute compute error). Use the result of "Assemble the brief", "Lay it out to be skimmed", "Send it a day before", "Deliver it to the host".
