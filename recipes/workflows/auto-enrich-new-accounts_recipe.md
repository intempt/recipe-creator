---
name: auto-enrich-new-accounts
description: Use when a user mentions "auto enrich new accounts", "account enrichment workflow", "firmographic enrichment", or asks for related help. When a new account record is created (from signup, form, or import), immediately enrich it with firmographic + technographic data, compute ICP fit, and route based on tier, so reps see fully-formed account context, not a name and email.
arguments: []
intempt:
  id: auto-enrich-new-accounts
  title: "Enrich new accounts automatically"
  version: 1.0.0
  slashCommand: /auto-enrich-new-accounts
  group: Workflows
  shortDescription: "Fills in industry, size, revenue and tech stack for every new account within minutes, scores the fit, and routes the best ones to an owner."
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
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Score the fit once enriched"
      command: create_ai_attribute
      produces: attribute
      bindsAs: icp_fit
      description: "A 0 to 100 score from industry against your target list, headcount band, revenue band, the tools they already run, and geography. Banded ideal at 80 and up, viable 50 to 79, marginal 20 to 49, poor below 20. It recalculates when the enrichment data changes."
      prompt: 'Create an AI-derived attribute ''icp_fit_score'' on the Account object. Inputs after enrichment: industry (match against ICP target industries), employee count band, annual revenue band, tech stack signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates.'
    - step: 2
      title: "Find the accounts still blank"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - icp_fit
      description: "Accounts created in the last 90 days with at least one known user and no industry, headcount or country. This is what the daily backfill works through."
      prompt: Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry, employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time enrichment.
    - step: 3
      title: "Enrich on creation, then daily"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - icp_fit
      - segment
      description: "Runs on account creation and again daily over the blank ones. It calls your enrichment provider with the domain, writes back the firmographics and tech stack, scores the fit, routes ideal accounts with no AE by territory, and posts to the data quality channel when the match was weak. Accounts enriched in the last 90 days are skipped."
      prompt: 'Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already enriched in last 90 days.'
    - step: 4
      title: "Check coverage and fit mix"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - icp_fit
      - segment
      - workflow
      description: "The share of active accounts fully enriched against a 95% target, how fit scores are spread, the provider's success rate, the median time from creation to enriched, which should be under five minutes, and the fit mix among new accounts."
      prompt: 'Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales targeting health).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Enrich new accounts automatically

Fills in industry, size, revenue and tech stack for every new account within minutes, scores the fit, and routes the best ones to an owner.

## Before you run it

- Connect slack

## What it does

1. **Score the fit once enriched** (`create_ai_attribute`)

   A 0 to 100 score from industry against your target list, headcount band, revenue band, the tools they already run, and geography. Banded ideal at 80 and up, viable 50 to 79, marginal 20 to 49, poor below 20. It recalculates when the enrichment data changes.

2. **Find the accounts still blank** (`create_segment`)

   Accounts created in the last 90 days with at least one known user and no industry, headcount or country. This is what the daily backfill works through.

3. **Enrich on creation, then daily** (`create_workflow`)

   Runs on account creation and again daily over the blank ones. It calls your enrichment provider with the domain, writes back the firmographics and tech stack, scores the fit, routes ideal accounts with no AE by territory, and posts to the data quality channel when the match was weak. Accounts enriched in the last 90 days are skipped.

4. **Check coverage and fit mix** (`create_dashboard`)

   The share of active accounts fully enriched against a 95% target, how fit scores are spread, the provider's success rate, the median time from creation to enriched, which should be under five minutes, and the fit mix among new accounts.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
