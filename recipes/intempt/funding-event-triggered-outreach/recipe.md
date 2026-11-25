---
frontmatter_id: funding-event-triggered-outreach
slash_command: /funding-event-triggered-outreach
description: Catches an account raising money, drafts a congratulations with a budget angle, puts it on the AE with a task
  to act within a day, and emails the sales team.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: When an account announces a funding round, drafts a congratulations email for the AE to review, gives the AE a
    task to reach out within a day, and emails the sales team.
  parameters:
  - name: sla_hours
    type: number
    label: AE outreach SLA (hours after funding announcement)
    default: 24
    required: false
  - name: task_priority
    type: enum
    label: Task priority
    default: high
    required: false
    options:
    - high
    - medium
    - low
  - name: signal_window
    type: duration
    label: Window in which funding signal is most valuable
    default: 14 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the sales team that gets funding alerts
    required: true
  requirements:
  - slot: funding_event
    kind: event
    meaning: A target account announced a funding round
    properties:
    - name: company_domain
      type: string
      meaning: Web domain of the company that raised funds
      optional: false
    - name: round_type
      type: string
      meaning: Funding round stage such as seed, A, B, or C
      optional: false
    - name: amount_raised
      type: string
      meaning: Amount of money raised in the round
      optional: false
    - name: investors
      type: text
      meaning: Names of investors in the round
      optional: true
    - name: announcement_date
      type: date
      meaning: Date the round was announced
      optional: false
  - slot: account_owner
    kind: attribute
    meaning: The AE who owns the account or territory assignment rules for unassigned accounts
  steps:
  - id: s1
    builds: email
    uses:
    - funding_event
    instruction: Write a short congratulations email from an AE to a decision-maker at a company that just announced a funding
      round. It names the round {funding_event.round_type} and the amount {funding_event.amount_raised}, names {funding_event.investors}
      when present, ties one way we help teams that are growing after a raise to that stage, and ends with a soft request
      for a 20-minute call. No prices.
  - id: s2
    builds: task
    uses:
    - s1
    - funding_event
    - account_owner
    - task_priority
    - sla_hours
    - signal_window
    dependsOn:
    - s1
    instruction: 'For each account that did {funding_event}, create a task for its {account_owner} with priority {task_priority},
      due {sla_hours} hours after {funding_event.announcement_date}: reach out about the {funding_event.round_type} round
      of {funding_event.amount_raised} using the email from "Draft the congratulations", within the {signal_window} after
      the announcement.'
  - id: s3
    builds: automation
    uses:
    - funding_event
    - account_owner
    - sla_hours
    - alert_recipients
    instruction: 'Build an automation triggered when an account does {funding_event}. It emails {alert_recipients} one line
      per event: the account name, {funding_event.company_domain}, {funding_event.round_type}, {funding_event.amount_raised},
      {funding_event.announcement_date}, the AE from {account_owner}, and that outreach is due within {sla_hours} hours.'
---

# Outreach on a funding round

Slash command: /funding-event-triggered-outreach

## Step 1: Draft the congratulations

Write a short congratulations email from an AE to a decision-maker at a company that just announced a funding round. It names the round round type and the amount amount raised, names investors when present, ties one way we help teams that are growing after a raise to that stage, and ends with a soft request for a 20-minute call. No prices.

## Step 2: Put it on an AE within a day

For each account that did funding event, create a task for its account owner with priority high, due 24 hours after announcement date: reach out about the round type round of amount raised using the email from "Draft the congratulations", within the 14 d after the announcement.

## Step 3: Alert the sales team

Build an automation triggered when an account does funding event. It emails the email addresses of the sales team that gets funding alerts one line per event: the account name, company domain, round type, amount raised, announcement date, the AE from account owner, and that outreach is due within 24 hours.
