---
name: no-show-recovery
description: Use when a user mentions "no-show recovery", "missed meeting re-engagement", "no-show recovery sequence", or asks for related help. When a prospect doesn't attend a scheduled meeting, fire a 3-touch recovery sequence over 7 days, assuming scheduling conflict (not disinterest) and offering an easy reschedule, then dropping into nurture if still unresponsive.
arguments: []
intempt:
  id: no-show-recovery
  title: "Meeting no show recovery"
  version: 1.0.0
  slashCommand: /no-show-recovery
  group: Journeys
  shortDescription: "Assumes a diary clash rather than disinterest and offers an easy reschedule three times over a week, then hands the prospect to nurture."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [no-show, meeting-recovery]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: meeting_completed, severity: blocking }
      - { value: meeting_scheduled, severity: recommended }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find who missed a meeting"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone whose meeting in the last 7 days shows no attendance, or under two minutes of it. People who already rebooked within a day are left out."
      prompt: Build a segment 'Recent no-shows - last 7 days' capturing users with a meeting_completed event in the last 7 days where the attendance attribute = false (or attended_minutes < 2). Excludes users who have already rescheduled within 24 hours of the original meeting.
    - step: 2
      title: "Write three reschedule notes"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "One hour after: warm, assumes a clash, offers a new booking link, no guilt. Two days later: a short reminder that the link is still open, referencing the original meeting. Five days later: a case study or playbook for their stage, with the link attached. All from the person who was hosting."
      prompt: 'Generate 3-touch recovery email content. Touch 1 (1 hour after no-show): assumes scheduling conflict; warm tone; offers easy reschedule with new booking link; no guilt. Touch 2 (48 hours later, if unresponsive): brief reminder that the booking link is still available; references the original meeting context. Touch 3 (5 days later): final outreach with value-content (case study or playbook PDF relevant to their stage) plus the booking link as a soft re-engage. Send-from: the original meeting host.'
    - step: 3
      title: "Send at 1 hour, 2 days, 5 days"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Each email is skipped if they have already rebooked or replied. If nothing lands by the third, they move into the standard nurture journey. They leave on a new booking, a reply, or an opt out."
      prompt: 'Build a 3-touch journey wired to the no-show segment: send touch 1 at 1 hour after no-show, touch 2 at 48 hours after no-show (skip if user has rescheduled), touch 3 at 5 days after no-show (skip if user has rescheduled or replied). After touch 3 with no engagement: move user into the standard nurture journey (handoff). Exit conditions: meeting_scheduled (rescheduled), email_replied, or user opted out.'
    - step: 4
      title: "Watch the no show rate"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey]
      description: "The overall no show rate and its trend, how many rebook through this sequence, how long that takes, and open, click and reschedule rates per email, broken out by meeting type and rep. A rise of more than five points week over week is flagged."
      prompt: 'Compose a dashboard tracking no-show recovery health: overall no-show rate (% of scheduled meetings that no-show, trend over time), reschedule conversion rate (% of no-shows that book a new meeting via the recovery journey), time-to-reschedule distribution, and per-touch open/click/reschedule rates. Break down by meeting type and rep. Flag if no-show rate is rising more than 5 percentage points week-over-week (process or scheduling-link problem signal).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Meeting no show recovery

Assumes a diary clash rather than disinterest and offers an easy reschedule three times over a week, then hands the prospect to nurture.

## Before you run it

- Send the `meeting_completed` event
- Send the `meeting_scheduled` event

## What it does

1. **Find who missed a meeting** (`create_segment`)

   Anyone whose meeting in the last 7 days shows no attendance, or under two minutes of it. People who already rebooked within a day are left out.

2. **Write three reschedule notes** (`create_email_content`)

   One hour after: warm, assumes a clash, offers a new booking link, no guilt. Two days later: a short reminder that the link is still open, referencing the original meeting. Five days later: a case study or playbook for their stage, with the link attached. All from the person who was hosting.

3. **Send at 1 hour, 2 days, 5 days** (`create_journey`)

   Each email is skipped if they have already rebooked or replied. If nothing lands by the third, they move into the standard nurture journey. They leave on a new booking, a reply, or an opt out.

4. **Watch the no show rate** (`create_dashboard`)

   The overall no show rate and its trend, how many rebook through this sequence, how long that takes, and open, click and reschedule rates per email, broken out by meeting type and rep. A rise of more than five points week over week is flagged.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
