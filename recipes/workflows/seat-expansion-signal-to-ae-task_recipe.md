---
name: seat-expansion-signal-to-ae-task
description: Use when a user mentions "seat expansion signal", "approaching plan limit", "seat upgrade workflow", or asks for related help. When an existing customer adds users approaching their plan limit OR multiple new users from the same domain self-serve sign up, create an AE expansion task, the strongest predictor of a seat upsell opportunity.
arguments: []
intempt:
  id: seat-expansion-signal-to-ae-task
  title: "Seat expansion signal to AE"
  version: 1.0.0
  slashCommand: /seat-expansion-signal-to-ae-task
  group: Workflows
  shortDescription: "Tells the AE when a customer is running out of seats or people from their domain keep signing up, which is the clearest upsell signal there is."
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
      title: "Measure how full the plan is"
      command: create_ai_attribute
      produces: attribute
      bindsAs: seat_capacity
      description: "Active seats as a share of the plan limit, flagged at 80% and again above 100%, where the overage is being billed. It also shows net seat growth over 30 days, how many people from the domain signed up in the last 14 days without a seat, and how close they are to any other cap such as API calls or contacts."
      prompt: 'Create an AI-derived attribute ''seat_capacity_used'' on the Account object. Compute: (active_seats / plan_seat_limit) as a fraction. Flag when >= 0.8 (approaching limit) or > 1.0 (over limit, billed as overage). Also surface: (a) net seat growth in last 30 days, (b) count of new sign-ups from the account''s domain in last 14 days not yet provisioned, (c) any usage cap proximity (API calls, contacts, etc.).'
    - step: 2
      title: "Find accounts near a limit"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - seat_capacity
      description: "Paying accounts at 80% of their seats or more, or with three or more unprovisioned signups from the domain in the last 14 days, or at 90% of any other cap. Accounts already in an expansion conversation are left out."
      prompt: Build a segment 'Seat-expansion candidates' capturing existing paying accounts where (a) seat_capacity_used >= 0.8, OR (b) 3+ new users from the domain signed up in the last 14 days not yet provisioned, OR (c) any usage cap is >= 0.9 utilized. Excludes accounts already in active expansion deal conversations (handled by AE).
    - step: 3
      title: "Raise the expansion task"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - seat_capacity
      - segment
      description: "When seats cross 80%, or a new signup arrives from a customer domain, it refreshes the account, checks whether an AE has engaged in the last 30 days and skips if so, then creates an expansion task naming which trigger fired, the current ARR, the plan and the likely upsell size, and messages the AE. Accounts with no AE go to the RevOps queue."
      prompt: 'Create a workflow firing when seat_capacity_used crosses 0.8, or when a new user_signed_up event comes from an existing customer domain. Step sequence: (1) refresh account context; (2) check whether AE already engaged this account in last 30 days (if so, skip: they''re on it); (3) create an AE expansion task with the trigger context (seat-capacity threshold vs. domain-signup spike vs. usage-cap), current ARR, plan tier, expected upsell size; (4) post Slack DM to the AE owner. If the account has no assigned AE, route to RevOps queue.'
    - step: 4
      title: "Track the expansion pipeline"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - seat_capacity
      - segment
      - workflow
      description: "Signals per week by trigger, how fast AEs respond, how many tasks become deals, how long those deals take, which is usually two to three times faster than new business, the win rate, and the ARR added so far this year against target."
      prompt: 'Compose an expansion pipeline dashboard: count of expansion signals per week (by trigger type: seat-cap / domain-signup / usage-cap), AE response time, expansion-task-to-deal-created conversion, expansion deal cycle time (typically 2-3x faster than new-logo deals), and expansion-deal win rate. ARR uplift from expansion signals YTD vs. target.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Seat expansion signal to AE

Tells the AE when a customer is running out of seats or people from their domain keep signing up, which is the clearest upsell signal there is.

## Before you run it

- Connect slack
- Send the `user_signed_up` event

## What it does

1. **Measure how full the plan is** (`create_ai_attribute`)

   Active seats as a share of the plan limit, flagged at 80% and again above 100%, where the overage is being billed. It also shows net seat growth over 30 days, how many people from the domain signed up in the last 14 days without a seat, and how close they are to any other cap such as API calls or contacts.

2. **Find accounts near a limit** (`create_segment`)

   Paying accounts at 80% of their seats or more, or with three or more unprovisioned signups from the domain in the last 14 days, or at 90% of any other cap. Accounts already in an expansion conversation are left out.

3. **Raise the expansion task** (`create_workflow`)

   When seats cross 80%, or a new signup arrives from a customer domain, it refreshes the account, checks whether an AE has engaged in the last 30 days and skips if so, then creates an expansion task naming which trigger fired, the current ARR, the plan and the likely upsell size, and messages the AE. Accounts with no AE go to the RevOps queue.

4. **Track the expansion pipeline** (`create_dashboard`)

   Signals per week by trigger, how fast AEs respond, how many tasks become deals, how long those deals take, which is usually two to three times faster than new business, the win rate, and the ARR added so far this year against target.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
