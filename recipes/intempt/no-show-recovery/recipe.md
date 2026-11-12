---
frontmatter_id: no-show-recovery
slash_command: /no-show-recovery
description: Assumes a diary clash rather than disinterest and offers an easy reschedule three times over a week, then hands the prospect to nurture.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Wins back prospects who missed a meeting by assuming a scheduling clash, offering an easy reschedule over three
    touches, then handing non-responders to nurture.
  parameters:
  - name: no_show_window
    type: duration
    label: Lookback window for no-shows
    default: 7 d
    required: false
  - name: touch1_delay
    type: duration
    label: Delay before touch 1 after no-show
    default: 1 h
    required: false
  - name: touch2_delay
    type: duration
    label: Delay before touch 2 after no-show
    default: 48 h
    required: false
  - name: touch3_delay
    type: duration
    label: Delay before touch 3 after no-show
    default: 5 d
    required: false
  - name: min_attended_minutes
    type: number
    label: Minutes attended below which a meeting counts as a no-show
    default: 2
    required: false
  - name: reschedule_grace_period
    type: duration
    label: Window after original meeting in which a reschedule excludes the user from the segment
    default: 24 h
    required: false
  requirements:
  - slot: meeting_completed
    kind: event
    meaning: A prospect's scheduled meeting was held or recorded as attended
    properties:
    - name: attendance
      type: boolean
      meaning: Whether the prospect attended the meeting
      optional: false
    - name: attended_minutes
      type: number
      meaning: Minutes the prospect stayed in the meeting
      optional: true
  - slot: meeting_rescheduled
    kind: event
    meaning: A prospect booked a new meeting after missing an earlier one
    properties:
    - name: original_meeting_time
      type: date
      meaning: Start time of the meeting that was missed
      optional: false
  - slot: email_replied
    kind: event
    meaning: A prospect replied to an outreach email
  - slot: opted_out
    kind: attribute
    meaning: A prospect has opted out of marketing or sales outreach
  - slot: recent_no_show_segment
    kind: segment
    meaning: Prospects who missed a scheduled meeting in the recent window and have not rescheduled within the grace period
    creatable: true
    definition: users who did {meeting_completed} with attendance false or attended_minutes below {min_attended_minutes} in
      the last {no_show_window}, excluding users who did {meeting_rescheduled} within {reschedule_grace_period} of the original
      meeting
  - slot: standard_nurture_journey
    kind: integration
    meaning: The existing standard nurture journey that prospects are handed to after recovery outreach
    channel: hubspot
  - slot: booking_link
    kind: integration
    meaning: A calendar scheduling tool with an active reschedule booking link for the meeting host
    channel: hubspot
  - slot: case_study_asset
    kind: knowledge
    meaning: A case study or playbook PDF relevant to the prospect's stage
    optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - meeting_completed
    - meeting_rescheduled
    - no_show_window
    - min_attended_minutes
    - reschedule_grace_period
    instruction: Build the segment "Recent no-shows" of users with {meeting_completed} where {meeting_completed.attendance}
      is false or {meeting_completed.attended_minutes} is below {min_attended_minutes}, within the last {no_show_window}.
      Exclude users who did {meeting_rescheduled} within {reschedule_grace_period} of the original meeting.
  - id: s2
    builds: email
    uses:
    - s1
    - booking_link
    - case_study_asset
    instruction: 'Write a three-touch recovery email sequence for the segment from "Recent no-shows", sent from the original
      meeting host. Touch 1 (sent at {touch1_delay} after the no-show): warm tone, assume a scheduling conflict rather than
      lack of interest, no guilt, offer an easy reschedule with a new link from {booking_link}. Touch 2 (sent at {touch2_delay}
      after the no-show, only if unresponsive): briefly remind them the booking link is still available and reference the
      original meeting. Touch 3 (sent at {touch3_delay} after the no-show): final outreach with a relevant value asset from
      {case_study_asset} for their stage plus the booking link as a soft re-engage.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - standard_nurture_journey
    - meeting_rescheduled
    - email_replied
    - opted_out
    - touch1_delay
    - touch2_delay
    - touch3_delay
    instruction: Build a three-touch journey wired to the "Recent no-shows" segment. Send touch 1 from "Write a three-touch
      recovery email sequence" at {touch1_delay} after the no-show. Send touch 2 at {touch2_delay} after the no-show, skipping
      users who did {meeting_rescheduled}. Send touch 3 at {touch3_delay} after the no-show, skipping users who did {meeting_rescheduled}
      or {email_replied}. After touch 3 with no engagement, move the user into {standard_nurture_journey} as the handoff.
      Exit the journey when the user did {meeting_rescheduled}, did {email_replied}, or {opted_out} is true.
  - id: s4
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - meeting_completed
    - meeting_rescheduled
    instruction: 'Create a no-show recovery health dashboard showing: overall no-show rate as a percentage of scheduled meetings
      with its trend over time; reschedule conversion rate as the percentage of users in "Recent no-shows" who did {meeting_rescheduled}
      through the journey in "Build a three-touch journey wired to the" segment; time-to-reschedule distribution; and per-touch
      open, click, and reschedule rates for the touches from "Write a three-touch recovery email sequence". Break down all
      metrics by meeting type and by rep. Flag an alert when the no-show rate rises by more than 5 percentage points week
      over week.'
---

# Meeting no show recovery

Slash command: /no-show-recovery

## Step 1: Find who missed a meeting

Build a segment 'Recent no-shows - last 7 days' capturing users with a meeting_completed event in the last 7 days where the attendance attribute = false (or attended_minutes < 2). Excludes users who have already rescheduled within 24 hours of the original meeting.

## Step 2: Write three reschedule notes

Generate 3-touch recovery email content. Touch 1 (1 hour after no-show): assumes scheduling conflict; warm tone; offers easy reschedule with new booking link; no guilt. Touch 2 (48 hours later, if unresponsive): brief reminder that the booking link is still available; references the original meeting context. Touch 3 (5 days later): final outreach with value-content (case study or playbook PDF relevant to their stage) plus the booking link as a soft re-engage. Send-from: the original meeting host. Use the result of "Find who missed a meeting".

## Step 3: Send at 1 hour, 2 days, 5 days

Build a 3-touch journey wired to the no-show segment: send touch 1 at 1 hour after no-show, touch 2 at 48 hours after no-show (skip if user has rescheduled), touch 3 at 5 days after no-show (skip if user has rescheduled or replied). After touch 3 with no engagement: move user into the standard nurture journey (handoff). Exit conditions: Meeting scheduled (rescheduled), email_replied, or user opted out. Use the result of "Find who missed a meeting", "Write three reschedule notes".

## Step 4: Watch the no show rate

Compose a dashboard tracking no-show recovery health: overall no-show rate (% of scheduled meetings that no-show, trend over time), reschedule conversion rate (% of no-shows that book a new meeting via the recovery journey), time-to-reschedule distribution, and per-touch open/click/reschedule rates. Break down by meeting type and rep. Flag if no-show rate is rising more than 5 percentage points week-over-week (process or scheduling-link problem signal). Use the result of "Find who missed a meeting", "Write three reschedule notes", "Send at 1 hour, 2 days, 5 days".
