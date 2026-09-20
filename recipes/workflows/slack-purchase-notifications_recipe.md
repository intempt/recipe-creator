---
name: slack-purchase-notifications
description: Use when a user mentions "slack purchase notifications", "revenue celebrations", "deal-won slack alert", or asks for related help. Post celebration-grade Slack messages on key revenue events (deal_won, new subscription, expansion) and operational Slack messages on at-risk events (payment_failed, churn). Single configurable workflow handling the Slack revenue-notifications surface.
arguments: []
intempt:
  id: slack-purchase-notifications
  title: "Revenue notifications in Slack"
  version: 1.0.0
  slashCommand: /slack-purchase-notifications
  group: Workflows
  shortDescription: "Posts the wins to one channel and the problems to another, with the person who needs to act tagged, and stays quiet outside working hours."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas, ecommerce]
    complexity: standard
    executionMode: live
    tags: [slack-notifications, revenue-events]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: deal_won, severity: blocking }
      - { value: subscription_created, severity: blocking }
      - { value: order_placed, severity: recommended }
    integrations:
      - { value: slack, severity: blocking }
  invokesCommands:
    - create_slack_content
    - create_workflow
  procedure:
    - step: 1
      title: "Write the celebration posts"
      command: create_slack_content
      produces: asset
      bindsAs: celebration_asset
      description: "A won deal names the rep, the account, the ARR and the contract length and tags the team. The first new B2B subscription of the month gets a fanfare and the rest a one liner. An ecommerce order only gets a post if it is in the top 5% by value. An upsell names the amount, the customer and the AE. Warm and brief."
      prompt: 'Generate Slack message content for revenue celebrations. Variants: (a) deal_won (include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B)) first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) (large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion) upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.'
    - step: 2
      title: "Write the operational alerts"
      command: create_slack_content
      produces: asset
      bindsAs: alert_asset
      description: "For a different channel: a failed payment with the customer, the plan, the revenue at risk and the CSM tagged, a cancellation with its reason, and an unusually large abandoned cart. Terse, and clear about who has to act."
      prompt: 'Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) payment_failed: customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear.'
    - step: 3
      title: "Route wins and problems apart"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - celebration_asset
      - alert_asset
      description: "On a revenue event it decides whether this is a celebration or an operational problem, posts celebrations to the wins channel and alerts to revenue ops with the owner tagged, and for the top quartile by ARR also messages the CEO or CRO and the AE's manager. Nothing posts outside working hours unless it is marked urgent."
      prompt: 'Create a workflow firing on revenue events. Step sequence: (1) classify event type: celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don''t ping the team at 2am for routine wins).'
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Revenue notifications in Slack

Posts the wins to one channel and the problems to another, with the person who needs to act tagged, and stays quiet outside working hours.

## Before you run it

- Connect slack
- Send the `deal_won` event
- Send the `subscription_created` event
- Send the `order_placed` event

## What it does

1. **Write the celebration posts** (`create_slack_content`)

   A won deal names the rep, the account, the ARR and the contract length and tags the team. The first new B2B subscription of the month gets a fanfare and the rest a one liner. An ecommerce order only gets a post if it is in the top 5% by value. An upsell names the amount, the customer and the AE. Warm and brief.

2. **Write the operational alerts** (`create_slack_content`)

   For a different channel: a failed payment with the customer, the plan, the revenue at risk and the CSM tagged, a cancellation with its reason, and an unusually large abandoned cart. Terse, and clear about who has to act.

3. **Route wins and problems apart** (`create_workflow`)

   On a revenue event it decides whether this is a celebration or an operational problem, posts celebrations to the wins channel and alerts to revenue ops with the owner tagged, and for the top quartile by ARR also messages the CEO or CRO and the AE's manager. Nothing posts outside working hours unless it is marked urgent.

## What you end up with

- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
