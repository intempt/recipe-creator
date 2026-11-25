---
frontmatter_id: support-tickets-vs-churn-correlation
slash_command: /support-tickets-vs-churn-correlation
description: Builds a segment of customers with recent high-priority tickets, and emails a weekly digest comparing ticket
  volume with subscription cancellations, flagging spikes and whether ticket surges come before churn.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds the high-priority ticket customers segment and emails a weekly digest of tickets against cancellations,
    with spike flags and whether ticket surges lead churn.
  parameters:
  - name: ticket_lookback
    type: duration
    label: High-priority ticket lookback for the segment
    default: 30 d
    required: false
  - name: time_range
    type: duration
    label: Weeks analyzed
    default: 12 w
    required: false
  - name: spike_threshold_pct
    type: number
    label: Rise over the trailing average that makes a ticket spike (%)
    default: 50
    required: false
  - name: trailing_window_weeks
    type: number
    label: Weeks in the trailing average
    default: 8
    required: false
  - name: churn_spike_lead_threshold_pct
    type: number
    label: Rise in tickets before a churn spike that gets flagged (%)
    default: 30
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: ticket_created_event
    kind: event
    meaning: A customer support ticket was created
    properties:
    - name: priority
      type: text
      meaning: Priority level of the ticket (e.g. P1-P4 or High/Medium/Low)
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
    properties:
    - name: reason
      type: text
      meaning: Free-text reason given for the cancellation
      optional: true
  steps:
  - id: s1
    builds: segment
    uses:
    - ticket_created_event
    - subscription_canceled_event
    - ticket_lookback
    instruction: 'Build a new segment of users named "Customers With High-Priority Tickets": users who did {ticket_created_event}
      with {ticket_created_event.priority} equal to P1, P2, High or Urgent in the last {ticket_lookback} and did not do {subscription_canceled_event}
      in the last {ticket_lookback}.'
  - id: s2
    builds: automation
    uses:
    - s1
    - ticket_created_event
    - subscription_canceled_event
    - time_range
    - spike_threshold_pct
    - trailing_window_weeks
    - churn_spike_lead_threshold_pct
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last {time_range}
      week by week and writes these figures: {ticket_created_event} count per week by {ticket_created_event.priority}; {subscription_canceled_event}
      count per week, grouped into a few reason themes from {subscription_canceled_event.reason}; weeks where high-priority
      tickets were {spike_threshold_pct}% or more above the trailing {trailing_window_weeks}-week average; for each churn
      spike week, ticket volume in the 2 weeks before against that average; whether high-priority ticket spikes came 2 to
      4 weeks before churn spikes, and which reason themes follow them; the number of users in the segment from "Find customers
      with urgent tickets". When last week was a ticket spike, or tickets before a churn spike rose more than {churn_spike_lead_threshold_pct}%,
      the email''s first line says so. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Support volume versus churn

Slash command: /support-tickets-vs-churn-correlation

## Step 1: Find customers with urgent tickets

Build a new segment of users named "Customers With High-Priority Tickets": users who did ticket created event with priority equal to P1, P2, High or Urgent in the last 30 d and did not do subscription canceled event in the last 30 d.

## Step 2: Email the weekly tickets vs churn digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 12 w week by week and writes these figures: ticket created event count per week by priority; subscription canceled event count per week, grouped into a few reason themes from reason; weeks where high-priority tickets were 50% or more above the trailing 8-week average; for each churn spike week, ticket volume in the 2 weeks before against that average; whether high-priority ticket spikes came 2 to 4 weeks before churn spikes, and which reason themes follow them; the number of users in the segment from "Find customers with urgent tickets". When last week was a ticket spike, or tickets before a churn spike rose more than 30%, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
