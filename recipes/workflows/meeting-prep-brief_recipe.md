---
name: meeting-prep-brief
description: Use when a user mentions "meeting prep brief", "pre-meeting brief", "AE prep document", or asks for related help. When a meeting is scheduled, auto-generate an AE prep brief 24 hours before the meeting — stakeholder map, prior touches, account health, suggested talking points — delivered to the host via email or Slack.
arguments: []
intempt:
  id: meeting-prep-brief
  version: 1.0.0
  slashCommand: /meeting-prep-brief
  group: Workflows
  shortDescription: "When a meeting is scheduled, auto-generate an AE prep brief 24 hours before the meeting — stakeholder map, prior touches, account health, suggested talking points — delivered to the host via email or Slack."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [meeting-prep, ae-enablement]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: meeting_scheduled, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_email_content
    - create_workflow
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Prep Brief AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: 'Create an AI-derived attribute on the Meeting object called ''prep_brief''. Computed at meeting_scheduled time. Output: a structured brief with sections — (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time.'
      prompt: 'Create an AI-derived attribute on the Meeting object called ''prep_brief''. Computed at meeting_scheduled time. Output: a structured brief with sections — (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time.'
    - step: 2
      title: Build Brief Delivery Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: 'Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing.'
      prompt: 'Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing.'
    - step: 3
      title: Build Prep Delivery Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: 'Create a workflow firing on meeting_scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery.'
      prompt: 'Create a workflow firing on meeting_scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery.'
    - step: 4
      title: Build Prep Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, asset, workflow]
      description: 'Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief.'
      prompt: 'Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief.'
    - step: 5
      title: Build Prep Coverage Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow, journey]
      description: 'Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed (missing data, attribute compute error).'
      prompt: 'Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed (missing data, attribute compute error).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Meeting Prep Brief

## Procedure

1. **Build Prep Brief AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute on the Meeting object called 'prep_brief'. Computed at meeting_scheduled time. Output: a structured brief with sections — (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time. → produces: attribute
2. **Build Brief Delivery Content** [`create_email_content`] — Generate an HTML email template that renders the prep_brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing. → produces: asset
3. **Build Prep Delivery Workflow** [`create_workflow`] — Create a workflow firing on meeting_scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep_brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery. → produces: workflow
4. **Build Prep Journey** [`create_journey`] — Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief. → produces: journey
5. **Build Prep Coverage Dashboard** [`create_dashboard`] — Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep_brief computation failed (missing data, attribute compute error). → produces: dashboard
