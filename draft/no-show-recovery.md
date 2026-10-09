---
description: Assumes a diary clash rather than disinterest and offers an easy reschedule three times over a week, then hands the prospect to nurture.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
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
