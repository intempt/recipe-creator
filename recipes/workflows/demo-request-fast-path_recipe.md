---
name: demo-request-fast-path
description: Use when a user mentions "demo request fast path", "instant demo response", "demo SLA workflow", or asks for related help. When a prospect submits a demo form, fire instant account enrichment, create a high-priority AE task, and ping Slack — getting from request to AE outreach in under an hour.
arguments: []
intempt:
  id: demo-request-fast-path
  version: 1.0.0
  slashCommand: /demo-request-fast-path
  group: Workflows
  shortDescription: "When a prospect submits a demo form, fire instant account enrichment, create a high-priority AE task, and ping Slack — getting from request to AE outreach in under an hour."
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
      title: Identify Demo Requesters
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Demo Requesters - last 7 days' capturing users with form_submitted event where form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window.
      prompt: Build a segment 'Demo Requesters - last 7 days' capturing users with form_submitted event where form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window.
    - step: 2
      title: Build Alert Content
      command: create_slack_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: 'Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable — this is a triage card, not a marketing message.'
      prompt: 'Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable — this is a triage card, not a marketing message.'
    - step: 3
      title: Build Routing Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [segment, asset]
      description: 'Create a workflow firing on form_submitted where form_type = demo_request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect''s contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead.'
      prompt: 'Create a workflow firing on form_submitted where form_type = demo_request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect''s contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead.'
    - step: 4
      title: Build SLA Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, workflow]
      description: 'Compose a dashboard tracking the demo-request response funnel: form_submitted → task_created → task_completed → meeting_scheduled. Surface median + p75 time from form_submitted to AE first-touch (SLA metric — target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion.'
      prompt: 'Compose a dashboard tracking the demo-request response funnel: form_submitted → task_created → task_completed → meeting_scheduled. Surface median + p75 time from form_submitted to AE first-touch (SLA metric — target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Demo Request Fast Path

## Procedure

1. **Identify Demo Requesters** [`create_segment`] — Build a segment 'Demo Requesters - last 7 days' capturing users with form_submitted event where form_type = demo_request in the last 7 days. Used by the routing workflow to identify which users should hit the fast-path and excluded from standard nurture journeys for the duration of the fast-path window. → produces: segment
2. **Build Alert Content** [`create_slack_content`] — Generate Slack alert content for the #demo-requests channel. Include: requester name, account name, employee count, industry, deal-size estimate (if available), prior touch history (last engagement, ICP fit score), and a direct link to the user record. Tone: terse, scannable — this is a triage card, not a marketing message. → produces: asset
3. **Build Routing Workflow** [`create_workflow`] — Create a workflow firing on form_submitted where form_type = demo_request. Step sequence: (1) enrich account via firmographic lookup if not already enriched; (2) compute ICP fit score and store as user attribute; (3) for high-fit ICPs (score >= 70), create a high-priority AE task due same-day with the prospect's contact info, account context, and form responses pre-attached; (4) post the alert content to Slack #demo-requests. For low-fit ICPs, drop into self-serve nurture journey instead. → produces: workflow
4. **Build SLA Dashboard** [`create_dashboard`] — Compose a dashboard tracking the demo-request response funnel: form_submitted → task_created → task_completed → meeting_scheduled. Surface median + p75 time from form_submitted to AE first-touch (SLA metric — target: under 60 minutes during business hours). Break down by ICP fit tier (high/med/low) and by AE owner. Add a card flagging any demo request open >2 hours without a task completion. → produces: dashboard
