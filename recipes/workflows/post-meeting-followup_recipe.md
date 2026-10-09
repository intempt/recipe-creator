---
name: post-meeting-followup
description: Use when a user mentions "post-meeting follow-up", "after meeting automation", "meeting action items", or asks for related help. When a meeting completes, auto-extract AI summary + action items, update the linked deal with decisions/next-steps/objections, create tasks for each action item, and send a structured follow-up email to attendees within minutes.
arguments: []
intempt:
  id: post-meeting-followup
  title: "Post meeting follow up"
  version: 1.0.0
  slashCommand: /post-meeting-followup
  group: Workflows
  shortDescription: "Turns a finished call into a recap email, a set of tasks with owners and due dates, and an updated deal, inside half an hour."
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
    integrations:
      - { value: slack, severity: recommended }
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
      title: "Pull the meeting apart"
      command: create_ai_attribute
      produces: attribute
      bindsAs: attribute
      description: "From the transcript once the meeting ends: a one paragraph summary, the decisions reached, the action items with an owner and a due date each, the objections raised, a sentiment score and the next step proposed. A short or incomplete transcript still yields what it can."
      prompt: 'Create an AI-derived attribute on the Meeting object called ''meeting summary''. Computed when the meeting completes, from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short.'
    - step: 2
      title: "Write the recap email"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [attribute]
      description: "It thanks them, names the subject and who was there, recaps the decisions, lists the action items with owners and dates, links the recording where there is one, and closes with the proposed next step and a scheduling link. It comes from the host and matches their usual tone."
      prompt: 'Generate a follow-up email template that renders the meeting summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep''s voice based on prior outbound style if available. Send-from address: the meeting host''s email.'
    - step: 3
      title: "File it and raise the tasks"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn: [attribute, asset]
      description: "When the meeting completes it builds the summary, writes the next step, objections, sentiment and notes onto the deal, creates a task for every action item against its named owner and due date, and triggers the recap email. If the summary cannot be built it still creates a task for the host to follow up by hand and tells them in Slack."
      prompt: 'Create a workflow firing on Meeting completed. Step sequence: (1) compute the meeting summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If the meeting summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack.'
    - step: 4
      title: "Send it within 30 minutes"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [attribute, asset, workflow]
      description: "One email to every external attendee within half an hour of the meeting ending. The body is the same for everyone, with the greeting and signature adapted."
      prompt: 'Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of Meeting completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt.'
    - step: 5
      title: "Check nothing goes unanswered"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [attribute, asset, workflow, journey]
      description: "The median time from the meeting ending to the email going out against a 30 minute target, how many meetings got a follow up and how many did not, how many action items are completed, and the reply rate, broken out by meeting type and rep, with anything over four hours without a follow up flagged."
      prompt: 'Compose a dashboard tracking post-meeting follow-up health: median time from Meeting completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Post meeting follow up

Turns a finished call into a recap email, a set of tasks with owners and due dates, and an updated deal, inside half an hour.

## Before you run it

- Connect slack
- Send the `meeting_completed` event

## What it does

1. **Pull the meeting apart** (`create_ai_attribute`)

   From the transcript once the meeting ends: a one paragraph summary, the decisions reached, the action items with an owner and a due date each, the objections raised, a sentiment score and the next step proposed. A short or incomplete transcript still yields what it can.

2. **Write the recap email** (`create_email_content`)

   It thanks them, names the subject and who was there, recaps the decisions, lists the action items with owners and dates, links the recording where there is one, and closes with the proposed next step and a scheduling link. It comes from the host and matches their usual tone.

3. **File it and raise the tasks** (`create_workflow`)

   When the meeting completes it builds the summary, writes the next step, objections, sentiment and notes onto the deal, creates a task for every action item against its named owner and due date, and triggers the recap email. If the summary cannot be built it still creates a task for the host to follow up by hand and tells them in Slack.

4. **Send it within 30 minutes** (`create_journey`)

   One email to every external attendee within half an hour of the meeting ending. The body is the same for everyone, with the greeting and signature adapted.

5. **Check nothing goes unanswered** (`create_dashboard`)

   The median time from the meeting ending to the email going out against a 30 minute target, how many meetings got a follow up and how many did not, how many action items are completed, and the reply rate, broken out by meeting type and rep, with anything over four hours without a follow up flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
