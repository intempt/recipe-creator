---
description: Builds a post-meeting follow-up journey that creates tasks with owners and due dates from action items you provide, and can send a structured follow-up email to attendees.
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

# Post meeting follow up

Slash command: /post-meeting-followup

## Step 1: Pull the meeting apart

Create an AI-derived attribute on the Meeting object called 'meeting_summary'. Computed at meeting_completed from the transcript. Output: structured object with (a) one-paragraph executive summary; (b) decisions reached (list); (c) action items (list of {assignee, due, description}); (d) objections raised (list); (e) sentiment score; (f) next step proposed (free-text). Falls back to gracefully partial output if transcript is incomplete or short.

## Step 2: Write the recap email

Generate a follow-up email template that renders the meeting_summary attribute. Structure: thank-you opening referencing meeting subject and attendees, recap of decisions, bulleted action items with owners and due dates, link to recording if available, signature with proposed next step and a scheduling link. Tone: professional but warm; reflects the rep's voice based on prior outbound style if available. Send-from address: the meeting host's email. Use the result of "Pull the meeting apart".

## Step 3: File it and raise the tasks

Create a workflow firing on meeting_completed. Step sequence: (1) compute meeting_summary attribute; (2) update the linked deal record with the AI-extracted next step, objections, sentiment, and the meeting note; (3) for each action item in the summary, create a CRM task assigned to the named owner with the due date; (4) trigger the follow-up journey to send the recap email. If meeting_summary computation fails (no transcript, processing error), still create a task for the host to manually follow up and notify them via Slack. Use the result of "Pull the meeting apart", "Write the recap email".

## Step 4: Send it within 30 minutes

Build a 1-touch journey that sends the follow-up email to all meeting attendees (excluding internal users) within 30 minutes of meeting_completed, when triggered by the post-meeting workflow. Personalize per attendee: the body stays the same but the salutation and signature adapt. Use the result of "Pull the meeting apart", "Write the recap email", "File it and raise the tasks".

## Step 5: Check nothing goes unanswered

Compose a dashboard tracking post-meeting follow-up health: median time from meeting_completed to follow-up email sent (target: under 30 min), % of meetings with completed follow-ups vs missed, action-item completion rate (tasks created vs tasks completed), and reply rate to follow-up emails. Break down by meeting type and rep. Flag any meeting older than 4 hours without a follow-up sent. Use the result of "Pull the meeting apart", "Write the recap email", "File it and raise the tasks", "Send it within 30 minutes".
