---
name: enterprise-domain-signup-to-ae-task
description: Use when a user mentions "enterprise domain signup", "fortune 500 signup alert", "high-tier domain detection", or asks for related help. When a self-serve signup comes from an enterprise-tier domain (Fortune 500, target-account list, or domain matching ICP), immediately create an AE task with full account enrichment — don't let an enterprise lead languish in the standard free-tier funnel.
arguments: []
intempt:
  id: enterprise-domain-signup-to-ae-task
  version: 1.0.0
  slashCommand: /enterprise-domain-signup-to-ae-task
  group: Workflows
  shortDescription: "When a self-serve signup comes from an enterprise-tier domain (Fortune 500, target-account list, or domain matching ICP), immediately create an AE task with full account enrichment — don't let an enterprise lead languish in the standard free-tier funnel."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [enterprise-lead, domain-detection, ae-routing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: user_signed_up, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Enterprise Tier Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: domain_tier
      description: 'Create an AI-derived attribute ''account_tier'' on the Account object. Computed at signup from email domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise, 100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains (gmail, outlook) → tier: consumer (likely not a buyer).'
      prompt: 'Create an AI-derived attribute ''account_tier'' on the Account object. Computed at signup from email domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise, 100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains (gmail, outlook) → tier: consumer (likely not a buyer).'
    - step: 2
      title: Identify Enterprise Signups
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - domain_tier
      description: Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow audit and post-hoc analysis of enterprise-lead conversion.
      prompt: Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow audit and post-hoc analysis of enterprise-lead conversion.
    - step: 3
      title: Build Enterprise Detection Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - domain_tier
      - segment
      description: 'Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers, tech stack); (3) check whether the account is already in the CRM or part of target-account list; (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts with account context, decision-maker contacts, and current product activity; (6) suppress this user from the standard self-serve nurture journey (different motion for enterprise — sales-led, not marketing-led).'
      prompt: 'Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers, tech stack); (3) check whether the account is already in the CRM or part of target-account list; (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts with account context, decision-maker contacts, and current product activity; (6) suppress this user from the standard self-serve nurture journey (different motion for enterprise — sales-led, not marketing-led).'
    - step: 4
      title: Build Enterprise Lead Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - domain_tier
      - segment
      - workflow
      description: 'Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target: <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound), and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can see ICP attraction trends.'
      prompt: 'Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target: <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound), and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can see ICP attraction trends.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Enterprise Domain Signup To Ae Task

## Procedure

1. **Build Enterprise Tier Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'account_tier' on the Account object. Computed at signup from email domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise, 100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains (gmail, outlook) → tier: consumer (likely not a buyer). → produces: attribute
2. **Identify Enterprise Signups** [`create_segment`] — Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow audit and post-hoc analysis of enterprise-lead conversion. → produces: segment
3. **Build Enterprise Detection Workflow** [`create_workflow`] — Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers, tech stack); (3) check whether the account is already in the CRM or part of target-account list; (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts with account context, decision-maker contacts, and current product activity; (6) suppress this user from the standard self-serve nurture journey (different motion for enterprise — sales-led, not marketing-led). → produces: workflow
4. **Build Enterprise Lead Dashboard** [`create_dashboard`] — Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target: <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound), and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can see ICP attraction trends. → produces: dashboard
