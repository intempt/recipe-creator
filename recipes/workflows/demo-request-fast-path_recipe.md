---
name: demo-request-fast-path
description: Use when a user mentions "demo request fast path", "instant demo response", "demo SLA workflow", or asks for related help. When a prospect submits a demo form, fire instant account enrichment, create a high-priority AE task, and ping Slack, getting from request to AE outreach in under an hour.
arguments: []
intempt:
  id: demo-request-fast-path
  title: "Demo request fast path"
  version: 1.0.0
  slashCommand: /demo-request-fast-path
  group: Workflows
  shortDescription: "Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts it to Slack, aiming for first contact inside an hour."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [demo-routing, sla]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: form_submitted, severity: blocking }
      - { value: user_identified, severity: recommended }
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_segment
    - create_slack_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Find recent demo requests"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who submitted a demo request form in the last 7 days. They are held out of the normal nurture journeys while the fast path runs."
      prompt: Build a segment 'Demo Requesters - last 7 days' capturing users with the Form submitted event where form type = demo request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window.
    - step: 2
      title: "Write the triage card"
      command: create_slack_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "For the demo requests channel: who asked, the account, headcount, industry, a deal size estimate where there is one, their last engagement and ICP fit score, and a link to the record. Short and scannable."
      prompt: 'Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable: this is a triage card, not a marketing message.'
    - step: 3
      title: "Route it inside the hour"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset]
      description: "On a demo request it enriches the account if needed and scores the ICP fit. At 70 or above it creates a high priority AE task due the same day, with the contact details, the account context and the form answers attached, then posts the card to Slack. Low fit requests go into self serve nurture instead."
      prompt: 'Create a workflow firing on Form submitted where form type = demo request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect''s contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead.'
    - step: 4
      title: "Hold the response time"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, workflow]
      description: "The funnel from form to task created, task done and meeting booked, with the median and 75th percentile time from form to first contact against a 60 minute target in business hours, split by fit tier and AE, and a card for any request open more than two hours."
      prompt: 'Compose a dashboard tracking the demo-request response funnel: Form submitted to Task created to Task completed to Meeting scheduled. Surface median + p75 time from Form submitted to AE first-touch (SLA metric: target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Demo request fast path

Enriches a demo request the moment it lands, puts a same day task on the right AE, and posts it to Slack, aiming for first contact inside an hour.

## Before you run it

- Connect slack
- Send the `form_submitted` event
- Send the `user_identified` event

## What it does

1. **Find recent demo requests** (`create_segment`)

   Anyone who submitted a demo request form in the last 7 days. They are held out of the normal nurture journeys while the fast path runs.

2. **Write the triage card** (`create_slack_content`)

   For the demo requests channel: who asked, the account, headcount, industry, a deal size estimate where there is one, their last engagement and ICP fit score, and a link to the record. Short and scannable.

3. **Route it inside the hour** (`create_workflow`)

   On a demo request it enriches the account if needed and scores the ICP fit. At 70 or above it creates a high priority AE task due the same day, with the contact details, the account context and the form answers attached, then posts the card to Slack. Low fit requests go into self serve nurture instead.

4. **Hold the response time** (`create_dashboard`)

   The funnel from form to task created, task done and meeting booked, with the median and 75th percentile time from form to first contact against a 60 minute target in business hours, split by fit tier and AE, and a card for any request open more than two hours.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
