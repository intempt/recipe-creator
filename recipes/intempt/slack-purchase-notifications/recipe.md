---
id: slack-purchase-notifications
title: Revenue notifications in Slack
slash_command: /slack-purchase-notifications
group: Workflows
owner: intempt
summary: Posts the wins to one channel and the problems to another, with the person who needs to act tagged,
  and stays quiet outside working hours.
description: >-
  Post celebration-grade Slack messages on key revenue events (deal_won, new subscription, expansion)
  and operational Slack messages on at-risk events (payment_failed, churn). Single configurable workflow
  handling the Slack revenue-notifications surface.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
    - ecommerce
  complexity: standard
  executionMode: live
  tags:
    - slack-notifications
    - revenue-events
prerequisites:
  events:
    - value: deal_won
      severity: blocking
    - value: subscription_created
      severity: blocking
    - value: order_placed
      severity: recommended
  integrations:
    - value: slack
      severity: blocking
steps:
  - id: s1
    title: Write the celebration posts
    summary: >-
      A won deal names the rep, the account, the ARR and the contract length and tags the team. The first
      new B2B subscription of the month gets a fanfare and the rest a one liner. An ecommerce order only
      gets a post if it is in the top 5% by value. An upsell names the amount, the customer and the AE.
      Warm and brief.
    builds: slack
    description: >-
      Generate Slack message content for revenue celebrations. Variants: (a) deal_won (include rep name,
      account, ARR, contract length, with a 🎉 emoji and team @mention; (b) subscription_created (B2B))
      first paying customer of the month gets a fanfare message, subsequent ones get a compact one-liner;
      (c) order_placed (ecommerce) (large-order threshold (top 5% of order values) gets celebration, normal
      orders silent; (d) expansion) upsell amount, customer name, AE who closed. Tone: warm, brief, team-celebratory.
  - id: s2
    title: Write the operational alerts
    summary: >-
      For a different channel: a failed payment with the customer, the plan, the revenue at risk and the
      CSM tagged, a cancellation with its reason, and an unusually large abandoned cart. Terse, and clear
      about who has to act.
    builds: slack
    description: >-
      Generate Slack message content for operational alerts (different channel from celebrations). Variants:
      (a) payment_failed: customer name, plan, MRR at risk, CSM owner @mention; (b) subscription_canceled
      with reason; (c) high-value-cart_abandoned (B2C, single cart value > threshold). Tone: terse, action-oriented,
      who-needs-to-respond clear.
  - id: s3
    title: Route wins and problems apart
    summary: >-
      On a revenue event it decides whether this is a celebration or an operational problem, posts celebrations
      to the wins channel and alerts to revenue ops with the owner tagged, and for the top quartile by
      ARR also messages the CEO or CRO and the AE's manager. Nothing posts outside working hours unless
      it is marked urgent.
    builds: workflow
    description: >-
      Create a workflow firing on revenue events. Step sequence: (1) classify event type: celebration
      (won/created/expansion) vs. operational (failed/canceled/at-risk); (2) for celebrations, post celebration
      content to #wins channel with deal/account context; (3) for operational, post alert content to #revenue-ops
      with rep/CSM @mention; (4) for high-value events (top-quartile ARR), additionally DM the CEO/CRO
      and AE manager (configurable threshold); (5) suppress notifications during off-hours unless explicitly
      tagged urgent (don't ping the team at 2am for routine wins). Use the result of "Write the celebration
      posts", "Write the operational alerts".
    dependsOn:
      - s1
      - s2
outputs:
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Revenue notifications in Slack

Posts the wins to one channel and the problems to another, with the person who needs to act tagged, and stays quiet outside working hours.

## Steps

1. **Write the celebration posts** (builds slack)

   A won deal names the rep, the account, the ARR and the contract length and tags the team. The first new B2B subscription of the month gets a fanfare and the rest a one liner. An ecommerce order only gets a post if it is in the top 5% by value. An upsell names the amount, the customer and the AE. Warm and brief.

2. **Write the operational alerts** (builds slack)

   For a different channel: a failed payment with the customer, the plan, the revenue at risk and the CSM tagged, a cancellation with its reason, and an unusually large abandoned cart. Terse, and clear about who has to act.

3. **Route wins and problems apart** (builds workflow)

   On a revenue event it decides whether this is a celebration or an operational problem, posts celebrations to the wins channel and alerts to revenue ops with the owner tagged, and for the top quartile by ARR also messages the CEO or CRO and the AE's manager. Nothing posts outside working hours unless it is marked urgent.

## What you end up with

- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
