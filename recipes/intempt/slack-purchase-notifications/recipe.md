---
frontmatter_id: slack-purchase-notifications
slash_command: /slack-purchase-notifications
description: Emails revenue wins to one group and at-risk events such as failed payments, cancellations and large abandoned
  carts to another, holding routine alerts during quiet hours.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails each revenue win to the wins list and each failed payment, cancellation or large abandoned cart to the revenue-ops
    list.
  parameters:
  - name: wins_recipients
    type: string
    label: Email addresses that get revenue wins
    required: true
  - name: ops_recipients
    type: string
    label: Email addresses that get at-risk alerts
    required: true
  - name: highValueThreshold
    type: number
    label: Order or cart value at or above which an event is alerted
    default: 1000
    required: false
  - name: quietHoursStart
    type: string
    label: Start of quiet hours (HH:MM)
    default: '20:00'
    required: false
  - name: quietHoursEnd
    type: string
    label: End of quiet hours (HH:MM)
    default: 08:00
    required: false
  requirements:
  - slot: revenue_won_event
    kind: event
    meaning: A deal was won, a subscription started, an order was placed, or an expansion closed
    properties:
    - name: rep_name
      type: string
      meaning: Rep who closed the deal
      optional: true
    - name: account_name
      type: string
      meaning: Customer or account name
      optional: false
    - name: arr
      type: number
      meaning: Annual recurring revenue of the deal
      optional: true
    - name: order_value
      type: number
      meaning: Value of the order
      optional: true
  - slot: revenue_problem_event
    kind: event
    meaning: A payment failed, a subscription was canceled, or a high-value cart was abandoned
    properties:
    - name: customer_name
      type: string
      meaning: Customer name
      optional: false
    - name: plan
      type: string
      meaning: Customer's plan
      optional: true
    - name: mrr_at_risk
      type: number
      meaning: Monthly revenue at risk
      optional: true
    - name: cancel_reason
      type: string
      meaning: Reason given for cancelling
      optional: true
    - name: cart_value
      type: number
      meaning: Value of the abandoned cart
      optional: true
  - slot: csm_owner
    kind: attribute
    meaning: Name of the customer success manager assigned to the account
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - revenue_won_event
    - highValueThreshold
    - quietHoursStart
    - quietHoursEnd
    - wins_recipients
    instruction: Build an automation that starts when a user does {revenue_won_event}. It continues only when {revenue_won_event.arr}
      is set, or {revenue_won_event.order_value} is {highValueThreshold} or more. If the event happens between {quietHoursStart}
      and {quietHoursEnd}, it waits until {quietHoursEnd}. Then it emails {wins_recipients} one short, celebratory plain-text
      line with {revenue_won_event.account_name}, {revenue_won_event.rep_name}, and {revenue_won_event.arr} or {revenue_won_event.order_value}.
  - id: s2
    builds: automation
    uses:
    - revenue_problem_event
    - csm_owner
    - highValueThreshold
    - ops_recipients
    instruction: Build an automation that starts when a user does {revenue_problem_event}. When {revenue_problem_event.cart_value}
      is set it continues only if it is {highValueThreshold} or more. Then it emails {ops_recipients} one terse, action-first
      plain-text alert with {revenue_problem_event.customer_name}, {revenue_problem_event.plan}, {revenue_problem_event.mrr_at_risk},
      {revenue_problem_event.cancel_reason} or {revenue_problem_event.cart_value} when set, and the account's {csm_owner}
      as the person to respond. Alerts are sent at any hour.
---

# Revenue win and risk alerts

Slash command: /slack-purchase-notifications

## Step 1: Route wins to the wins list

Build an automation that starts when a user does revenue won event. It continues only when arr is set, or order value is 1000 or more. If the event happens between 20:00 and 08:00, it waits until 08:00. Then it emails the email addresses that get revenue wins one short, celebratory plain-text line with account name, rep name, and arr or order value.

## Step 2: Route problems to revenue ops

Build an automation that starts when a user does revenue problem event. When cart value is set it continues only if it is 1000 or more. Then it emails the email addresses that get at-risk alerts one terse, action-first plain-text alert with customer name, plan, mrr at risk, cancel reason or cart value when set, and the account's csm owner as the person to respond. Alerts are sent at any hour.
