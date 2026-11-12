---
frontmatter_id: slack-purchase-notifications
slash_command: /slack-purchase-notifications
description: Posts revenue wins to one Slack channel and at-risk events to another through a configurable workflow. Notifications are static channel posts, with no dynamic owner mentions or DMs.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Posts revenue wins to a wins Slack channel and payment, cancellation, and cart alerts to a revenue-ops channel,
    with static posts and no personal mentions or DMs.
  parameters:
  - name: winsChannel
    type: string
    label: Slack channel for revenue wins
    default: '#wins'
  - name: opsChannel
    type: string
    label: Slack channel for operational alerts
    default: '#revenue-ops'
  - name: highValueThreshold
    type: number
    label: High-value ARR threshold (top quartile, configurable)
    default: 0
  - name: largeOrderPercentile
    type: number
    label: Large-order threshold percentile of order values
    default: 95
  - name: quietHoursStart
    type: string
    label: Off-hours start (quiet period begins)
    default: '20:00'
  - name: quietHoursEnd
    type: string
    label: Off-hours end (quiet period ends)
    default: 08:00
  - name: celebrationTone
    type: enum
    label: Tone of celebration posts
    default: warm
    options:
    - warm
    - neutral
    - formal
  - name: alertTone
    type: enum
    label: Tone of operational alerts
    default: terse
    options:
    - terse
    - neutral
    - formal
  requirements:
  - slot: revenue_won_event
    kind: event
    meaning: A deal was won, a subscription started, an order was placed, or an expansion closed
    properties:
    - name: rep_name
      type: text
      meaning: Name of the rep who closed the deal
      optional: true
    - name: account_name
      type: text
      meaning: Customer account name
      optional: false
    - name: arr
      type: number
      meaning: Annual recurring revenue of the deal
      optional: false
    - name: contract_length
      type: number
      meaning: Contract length in months
      optional: true
    - name: order_value
      type: number
      meaning: Order value for ecommerce orders
      optional: true
    - name: upsell_amount
      type: number
      meaning: Expansion amount
      optional: true
  - slot: revenue_problem_event
    kind: event
    meaning: A payment failed, a subscription was canceled, or a high-value cart was abandoned
    properties:
    - name: customer_name
      type: text
      meaning: Customer name
      optional: false
    - name: plan
      type: text
      meaning: Subscription plan
      optional: true
    - name: mrr_at_risk
      type: number
      meaning: Monthly recurring revenue at risk
      optional: true
    - name: cancel_reason
      type: text
      meaning: Reason given for cancellation
      optional: true
    - name: cart_value
      type: number
      meaning: Abandoned cart value
      optional: true
  - slot: csm_owner
    kind: attribute
    meaning: The customer success manager assigned to an account
    optional: true
  - slot: ae_manager
    kind: attribute
    meaning: The account executive manager of the rep who closed a deal
    optional: true
  - slot: slack_workspace
    kind: integration
    meaning: A connected Slack workspace where the bot can post to channels
    channel: slack
  steps:
  - id: s1
    builds: content
    uses:
    - revenue_won_event
    - celebrationTone
    - largeOrderPercentile
    instruction: 'Write Slack celebration post content in a {celebrationTone} tone, brief and team-celebratory. Variants:
      (a) Deal won: include rep name, account, ARR, and contract length, with a 🎉 emoji and a team mention. (b) Subscription
      started (B2B): the first paying customer of the month gets a fanfare message; subsequent ones get a compact one-liner.
      (c) Ecommerce order placed: only orders at or above the {largeOrderPercentile} percentile of order values get a celebration;
      normal orders stay silent. (d) Expansion: include upsell amount, customer name, and the AE who closed the deal. Use
      fields from {revenue_won_event}.'
  - id: s2
    builds: content
    uses:
    - revenue_problem_event
    - csm_owner
    - alertTone
    - highValueThreshold
    instruction: 'Write Slack operational alert content in a {alertTone} tone, action-oriented, with clear who-needs-to-respond.
      Variants: (a) Payment failed: customer name, plan, MRR at risk, and a CSM owner mention from {csm_owner}. (b) Subscription
      canceled: include the cancellation reason. (c) High-value abandoned cart (B2C): a single cart value above {highValueThreshold}
      triggers the alert. Use fields from {revenue_problem_event}.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - revenue_won_event
    - revenue_problem_event
    - winsChannel
    - opsChannel
    - highValueThreshold
    - quietHoursStart
    - quietHoursEnd
    - ae_manager
    - slack_workspace
    instruction: 'Create a workflow that fires on {revenue_won_event} and {revenue_problem_event}. Step 1: classify the event
      as celebration (won, created, expansion) or operational (failed, canceled, at-risk). Step 2: for celebrations, post
      the content from "Write the celebration posts" to {winsChannel} with deal and account context. Step 3: for operational
      events, post the content from "Write the operational alerts" to {opsChannel} with a CSM or rep mention. Step 4: for
      events at or above {highValueThreshold} ARR (top quartile), also send a direct message to the CEO or CRO and the {ae_manager}.
      Step 5: between {quietHoursStart} and {quietHoursEnd}, suppress notifications unless the event is explicitly tagged
      urgent, so routine wins never ping the team overnight. Post all messages as static channel posts with no dynamic owner
      mentions in the channel.'
---

# Revenue notifications in Slack

Slash command: /slack-purchase-notifications

## Step 1: Write the celebration posts

Generate Slack message content for revenue celebrations. Variants: (a) Deal won (include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) Subscription started (B2B)) first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) (large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion) upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.

## Step 2: Write the operational alerts

Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) Payment failed: customer name, plan, MRR at risk, CSM owner @mention; (b) Subscription canceled with reason; (c) high-value-Abandoned cart (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear.

## Step 3: Route wins and problems apart

Create a workflow firing on revenue events. Step sequence: (1) classify event type: celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don't ping the team at 2am for routine wins). Use the result of "Write the celebration posts", "Write the operational alerts".
