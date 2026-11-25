---
frontmatter_id: sales-activity-coaching-dashboard
slash_command: /sales-activity-coaching-dashboard
description: Emails sales managers a weekly per-rep digest of calls, emails and meetings next to the revenue they produced,
  so managers can spot coaching needs and performance gaps before weekly 1:1s.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails sales managers a weekly per-rep digest of calls, outbound emails, meetings and won revenue, with revenue
    per 100 calls and reps whose activity is rising or falling.
  parameters:
  - name: efficiencyAlertRatio
    type: number
    label: Share of the team's revenue per 100 calls below which a rep is flagged
    default: 0.5
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: call_completed
    kind: event
    meaning: A rep completed a call with a prospect or customer
    properties:
    - name: owner_id
      type: string
      meaning: The rep who made the call
      optional: false
  - slot: email_sent_outbound
    kind: event
    meaning: A rep sent an outbound email to a prospect or customer
    properties:
    - name: owner_id
      type: string
      meaning: The rep who sent it
      optional: false
  - slot: meeting_scheduled
    kind: event
    meaning: A rep scheduled a meeting with a prospect or customer
    properties:
    - name: owner_id
      type: string
      meaning: The rep who booked it
      optional: false
  - slot: deal_won
    kind: event
    meaning: A deal was marked won
    properties:
    - name: owner_id
      type: string
      meaning: The rep who owns the deal
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - call_completed
    - email_sent_outbound
    - meeting_scheduled
    - deal_won
    - efficiencyAlertRatio
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes rep activity per
      owner_id and writes these figures: per rep, the count of {call_completed}, {email_sent_outbound} and {meeting_scheduled}
      in the last 7 days against the 7 days before; per rep, the count of {deal_won} and the sum of {deal_won.amount} in the
      last 30 days; per rep, revenue per 100 calls over the last 30 days against the team average, marking every rep below
      {efficiencyAlertRatio} times the team average; team totals of calls, meetings and won revenue for the last 30 days;
      the 3 reps with the largest rise and the 3 with the largest fall in calls plus meetings this week against last week.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Rep activity and coaching

Slash command: /sales-activity-coaching-dashboard

## Step 1: Email the weekly rep coaching digest

Build an automation that runs every Monday at 07:00 on a schedule. Each run it analyzes rep activity per owner_id and writes these figures: per rep, the count of call completed, email sent outbound and meeting scheduled in the last 7 days against the 7 days before; per rep, the count of deal won and the sum of amount in the last 30 days; per rep, revenue per 100 calls over the last 30 days against the team average, marking every rep below 0.5 times the team average; team totals of calls, meetings and won revenue for the last 30 days; the 3 reps with the largest rise and the 3 with the largest fall in calls plus meetings this week against last week. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
