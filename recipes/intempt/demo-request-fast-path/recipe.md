---
description: Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts it to Slack, aiming for first contact inside an hour.
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

# Demo request fast path

Slash command: /demo-request-fast-path

## Step 1: Find recent demo requests

Build a segment 'Demo Requesters - last 7 days' capturing users with Form submitted event where form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window.

## Step 2: Write the triage card

Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable: this is a triage card, not a marketing message. Use the result of "Find recent demo requests".

## Step 3: Route it inside the hour

Create a workflow firing on Form submitted where form_type = demo_request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect's contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead. Use the result of "Find recent demo requests", "Write the triage card".

## Step 4: Hold the response time

Compose a dashboard tracking the demo-request response funnel: Form submitted to task_created to Task completed to Meeting scheduled. Surface median + p75 time from Form submitted to AE first-touch (SLA metric: target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion. Use the result of "Find recent demo requests", "Write the triage card", "Route it inside the hour".
