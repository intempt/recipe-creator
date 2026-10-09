---
name: meeting-prep-brief
description: Use when a user mentions "meeting prep brief", "pre-meeting brief", "AE prep document", or asks for related help. When a meeting is scheduled, auto-generate an AE prep brief 24 hours before the meeting (stakeholder map, prior touches, account health, suggested talking points) delivered to the host via email or Slack.
arguments: []
intempt:
  id: meeting-prep-brief
  title: "Meeting prep brief"
  version: 1.0.0
  slashCommand: /meeting-prep-brief
  group: Workflows
  shortDescription: "Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every prior touch, and what to talk about."
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
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Assemble the brief"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "Built when the meeting is booked: the attendees with their titles, their role on the deal and their recent activity, the account's revenue, plan, health score and open opportunities, the last five interactions across email, meetings and support, talking points drawn from the deal stage, recent product usage and any open tickets, and any competitive flags. It rebuilds if an attendee is added within an hour of the meeting."
      prompt: 'Create an AI-derived attribute on the Meeting object called ''prep brief''. Computed when the meeting is scheduled. Output: a structured brief with sections: (a) attendees: name, title, role on deal, recent activity; (b) account snapshot: ARR, plan, health score, open opportunities; (c) prior touch history: last 5 interactions across email/meetings/support; (d) suggested talking points: AI-derived from deal stage, recent product usage, and any open support tickets; (e) competitive intel: if any flag exists. Refreshes if a new attendee is added within 1 hour of meeting time.'
    - step: 2
      title: "Lay it out to be skimmed"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: "An email with the meeting details at the top, then sections for the account, previous touches, talking points and competitive notes, plus a button to open the brief in the app. Plain and useful, not marketing."
      prompt: 'Generate an HTML email template that renders the prep brief attribute in a clean, scannable layout. Sections: meeting summary at top (date, time, duration, attendees), then collapsible sections for account, prior touches, talking points, competitive intel. Include a CTA button to view the brief in the app. Tone: utilitarian, not marketing.'
    - step: 3
      title: "Send it a day before"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: "On booking, delivery is scheduled for 24 hours before the meeting, or straight away if the meeting is sooner than that. The brief is rebuilt just before it goes, so late changes are included. A reschedule moves the delivery and a cancellation stops it."
      prompt: 'Create a workflow firing on Meeting scheduled. Schedule a delayed step to fire 24 hours before the meeting (or immediately if the meeting is within 24 hours). On firing: re-compute the prep brief attribute (catches any last-minute updates), then trigger the brief journey to deliver to the host. If the meeting is rescheduled, cancel the pending delivery and re-schedule. If cancelled, suppress delivery.'
    - step: 4
      title: "Deliver it to the host"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, asset, workflow]
      description: "One message to the host, not the attendees. Email by default, or a Slack message with a link if Slack is connected and the host has an ID there."
      prompt: 'Build a 1-touch journey that sends the prep-brief email to the meeting host when triggered by the prep delivery workflow. Audience: the meeting host (not the attendees). Channel: email by default; if a Slack integration is connected and the host has a Slack ID, prefer Slack DM with a link to the brief.'
    - step: 5
      title: "Check every meeting got one"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow, journey]
      description: "The share of meetings where a brief was actually delivered, how long before the meeting it went, and how often hosts open it, broken out by meeting type. Any meeting where the brief could not be built, for missing data or an error, is flagged."
      prompt: 'Compose a dashboard tracking prep-brief coverage: % of meetings where a brief was delivered, median time before meeting the brief was sent, and host open rate on brief emails. Break down by meeting type (demo, discovery, expansion, renewal). Flag any meetings where prep brief computation failed (missing data, attribute compute error).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Meeting prep brief

Sends the host a brief 24 hours before a meeting: who is coming, how the account is doing, every prior touch, and what to talk about.

## Before you run it

- Connect slack
- Send the `meeting_scheduled` event

## What it does

1. **Assemble the brief** (`create_ai_attribute`)

   Built when the meeting is booked: the attendees with their titles, their role on the deal and their recent activity, the account's revenue, plan, health score and open opportunities, the last five interactions across email, meetings and support, talking points drawn from the deal stage, recent product usage and any open tickets, and any competitive flags. It rebuilds if an attendee is added within an hour of the meeting.

2. **Lay it out to be skimmed** (`create_email_content`)

   An email with the meeting details at the top, then sections for the account, previous touches, talking points and competitive notes, plus a button to open the brief in the app. Plain and useful, not marketing.

3. **Send it a day before** (`create_workflow`)

   On booking, delivery is scheduled for 24 hours before the meeting, or straight away if the meeting is sooner than that. The brief is rebuilt just before it goes, so late changes are included. A reschedule moves the delivery and a cancellation stops it.

4. **Deliver it to the host** (`create_journey`)

   One message to the host, not the attendees. Email by default, or a Slack message with a link if Slack is connected and the host has an ID there.

5. **Check every meeting got one** (`create_dashboard`)

   The share of meetings where a brief was actually delivered, how long before the meeting it went, and how often hosts open it, broken out by meeting type. Any meeting where the brief could not be built, for missing data or an error, is flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
