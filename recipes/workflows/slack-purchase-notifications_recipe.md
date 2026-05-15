---
name: slack-purchase-notifications
description: Use when a user mentions "slack purchase notifications", "revenue celebrations", "deal-won slack alert", or asks for related help. Post celebration-grade Slack messages on key revenue events (deal_won, new subscription, expansion) and operational Slack messages on at-risk events (payment_failed, churn). Single configurable workflow handling the Slack revenue-notifications surface.
arguments: []
intempt:
  id: slack-purchase-notifications
  version: 1.0.0
  slashCommand: /slack-purchase-notifications
  group: Workflows
  shortDescription: "Post celebration-grade Slack messages on key revenue events (deal_won, new subscription, expansion) and operational Slack messages on at-risk events (payment_failed, churn). Single configurable workflow handling the Slack revenue-notifications surface."
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
      title: Build Celebration Slack Content
      command: create_slack_content
      produces: asset
      bindsAs: celebration_asset
      description: 'Generate Slack message content for revenue celebrations. Variants: (a) deal_won — include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B) — first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) — large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion — upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.'
      prompt: 'Generate Slack message content for revenue celebrations. Variants: (a) deal_won — include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B) — first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) — large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion — upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.'
    - step: 2
      title: Build Operational Alert Content
      command: create_slack_content
      produces: asset
      bindsAs: alert_asset
      description: 'Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) payment_failed — customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear.'
      prompt: 'Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) payment_failed — customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear.'
    - step: 3
      title: Build Notification Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - celebration_asset
      - alert_asset
      description: 'Create a workflow firing on revenue events. Step sequence: (1) classify event type — celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don''t ping the team at 2am for routine wins).'
      prompt: 'Create a workflow firing on revenue events. Step sequence: (1) classify event type — celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don''t ping the team at 2am for routine wins).'
  outputs:
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
---

# Slack Purchase Notifications

## Procedure

1. **Build Celebration Slack Content** [`create_slack_content`] — Generate Slack message content for revenue celebrations. Variants: (a) deal_won — include rep name, account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B) — first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner; (c) order_placed (ecommerce) — large-order threshold (top 5% of order values) gets celebration, normal orders silent; (d) expansion — upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory. → produces: asset
2. **Build Operational Alert Content** [`create_slack_content`] — Generate Slack message content for operational alerts (different channel from celebrations). Variants: (a) payment_failed — customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented, who-needs-to-respond clear. → produces: asset
3. **Build Notification Workflow** [`create_workflow`] — Create a workflow firing on revenue events. Step sequence: (1) classify event type — celebration (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly tagged urgent (don't ping the team at 2am for routine wins). → produces: workflow
