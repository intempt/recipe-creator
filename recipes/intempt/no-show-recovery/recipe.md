---
id: no-show-recovery
title: Meeting no show recovery
slash_command: /no-show-recovery
group: Journeys
owner: intempt
summary: Assumes a diary clash rather than disinterest and offers an easy reschedule three times over
  a week, then hands the prospect to nurture.
description: >-
  When a prospect doesn't attend a scheduled meeting, fire a 3-touch recovery sequence over 7 days, assuming
  scheduling conflict (not disinterest) and offering an easy reschedule, then dropping into nurture if
  still unresponsive.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - no-show
    - meeting-recovery
prerequisites:
  events:
    - value: meeting_completed
      severity: blocking
    - value: meeting_scheduled
      severity: recommended
touches:
  reads:
    - The meeting_completed event in your project
    - The meeting_scheduled event in your project
  writes:
    - A new segment, from step 1 "Find who missed a meeting"
    - A new designed email, from step 2 "Write three reschedule notes"
    - A new journey, from step 3 "Send at 1 hour, 2 days, 5 days"
    - A new dashboard, from step 4 "Watch the no show rate"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find who missed a meeting
    summary: >-
      Anyone whose meeting in the last 7 days shows no attendance, or under two minutes of it. People
      who already rebooked within a day are left out.
    builds: segment
    description: >-
      Build a segment 'Recent no-shows - last 7 days' capturing users with a meeting_completed event in
      the last 7 days where the attendance attribute = false (or attended_minutes < 2). Excludes users
      who have already rescheduled within 24 hours of the original meeting.
  - id: s2
    title: Write three reschedule notes
    summary: >-
      One hour after: warm, assumes a clash, offers a new booking link, no guilt. Two days later: a short
      reminder that the link is still open, referencing the original meeting. Five days later: a case
      study or playbook for their stage, with the link attached. All from the person who was hosting.
    builds: email_html
    description: >-
      Generate 3-touch recovery email content. Touch 1 (1 hour after no-show): assumes scheduling conflict;
      warm tone; offers easy reschedule with new booking link; no guilt. Touch 2 (48 hours later, if unresponsive):
      brief reminder that the booking link is still available; references the original meeting context.
      Touch 3 (5 days later): final outreach with value-content (case study or playbook PDF relevant to
      their stage) plus the booking link as a soft re-engage. Send-from: the original meeting host. Use
      the result of "Find who missed a meeting".
    dependsOn:
      - s1
  - id: s3
    title: Send at 1 hour, 2 days, 5 days
    summary: >-
      Each email is skipped if they have already rebooked or replied. If nothing lands by the third, they
      move into the standard nurture journey. They leave on a new booking, a reply, or an opt out.
    builds: journey
    description: >-
      Build a 3-touch journey wired to the no-show segment: send touch 1 at 1 hour after no-show, touch
      2 at 48 hours after no-show (skip if user has rescheduled), touch 3 at 5 days after no-show (skip
      if user has rescheduled or replied). After touch 3 with no engagement: move user into the standard
      nurture journey (handoff). Exit conditions: meeting_scheduled (rescheduled), email_replied, or user
      opted out. Use the result of "Find who missed a meeting", "Write three reschedule notes".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Watch the no show rate
    summary: >-
      The overall no show rate and its trend, how many rebook through this sequence, how long that takes,
      and open, click and reschedule rates per email, broken out by meeting type and rep. A rise of more
      than five points week over week is flagged.
    builds: dashboard
    description: >-
      Compose a dashboard tracking no-show recovery health: overall no-show rate (% of scheduled meetings
      that no-show, trend over time), reschedule conversion rate (% of no-shows that book a new meeting
      via the recovery journey), time-to-reschedule distribution, and per-touch open/click/reschedule
      rates. Break down by meeting type and rep. Flag if no-show rate is rising more than 5 percentage
      points week-over-week (process or scheduling-link problem signal). Use the result of "Find who missed
      a meeting", "Write three reschedule notes", "Send at 1 hour, 2 days, 5 days".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Meeting no show recovery

Assumes a diary clash rather than disinterest and offers an easy reschedule three times over a week, then hands the prospect to nurture.

## Steps

1. **Find who missed a meeting** (builds segment)

   Anyone whose meeting in the last 7 days shows no attendance, or under two minutes of it. People who already rebooked within a day are left out.

2. **Write three reschedule notes** (builds email_html)

   One hour after: warm, assumes a clash, offers a new booking link, no guilt. Two days later: a short reminder that the link is still open, referencing the original meeting. Five days later: a case study or playbook for their stage, with the link attached. All from the person who was hosting.

3. **Send at 1 hour, 2 days, 5 days** (builds journey)

   Each email is skipped if they have already rebooked or replied. If nothing lands by the third, they move into the standard nurture journey. They leave on a new booking, a reply, or an opt out.

4. **Watch the no show rate** (builds dashboard)

   The overall no show rate and its trend, how many rebook through this sequence, how long that takes, and open, click and reschedule rates per email, broken out by meeting type and rep. A rise of more than five points week over week is flagged.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The meeting_completed event in your project
- The meeting_scheduled event in your project

Writes:

- A new segment, from step 1 "Find who missed a meeting"
- A new designed email, from step 2 "Write three reschedule notes"
- A new journey, from step 3 "Send at 1 hour, 2 days, 5 days"
- A new dashboard, from step 4 "Watch the no show rate"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
