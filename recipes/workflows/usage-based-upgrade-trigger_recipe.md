---
name: usage-based-upgrade-trigger
description: Use when a user mentions "usage-based upgrade trigger", "plan limit approaching", "upgrade prompt workflow", or asks for related help. When a user approaches their plan's usage limit (API calls, contacts, seats, storage), trigger an in-app upgrade prompt AND create an AE task for high-MRR accounts — catch upgrade-ready moments at the moment of intent, not on the next renewal call.
arguments: []
intempt:
  id: usage-based-upgrade-trigger
  version: 1.0.0
  slashCommand: /usage-based-upgrade-trigger
  group: Workflows
  shortDescription: "Create a segment of accounts whose AI-derived usage_capacity_used attribute crosses 0.8, plus a workflow routing high-MRR ones to an AE."
  availability: coming-soon
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
      title: Compute Usage Capacity Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: usage_capacity
      description: 'Create an AI-derived attribute ''usage_capacity_used'' on the Account object. For each metered usage dimension on the account''s current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling).'
      prompt: 'Create an AI-derived attribute ''usage_capacity_used'' on the Account object. For each metered usage dimension on the account''s current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling).'
    - step: 2
      title: Identify Upgrade-Ready Accounts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - usage_capacity
      description: 'Build a segment ''Upgrade-ready accounts'' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn''t already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) → in-app prompt, (b) near-limit (0.95-1.0) → in-app prompt + AE task, (c) over-limit → urgent AE task + customer notification.'
      prompt: 'Build a segment ''Upgrade-ready accounts'' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn''t already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) → in-app prompt, (b) near-limit (0.95-1.0) → in-app prompt + AE task, (c) over-limit → urgent AE task + customer notification.'
    - step: 3
      title: Build Upgrade Prompt Asset
      command: create_page_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: ''You''ve used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.'' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we''re charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can''t approve).'
      prompt: 'Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: ''You''ve used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.'' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we''re charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can''t approve).'
    - step: 4
      title: Build Upgrade Trigger Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - usage_capacity
      - segment
      - asset
      description: 'Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don''t wait for prompt-clickthrough — these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don''t re-fire for the same account within 14 days even if it''s still over threshold (avoid prompt fatigue).'
      prompt: 'Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don''t wait for prompt-clickthrough — these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don''t re-fire for the same account within 14 days even if it''s still over threshold (avoid prompt fatigue).'
    - step: 5
      title: Build Upgrade Conversion Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - usage_capacity
      - segment
      - asset
      - workflow
      description: 'Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal.'
      prompt: 'Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Usage Based Upgrade Trigger

## Procedure

1. **Compute Usage Capacity Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'usage_capacity_used' on the Account object. For each metered usage dimension on the account's current plan (API calls / contacts / events / seats / storage / sends), compute current_usage / plan_limit as a fraction. Output: the maximum across all dimensions (the bottleneck), with which dimension is at threshold. Flag thresholds: 0.8 = approaching, 0.95 = near-limit, 1.0+ = over-limit (overage charges or service throttling). → produces: attribute
2. **Identify Upgrade-Ready Accounts** [`create_segment`] — Build a segment 'Upgrade-ready accounts' capturing paying accounts where usage_capacity_used >= 0.8 AND the account isn't already on the highest plan AND no upgrade conversation occurred in last 30 days. Splits implicitly: (a) approaching (0.8-0.94) → in-app prompt, (b) near-limit (0.95-1.0) → in-app prompt + AE task, (c) over-limit → urgent AE task + customer notification. → produces: segment
3. **Build Upgrade Prompt Asset** [`create_page_content`] — Generate in-app upgrade prompt content. Personalized to which dimension is approaching limit: 'You've used 84% of your monthly events on the Starter plan. Upgrade to Pro for 10x capacity + advanced reporting.' Include current usage stat, plan comparison, and a one-click upgrade CTA. Tone: helpful (we noticed) not pushy (we're charging you). Suppress display for users not in plan-decision-maker role (avoid spamming end users about upgrades they can't approve). → produces: asset
4. **Build Upgrade Trigger Workflow** [`create_workflow`] — Create a workflow firing when usage_capacity_used crosses 0.8 (and on each subsequent threshold). Step sequence: (1) trigger in-app upgrade prompt for plan-decision-makers on the account; (2) for accounts with MRR > $500/month, create AE expansion task immediately (don't wait for prompt-clickthrough — these are high-value, deserve human outreach); (3) for over-limit cases, additionally send an email notification to billing-contact about overage; (4) emit upgrade_signal event for analytics tracking. Throttle: don't re-fire for the same account within 14 days even if it's still over threshold (avoid prompt fatigue). → produces: workflow
5. **Build Upgrade Conversion Dashboard** [`create_dashboard`] — Compose an upgrade conversion dashboard: usage-trigger volume per week (accounts crossing 0.8 threshold), in-app-prompt-to-upgrade conversion rate, AE-task-to-upgrade conversion rate (for high-MRR cohort), ARR uplift from usage-based expansion this quarter, and median time from threshold-cross to upgrade-completed. Compare upgrade-via-prompt vs. upgrade-via-AE-outreach as motion-effectiveness signal. → produces: dashboard
