---
name: post-meeting-followup
description: Use when a user mentions "post-meeting follow-up", "after meeting automation", "meeting action items", or asks for related help. When a meeting completes, auto-extract AI summary + action items, update the linked deal with decisions/next-steps/objections, create tasks for each action item, and send a structured follow-up email to attendees within minutes.
arguments: []
intempt:
  id: post-meeting-followup
  version: 1.0.0
  slashCommand: /post-meeting-followup
  group: Workflows
  shortDescription: "When a meeting completes, auto-extract AI summary + action items, update the linked deal with decisions/next-steps/objections, create tasks for each action item, and send a structured follow-up email to attendees within minutes."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [post-meeting, ai-summary, crm-sync]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: meeting_completed, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_email_content
    - create_workflow
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Meeting Summary AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: 'Create an AI-derived attribute on the Meeting object called ''meeting_summary''. Computed at meeting_completed from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short.'
      prompt: 'Create an AI-derived attribute on the Meeting object called ''meeting_summary''. Computed at meeting_completed from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short.'
    - step: 2
      title: Build Follow-up Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: 'Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep''s voice based on prior outbound style if available. Send-from address: the meeting host''s email.'
      prompt: 'Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep''s voice based on prior outbound style if available. Send-from address: the meeting host''s email.'
    - step: 3
      title: Build Post-Meeting Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: 'Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack.'
      prompt: 'Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack.'
    - step: 4
      title: Build Follow-up Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, asset, workflow]
      description: 'Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt.'
      prompt: 'Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt.'
    - step: 5
      title: Build Follow-up Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow, journey]
      description: 'Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent.'
      prompt: 'Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Post Meeting Followup

## Procedure

1. **Build Meeting Summary AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute on the Meeting object called 'meeting_summary'. Computed at meeting_completed from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short. → produces: attribute
2. **Build Follow-up Email Content** [`create_email_content`] — Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep's voice based on prior outbound style if available. Send-from address: the meeting host's email. → produces: asset
3. **Build Post-Meeting Workflow** [`create_workflow`] — Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack. → produces: workflow
4. **Build Follow-up Journey** [`create_journey`] — Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt. → produces: journey
5. **Build Follow-up Performance Dashboard** [`create_dashboard`] — Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent. → produces: dashboard
