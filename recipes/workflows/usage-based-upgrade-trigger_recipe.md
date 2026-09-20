---
name: usage-based-upgrade-trigger
description: Use when a user mentions "usage-based upgrade trigger", "plan limit approaching", "upgrade prompt workflow", or asks for related help. When a user approaches their plan's usage limit (API calls, contacts, seats, storage), trigger an in-app upgrade prompt AND create an AE task for high-MRR accounts, catch upgrade-ready moments at the moment of intent, not on the next renewal call.
arguments: []
intempt:
  id: usage-based-upgrade-trigger
  title: "Upgrade prompt when limits approach"
  version: 1.0.0
  slashCommand: /usage-based-upgrade-trigger
  group: Workflows
  shortDescription: "Catches an account nearing its plan limits, shows the decision maker an upgrade inside the app, and calls an AE in on the bigger ones."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: revops-automator
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [usage-based-expansion, upgrade-trigger]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: feature_used, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_page_content
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Find the bottleneck limit"
      command: create_ai_attribute
      produces: attribute
      bindsAs: usage_capacity
      description: "For every metered dimension on the plan, API calls, contacts, events, seats, storage or sends, current use as a share of the limit. It reports the highest of them and names which one, flagging 80% as approaching, 95% as near the limit, and 100% or more as over, where overage charges or throttling start."
      prompt: 'Create an AI-derived attribute ''usage_capacity_used'' on the Account object. For each metered usage dimension on the account''s current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling).'
    - step: 2
      title: "Find accounts near a limit"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - usage_capacity
      description: "Paying accounts at 80% or more that are not already on the top plan and have not discussed an upgrade in the last 30 days. Between 80 and 94% gets the in app prompt, 95 to 100% adds an AE task, and over the limit means an urgent AE task and a notice to the customer."
      prompt: 'Build a segment ''Upgrade-ready accounts'' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn''t already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) to in-app prompt, (b) near-limit (0.95-1.0) to in-app prompt + AE task, (c) over-limit to urgent AE task + customer notification.'
    - step: 3
      title: "Write the in app prompt"
      command: create_page_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "Named to the dimension running out, for example 84% of this month's events used on the current plan, with the current figure, a plan comparison and a one click upgrade. Helpful rather than pushy, and hidden from users who cannot approve a plan change."
      prompt: 'Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: ''You''ve used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.'' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we''re charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can''t approve).'
    - step: 4
      title: "Prompt, then call in an AE"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - usage_capacity
      - segment
      - asset
      description: "When usage crosses 80%, and again at each later threshold, the prompt appears for whoever can approve the plan, accounts over $500 a month get an AE expansion task straight away without waiting for a click, going over the limit adds an email to the billing contact about the overage, and an upgrade signal is recorded for analytics. It will not fire again for the same account within 14 days."
      prompt: 'Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don''t wait for prompt-clickthrough: these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don''t re-fire for the same account within 14 days even if it''s still over threshold (avoid prompt fatigue).'
    - step: 5
      title: "Compare prompt against AE"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - usage_capacity
      - segment
      - asset
      - workflow
      description: "Accounts crossing 80% per week, how many upgrade from the prompt, how many upgrade after AE outreach among the higher value ones, the ARR added this quarter, and the median time from crossing the threshold to upgrading."
      prompt: 'Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Upgrade prompt when limits approach

Catches an account nearing its plan limits, shows the decision maker an upgrade inside the app, and calls an AE in on the bigger ones.

## Before you run it

- Send the `feature_used` event

## What it does

1. **Find the bottleneck limit** (`create_ai_attribute`)

   For every metered dimension on the plan, API calls, contacts, events, seats, storage or sends, current use as a share of the limit. It reports the highest of them and names which one, flagging 80% as approaching, 95% as near the limit, and 100% or more as over, where overage charges or throttling start.

2. **Find accounts near a limit** (`create_segment`)

   Paying accounts at 80% or more that are not already on the top plan and have not discussed an upgrade in the last 30 days. Between 80 and 94% gets the in app prompt, 95 to 100% adds an AE task, and over the limit means an urgent AE task and a notice to the customer.

3. **Write the in app prompt** (`create_page_content`)

   Named to the dimension running out, for example 84% of this month's events used on the current plan, with the current figure, a plan comparison and a one click upgrade. Helpful rather than pushy, and hidden from users who cannot approve a plan change.

4. **Prompt, then call in an AE** (`create_workflow`)

   When usage crosses 80%, and again at each later threshold, the prompt appears for whoever can approve the plan, accounts over $500 a month get an AE expansion task straight away without waiting for a click, going over the limit adds an email to the billing contact about the overage, and an upgrade signal is recorded for analytics. It will not fire again for the same account within 14 days.

5. **Compare prompt against AE** (`create_dashboard`)

   Accounts crossing 80% per week, how many upgrade from the prompt, how many upgrade after AE outreach among the higher value ones, the ARR added this quarter, and the median time from crossing the threshold to upgrading.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
