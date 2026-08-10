---
name: dormant-high-ltv-concierge
description: Use when a user mentions "dormant high LTV concierge", "VIP customer dormancy", "high-value silence workflow", or asks for related help. When a high-LTV customer goes dormant (no product activity 30+ days), trigger a concierge outreach task — high-LTV silence is the strongest churn precursor and warrants personal CSM contact, not automated nurture.
arguments: []
intempt:
  id: dormant-high-ltv-concierge
  version: 1.0.0
  slashCommand: /dormant-high-ltv-concierge
  group: Workflows
  shortDescription: "When a high-LTV customer goes dormant (no product activity 30+ days), trigger a concierge outreach task — high-LTV silence is the strongest churn precursor and warrants personal CSM contact, not automated nurture."
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
      title: Compute Dormancy + LTV Attributes
      command: create_ai_attribute
      produces: attribute
      bindsAs: dormancy_ltv
      description: 'Create AI-derived attributes on the Account object: ''days_dormant'' (days since last session_start by ANY user on the account) and ''account_ltv'' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily.'
      prompt: 'Create AI-derived attributes on the Account object: ''days_dormant'' (days since last session_start by ANY user on the account) and ''account_ltv'' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily.'
    - step: 2
      title: Identify Dormant VIPs
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - dormancy_ltv
      description: Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave' — these are flagged by CSM separately).
      prompt: Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave' — these are flagged by CSM separately).
    - step: 3
      title: Build Concierge Outreach Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - dormancy_ltv
      - segment
      description: 'Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as ''churn-risk: dormant'' for forecast visibility. Don''t auto-send any email — concierge outreach must be personal.'
      prompt: 'Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as ''churn-risk: dormant'' for forecast visibility. Don''t auto-send any email — concierge outreach must be personal.'
    - step: 4
      title: Build VIP Retention Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - dormancy_ltv
      - segment
      - workflow
      description: 'Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by ''CSM contacted within 48hr of dormancy'' vs. ''no CSM contact'' — typically the gap is dramatic and proves the workflow''s value.'
      prompt: 'Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by ''CSM contacted within 48hr of dormancy'' vs. ''no CSM contact'' — typically the gap is dramatic and proves the workflow''s value.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Dormant High Ltv Concierge

## Procedure

1. **Compute Dormancy + LTV Attributes** [`create_ai_attribute`] — Create AI-derived attributes on the Account object: 'days_dormant' (days since last session_start by ANY user on the account) and 'account_ltv' (cumulative revenue paid, plus projected forward LTV based on current MRR × historical retention curve for similar accounts). LTV tier: top 10% of customers by LTV = high-LTV. Refreshed daily. → produces: attribute
2. **Identify Dormant VIPs** [`create_segment`] — Build a segment 'Dormant high-LTV accounts' capturing accounts where account_ltv is in the top 10% AND days_dormant >= 30 AND the account has not had CSM contact in last 30 days. Excludes accounts with a known temporary-pause status (e.g. 'paused for legal review', 'team on annual leave' — these are flagged by CSM separately). → produces: segment
3. **Build Concierge Outreach Workflow** [`create_workflow`] — Create a workflow firing daily for newly-dormant high-LTV accounts. Step sequence: (1) refresh account context: usage trajectory (was it declining before going dormant?), recent support tickets, last meeting summary; (2) compose a context blob for CSM with: dormancy days, last activity date, decline pattern if any, recent support topics, suggested outreach angle (check-in / re-onboarding offer / executive sponsor intro); (3) create urgent CSM task with full context attached; (4) post Slack DM to the named CSM + their manager (high-LTV dormancy is escalation-worthy); (5) tag account in CRM as 'churn-risk: dormant' for forecast visibility. Don't auto-send any email — concierge outreach must be personal. → produces: workflow
4. **Build VIP Retention Dashboard** [`create_dashboard`] — Compose a VIP retention dashboard: count of high-LTV dormant accounts (the at-risk pile), ARR at risk in this segment, CSM response time on dormancy alerts (target: <48hr), re-engagement success rate (dormant-account-to-active-again within 14 days of CSM outreach), and 90-day churn rate split by 'CSM contacted within 48hr of dormancy' vs. 'no CSM contact' — typically the gap is dramatic and proves the workflow's value. → produces: dashboard
