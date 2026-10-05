---
name: auto-enrich-new-accounts
description: Use when a user mentions "auto enrich new accounts", "account enrichment workflow", "firmographic enrichment", or asks for related help. When a new account record is created (from signup, form, or import), immediately enrich it with firmographic + technographic data, compute ICP fit, and route based on tier — so reps see fully-formed account context, not a name and email.
arguments: []
intempt:
  id: auto-enrich-new-accounts
  version: 1.0.0
  slashCommand: /auto-enrich-new-accounts
  group: Workflows
  shortDescription: "Create an AI-derived icp_fit_score attribute on Accounts, an 'Unenriched accounts' segment, and a tier-routing workflow."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [enrichment, icp-scoring, data-quality]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build ICP Fit Score Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: icp_fit
      description: 'Create an AI-derived attribute ''icp_fit_score'' on the Account object. Inputs after enrichment: industry (match against ICP target industries), employee count band, annual revenue band, tech stack signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates.'
      prompt: 'Create an AI-derived attribute ''icp_fit_score'' on the Account object. Inputs after enrichment: industry (match against ICP target industries), employee count band, annual revenue band, tech stack signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates.'
    - step: 2
      title: Identify Unenriched Accounts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - icp_fit
      description: Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry, employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time enrichment.
      prompt: Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry, employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time enrichment.
    - step: 3
      title: Build Account Enrichment Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - icp_fit
      - segment
      description: 'Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already enriched in last 90 days.'
      prompt: 'Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already enriched in last 90 days.'
    - step: 4
      title: Build Enrichment Coverage Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - icp_fit
      - segment
      - workflow
      description: 'Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales targeting health).'
      prompt: 'Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales targeting health).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Auto Enrich New Accounts

## Procedure

1. **Build ICP Fit Score Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'icp_fit_score' on the Account object. Inputs after enrichment: industry (match against ICP target industries), employee count band, annual revenue band, tech stack signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates. → produces: attribute
2. **Identify Unenriched Accounts** [`create_segment`] — Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry, employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time enrichment. → produces: segment
3. **Build Account Enrichment Workflow** [`create_workflow`] — Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already enriched in last 90 days. → produces: workflow
4. **Build Enrichment Coverage Dashboard** [`create_dashboard`] — Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales targeting health). → produces: dashboard
