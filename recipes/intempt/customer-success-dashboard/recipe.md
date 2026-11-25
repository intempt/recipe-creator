---
frontmatter_id: customer-success-dashboard
slash_command: /customer-success-dashboard
description: Flags accounts whose product use is dropping or whose support load is rising, and emails customer success a weekly
  digest of at-risk accounts, retention, NPS and early churn signals.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds an at-risk accounts segment and emails customer success a weekly digest of at-risk accounts, account retention,
    NPS, engagement movers and tickets against cancellations.
  parameters:
  - name: usageDropPct
    type: number
    label: Drop in sessions that makes an account at risk (%)
    default: 30
    required: false
  - name: ticketThreshold
    type: number
    label: Support tickets in 30 days that make an account at risk
    default: 3
    required: false
  - name: npsSurveyType
    type: string
    label: Survey type value of NPS answers
    default: nps
    required: false
  - name: topAccountCount
    type: number
    label: Accounts listed as rising and falling
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: ticket_created_event
    kind: event
    meaning: A customer created a support ticket
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  - slot: feedback_submitted_event
    kind: event
    meaning: A customer answered a feedback survey, including NPS
    properties:
    - name: survey_type
      type: string
      meaning: Kind of survey, such as nps
      optional: false
    - name: score
      type: number
      meaning: The 0-10 rating given
      optional: false
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start_event
    - ticket_created_event
    - usageDropPct
    - ticketThreshold
    instruction: 'Build a new segment of accounts named "Accounts at Risk of Churn". An account is in it when either is true:
      (a) the number of {session_start_event} events by its users in the last 14 days is at least {usageDropPct}% lower than
      in the 14 days before that; (b) its users did {ticket_created_event} {ticketThreshold} or more times in the last 30
      days.'
  - id: s2
    builds: automation
    uses:
    - s1
    - session_start_event
    - ticket_created_event
    - subscription_canceled_event
    - feedback_submitted_event
    - npsSurveyType
    - topAccountCount
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts and writes
      these figures: the number of accounts in the segment from "Find accounts at risk" now and 7 days ago; account retention,
      the share of accounts active 30 to 60 days ago that did not do {subscription_canceled_event} in the last 30 days; NPS
      over the last 90 days from {feedback_submitted_event} where {feedback_submitted_event.survey_type} is {npsSurveyType},
      as % of scores 9-10 minus % of scores 0-6; the {topAccountCount} accounts with the largest rise and the {topAccountCount}
      with the largest fall in {session_start_event} count this week against last week, each by name; {ticket_created_event}
      and {subscription_canceled_event} counts per week for the last 8 weeks. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Account health and churn risk

Slash command: /customer-success-dashboard

## Step 1: Find accounts at risk

Build a new segment of accounts named "Accounts at Risk of Churn". An account is in it when either is true: (a) the number of session start event events by its users in the last 14 days is at least 30% lower than in the 14 days before that; (b) its users did ticket created event 3 or more times in the last 30 days.

## Step 2: Email the weekly account health digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts and writes these figures: the number of accounts in the segment from "Find accounts at risk" now and 7 days ago; account retention, the share of accounts active 30 to 60 days ago that did not do subscription canceled event in the last 30 days; NPS over the last 90 days from feedback submitted event where survey type is nps, as % of scores 9-10 minus % of scores 0-6; the 10 accounts with the largest rise and the 10 with the largest fall in session start event count this week against last week, each by name; ticket created event and subscription canceled event counts per week for the last 8 weeks. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
