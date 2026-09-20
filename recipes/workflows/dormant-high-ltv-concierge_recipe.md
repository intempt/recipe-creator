---
name: dormant-high-ltv-concierge
description: Use when a user mentions "dormant high LTV concierge", "VIP customer dormancy", "high-value silence workflow", or asks for related help. When a high-LTV customer goes dormant (no product activity 30+ days), trigger a concierge outreach task, high-LTV silence is the strongest churn precursor and warrants personal CSM contact, not automated nurture.
arguments: []
intempt:
  id: dormant-high-ltv-concierge
  title: "Concierge for dormant big accounts"
  version: 1.0.0
  slashCommand: /dormant-high-ltv-concierge
  group: Workflows
  shortDescription: "When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks them to call. Nothing is sent automatically."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [saas, ecommerce]
    complexity: standard
    executionMode: live
    tags: [dormancy-detection, vip-retention, csm-outreach]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: session_start, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Track dormancy and value"
      command: create_ai_attribute
      produces: attribute
      bindsAs: dormancy_ltv
      description: "Two things per account, refreshed daily: days since anyone there last started a session, and lifetime value, meaning what they have paid plus what their current monthly revenue is likely to become at the retention curve for similar accounts. The top 10% by value counts as high value."
      prompt: 'Create AI-derived attributes on the Account object: ''days_dormant'' (days since last session_start by ANY user on the account) and ''account_ltv'' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily.'
    - step: 2
      title: "Find the valuable ones gone quiet"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - dormancy_ltv
      description: "Accounts in the top 10% by value, dormant 30 days or more, with no CSM contact in the last 30 days. Accounts a CSM has flagged as temporarily paused, for a legal review or a team holiday, are left out."
      prompt: Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave', these are flagged by CSM separately).
    - step: 3
      title: "Brief the CSM and escalate"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - dormancy_ltv
      - segment
      description: "Daily, for each newly dormant account, it gathers the usage trend before they went quiet, recent support tickets and the last meeting summary, and writes a brief with the days dormant, the last activity, any decline pattern, the support topics and a suggested angle: a check in, re-onboarding, or an executive introduction. That becomes an urgent CSM task, a Slack message to the CSM and their manager, and a churn risk tag on the account. No email goes out automatically."
      prompt: 'Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as ''churn-risk: dormant'' for forecast visibility. Don''t auto-send any email: concierge outreach must be personal.'
    - step: 4
      title: "Prove the call is worth making"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - dormancy_ltv
      - segment
      - workflow
      description: "How many valuable accounts are dormant, the ARR they represent, how fast CSMs respond against a 48 hour target, how many come back within 14 days of contact, and the 90 day churn rate for accounts contacted inside 48 hours against those never contacted."
      prompt: 'Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by ''CSM contacted within 48hr of dormancy'' vs. ''no CSM contact'': typically the gap is dramatic and proves the workflow''s value.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Concierge for dormant big accounts

When one of your most valuable accounts stops showing up for a month, it briefs the CSM and asks them to call. Nothing is sent automatically.

## Before you run it

- Connect slack
- Send the `session_start` event

## What it does

1. **Track dormancy and value** (`create_ai_attribute`)

   Two things per account, refreshed daily: days since anyone there last started a session, and lifetime value, meaning what they have paid plus what their current monthly revenue is likely to become at the retention curve for similar accounts. The top 10% by value counts as high value.

2. **Find the valuable ones gone quiet** (`create_segment`)

   Accounts in the top 10% by value, dormant 30 days or more, with no CSM contact in the last 30 days. Accounts a CSM has flagged as temporarily paused, for a legal review or a team holiday, are left out.

3. **Brief the CSM and escalate** (`create_workflow`)

   Daily, for each newly dormant account, it gathers the usage trend before they went quiet, recent support tickets and the last meeting summary, and writes a brief with the days dormant, the last activity, any decline pattern, the support topics and a suggested angle: a check in, re-onboarding, or an executive introduction. That becomes an urgent CSM task, a Slack message to the CSM and their manager, and a churn risk tag on the account. No email goes out automatically.

4. **Prove the call is worth making** (`create_dashboard`)

   How many valuable accounts are dormant, the ARR they represent, how fast CSMs respond against a 48 hour target, how many come back within 14 days of contact, and the 90 day churn rate for accounts contacted inside 48 hours against those never contacted.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
