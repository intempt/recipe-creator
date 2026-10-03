---
id: demo-request-fast-path
title: Demo request fast path
slash_command: /demo-request-fast-path
group: Workflows
owner: intempt
summary: Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts
  it to Slack, aiming for first contact inside an hour.
description: >-
  When a prospect submits a demo form, fire instant account enrichment, create a high-priority AE task,
  and ping Slack, getting from request to AE outreach in under an hour.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - demo-routing
    - sla
prerequisites:
  events:
    - value: form_submitted
      severity: blocking
    - value: user_identified
      severity: recommended
  integrations:
    - value: slack
      severity: recommended
steps:
  - id: s1
    title: Find recent demo requests
    summary: >-
      Anyone who submitted a demo request form in the last 7 days. They are held out of the normal nurture
      journeys while the fast path runs.
    builds: segment
    description: >-
      Build a segment 'Demo Requesters - last 7 days' capturing users with form_submitted event where
      form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users
      should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path
      window.
  - id: s2
    title: Write the triage card
    summary: >-
      For the demo requests channel: who asked, the account, headcount, industry, a deal size estimate
      where there is one, their last engagement and ICP fit score, and a link to the record. Short and
      scannable.
    builds: slack
    description: >-
      Generate Slack alert content for the #demo-requests channel. Include: requester name, account name,
      employee count, industry, deal-size estimate (if available), prior touch history (last engagement,
      ICP fit score), and a direct link to the user record. Tone: terse, scannable: this is a triage card,
      not a marketing message. Use the result of "Find recent demo requests".
    dependsOn:
      - s1
  - id: s3
    title: Route it inside the hour
    summary: >-
      On a demo request it enriches the account if needed and scores the ICP fit. At 70 or above it creates
      a high priority AE task due the same day, with the contact details, the account context and the
      form answers attached, then posts the card to Slack. Low fit requests go into self serve nurture
      instead.
    builds: workflow
    description: >-
      Create a workflow firing on form_submitted where form_type = demo_request. Step sequence: (1) enrich
      account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as
      user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day
      with the prospect's contact info, account context, and form responses pre-attached; (4) post the
      alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead.
      Use the result of "Find recent demo requests", "Write the triage card".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Hold the response time
    summary: >-
      The funnel from form to task created, task done and meeting booked, with the median and 75th percentile
      time from form to first contact against a 60 minute target in business hours, split by fit tier
      and AE, and a card for any request open more than two hours.
    builds: dashboard
    description: >-
      Compose a dashboard tracking the demo-request response funnel: form_submitted to task_created to
      task_completed to meeting_scheduled. Surface median + p75 time from form_submitted to AE first-touch
      (SLA metric: target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low)
      and by AE owner. Add a card flagging any demo request open >2 hours without a task completion. Use
      the result of "Find recent demo requests", "Write the triage card", "Route it inside the hour".
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
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Demo request fast path

Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts it to Slack, aiming for first contact inside an hour.

## Steps

1. **Find recent demo requests** (builds segment)

   Anyone who submitted a demo request form in the last 7 days. They are held out of the normal nurture journeys while the fast path runs.

2. **Write the triage card** (builds slack)

   For the demo requests channel: who asked, the account, headcount, industry, a deal size estimate where there is one, their last engagement and ICP fit score, and a link to the record. Short and scannable.

3. **Route it inside the hour** (builds workflow)

   On a demo request it enriches the account if needed and scores the ICP fit. At 70 or above it creates a high priority AE task due the same day, with the contact details, the account context and the form answers attached, then posts the card to Slack. Low fit requests go into self serve nurture instead.

4. **Hold the response time** (builds dashboard)

   The funnel from form to task created, task done and meeting booked, with the median and 75th percentile time from form to first contact against a 60 minute target in business hours, split by fit tier and AE, and a card for any request open more than two hours.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
