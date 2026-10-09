---
description: Keeps a demo warm for 90 days with a playbook, a case study, an ROI calculator and a customer story, and pulls the AE in early if they bite.
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
  - media
---

# Post demo nurture

Slash command: /post-demo-nurture

## Step 1: Find recent demo attendees

Build a segment 'Recent demo attendees - last 90 days' capturing users with a meeting_completed event where meeting_type = demo in the last 90 days, attendance = true, and no deal won yet. Excludes users already in active deal-stage cadences (handled by AE manually).

## Step 2: Write five follow ups

This step builds a designed marketing email (HTML).
Generate 5-touch post-demo content. Touch 1 (Day 7): value content - a playbook or guide directly relevant to use case discussed in demo. Touch 2 (Day 14): case study matching the prospect's industry + company size. Touch 3 (Day 30): ROI calculator link with prospect's discussed metrics pre-filled where possible. Touch 4 (Day 60): customer story (video or article) showing 6-month outcomes from a similar customer. Touch 5 (Day 90): decision-stage check-in from the AE asking direct, low-pressure questions about timing/budget/champion status. Personalize using meeting_summary signals from the original demo. Use the result of "Find recent demo attendees".

## Step 3: Send over 90 days

Build a 5-touch journey wired to the post-demo segment: touch 1 at Day 7, touch 2 at Day 14, touch 3 at Day 30, touch 4 at Day 60, touch 5 at Day 90, all relative to meeting_completed. Add a high-engagement branch: if the prospect clicks on touch 1 or 2, route to a dedicated AE-outreach task instead of continuing the automated cadence (signal of buying intent). Exit conditions: Deal created, Meeting scheduled (re-engagement), or unsubscribe. Use the result of "Find recent demo attendees", "Write five follow ups".

## Step 4: Track demo to deal

Compose a dashboard tracking post-demo nurture conversion: demo-to-deal conversion rate (60d, 90d), drop-off by touch (which touches lose the most attention), AE-outreach handoffs triggered (count of high-engagement branches), and deal-velocity comparison between demos that went through the cadence vs not. Flag touches with reply rate below 1% (content failure signal). Use the result of "Find recent demo attendees", "Write five follow ups", "Send over 90 days".
