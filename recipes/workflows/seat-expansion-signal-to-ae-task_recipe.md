---
name: seat-expansion-signal-to-ae-task
description: Use when a user mentions "seat expansion signal", "approaching plan limit", "seat upgrade workflow", or asks for related help. When an existing customer adds users approaching their plan limit OR multiple new users from the same domain self-serve sign up, create an AE expansion task — the strongest predictor of a seat upsell opportunity.
arguments: []
intempt:
  id: seat-expansion-signal-to-ae-task
  version: 1.0.0
  slashCommand: /seat-expansion-signal-to-ae-task
  group: Workflows
  shortDescription: "When an existing customer adds users approaching their plan limit OR multiple new users from the same domain self-serve sign up, create an AE expansion task — the strongest predictor of a seat upsell opportunity."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [expansion, seat-upsell, ae-routing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: user_signed_up, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Seat Capacity Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: seat_capacity
      description: 'Create an AI-derived attribute ''seat_capacity_used'' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account''s domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.).'
      prompt: 'Create an AI-derived attribute ''seat_capacity_used'' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account''s domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.).'
    - step: 2
      title: Identify Expansion-Ready Accounts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - seat_capacity
      description: Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE).
      prompt: Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE).
    - step: 3
      title: Build Expansion Detection Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - seat_capacity
      - segment
      description: 'Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip — they''re on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue.'
      prompt: 'Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip — they''re on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue.'
    - step: 4
      title: Build Expansion Pipeline Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - seat_capacity
      - segment
      - workflow
      description: 'Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target.'
      prompt: 'Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Seat Expansion Signal To Ae Task

## Procedure

1. **Build Seat Capacity Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'seat_capacity_used' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account's domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.). → produces: attribute
2. **Identify Expansion-Ready Accounts** [`create_segment`] — Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE). → produces: segment
3. **Build Expansion Detection Workflow** [`create_workflow`] — Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip — they're on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue. → produces: workflow
4. **Build Expansion Pipeline Dashboard** [`create_dashboard`] — Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target. → produces: dashboard
