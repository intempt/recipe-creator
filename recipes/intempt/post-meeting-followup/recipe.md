---
id: post-meeting-followup
title: Post meeting follow up
slash_command: /post-meeting-followup
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Builds a post-meeting follow-up journey that creates tasks with owners and due dates from action items you
  provide, and can send a structured follow-up email to attendees.
description: >-
  When a meeting completes, use the workflow and journey to turn action items you supply into assigned tasks
  with due dates, send a follow-up email, and track progress on a dashboard. It does not generate meeting
  summaries from transcripts.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - post-meeting
    - ai-summary
    - crm-sync
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: meeting_completed
      severity: blocking
touches:
  reads:
    - The meeting_completed event in your project
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Pull the meeting apart"
    - A new designed email, from step 2 "Write the recap email"
    - A new workflow, from step 3 "File it and raise the tasks"
    - A new journey, from step 4 "Send it within 30 minutes"
    - A new dashboard, from step 5 "Check nothing goes unanswered"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Pull the meeting apart
    summary: >-
      From the transcript once the meeting ends: a one paragraph summary, the decisions reached, the action
      items with an owner and a due date each, the objections raised, a sentiment score and the next step
      proposed. A short or incomplete transcript still yields what it can.
    builds: attribute
    description: >-
      Create an AI-derived attribute on the Meeting object called 'meeting_summary'. Computed at meeting_completed
      from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions
      reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list);
      (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output
      if transcript is incomplete or short.
  - id: s2
    title: Write the recap email
    summary: >-
      It thanks them, names the subject and who was there, recaps the decisions, lists the action items
      with owners and dates, links the recording where there is one, and closes with the proposed next
      step and a scheduling link. It comes from the host and matches their usual tone.
    builds: email_html
    description: >-
      Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you
      opening referencing meeting subject and attendees, recap of decisions, bulleted action items with
      owners and due dates, link to recording if available, signature with proposed next step and a scheduling
      link. Tone: professional but warm; reflects the rep's voice based on prior outbound style if available.
      Send-from address: the meeting host's email. Use the result of "Pull the meeting apart".
    dependsOn:
      - s1
  - id: s3
    title: File it and raise the tasks
    summary: >-
      When the meeting completes it builds the summary, writes the next step, objections, sentiment and
      notes onto the deal, creates a task for every action item against its named owner and due date,
      and triggers the recap email. If the summary cannot be built it still creates a task for the host
      to follow up by hand and tells them in Slack.
    builds: workflow
    description: >-
      Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute;
      (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the
      meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner
      with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary
      computation fails (no transcript, processing error), still create a task for the host to manually
      follow up and notify them via Slack. Use the result of "Pull the meeting apart", "Write the recap
      email".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Send it within 30 minutes
    summary: >-
      One email to every external attendee within half an hour of the meeting ending. The body is the
      same for everyone, with the greeting and signature adapted.
    builds: journey
    description: >-
      Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal
      users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize
      per attendee: the body stays the same but the salutation and signature adapt. Use the result of
      "Pull the meeting apart", "Write the recap email", "File it and raise the tasks".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Check nothing goes unanswered
    summary: >-
      The median time from the meeting ending to the email going out against a 30 minute target, how many
      meetings got a follow up and how many did not, how many action items are completed, and the reply
      rate, broken out by meeting type and rep, with anything over four hours without a follow up flagged.
    builds: dashboard
    description: >-
      Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to
      follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed,
      action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails.
      Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent.
      Use the result of "Pull the meeting apart", "Write the recap email", "File it and raise the tasks",
      "Send it within 30 minutes".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Post meeting follow up

Builds a post-meeting follow-up journey that creates tasks with owners and due dates from action items you provide, and can send a structured follow-up email to attendees.

## Steps

1. **Pull the meeting apart** (builds attribute)

   From the transcript once the meeting ends: a one paragraph summary, the decisions reached, the action items with an owner and a due date each, the objections raised, a sentiment score and the next step proposed. A short or incomplete transcript still yields what it can.

2. **Write the recap email** (builds email_html)

   It thanks them, names the subject and who was there, recaps the decisions, lists the action items with owners and dates, links the recording where there is one, and closes with the proposed next step and a scheduling link. It comes from the host and matches their usual tone.

3. **File it and raise the tasks** (builds workflow)

   When the meeting completes it builds the summary, writes the next step, objections, sentiment and notes onto the deal, creates a task for every action item against its named owner and due date, and triggers the recap email. If the summary cannot be built it still creates a task for the host to follow up by hand and tells them in Slack.

4. **Send it within 30 minutes** (builds journey)

   One email to every external attendee within half an hour of the meeting ending. The body is the same for everyone, with the greeting and signature adapted.

5. **Check nothing goes unanswered** (builds dashboard)

   The median time from the meeting ending to the email going out against a 30 minute target, how many meetings got a follow up and how many did not, how many action items are completed, and the reply rate, broken out by meeting type and rep, with anything over four hours without a follow up flagged.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The meeting_completed event in your project
- Your Slack connection

Writes:

- A new attribute, from step 1 "Pull the meeting apart"
- A new designed email, from step 2 "Write the recap email"
- A new workflow, from step 3 "File it and raise the tasks"
- A new journey, from step 4 "Send it within 30 minutes"
- A new dashboard, from step 5 "Check nothing goes unanswered"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
