---
description: Sends attendees the recording and a next step, sends no shows the on demand link, and shows which webinars actually create deals.
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

# Webinar follow up

Slash command: /webinar-followup

## Step 1: Take everyone who registered

Build a segment 'Recent webinar audience - last 14 days' capturing users registered for a webinar that has ended in the last 14 days. Includes both attendees and no-shows; the branching happens inside the journey via the attendance attribute.

## Step 2: Record who actually turned up

Create an AI-derived attribute on the User object called 'last_webinar_attendance'. Computed at webinar_completed from webinar_attended events. Output: object with (a) webinar_id, (b) attended (boolean), (c) attendance_minutes, (d) engagement_score: composite of attendance duration + questions asked + poll responses, (e) topic of interest based on the webinar. Use the result of "Take everyone who registered".

## Step 3: Write both follow up paths

Generate two parallel email content paths. Attendees path: touch 1 (within 2 hours) thank-you + recording link + 2-3 key takeaways; touch 2 (3 days later) related content recommendation + book-a-meeting CTA; touch 3 (7 days later, if no engagement) AE outreach with personalized angle based on attendance signals. No-shows path: touch 1 (within 2 hours) 'sorry you missed it' + on-demand recording link; touch 2 (3 days later) objection-handling content (the most common reason for no-show is competing priorities: content positions on time-saving); touch 3 (7 days later, if engaged) next-webinar invite. Use the result of "Take everyone who registered", "Record who actually turned up".

## Step 4: Split on whether they showed

Build a branched journey wired to the webinar audience segment. Top-level split on last_webinar_attendance.attended: TRUE to attendee 3-touch path, FALSE to no-show 3-touch path. Both paths feed into the same exit conditions: meeting_scheduled, deal_created, or 14-day max duration. High-engagement attendees (engagement_score >= 70) get fast-tracked to AE-outreach task creation at touch 2 instead of touch 3. Use the result of "Take everyone who registered", "Record who actually turned up", "Write both follow up paths".

## Step 5: See which webinars make deals

Compose a webinar performance dashboard: registration-to-attendance rate, attendance-minutes distribution, post-webinar email engagement by path (attendee vs no-show), webinar-to-meeting conversion rate, and webinar-to-deal-created conversion rate (90 days). Break down by webinar topic and source channel (email vs paid vs organic). Surface the top 3 webinars by deal conversion (those are good rerun candidates). Use the result of "Take everyone who registered", "Record who actually turned up", "Write both follow up paths", "Split on whether they showed".
