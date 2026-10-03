---
id: auto-enrich-new-accounts
title: Enrich new accounts automatically
slash_command: /auto-enrich-new-accounts
group: Workflows
owner: intempt
summary: Fills in industry, size, revenue and tech stack for every new account within minutes, scores
  the fit, and routes the best ones to an owner.
description: >-
  When a new account record is created (from signup, form, or import), immediately enrich it with firmographic
  + technographic data, compute ICP fit, and route based on tier, so reps see fully-formed account context,
  not a name and email.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - enrichment
    - icp-scoring
    - data-quality
prerequisites:
  integrations:
    - value: slack
      severity: recommended
steps:
  - id: s1
    title: Score the fit once enriched
    summary: >-
      A 0 to 100 score from industry against your target list, headcount band, revenue band, the tools
      they already run, and geography. Banded ideal at 80 and up, viable 50 to 79, marginal 20 to 49,
      poor below 20. It recalculates when the enrichment data changes.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'icp_fit_score' on the Account object. Inputs after enrichment: industry
      (match against ICP target industries), employee count band, annual revenue band, tech stack signals
      (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score
      with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates.
  - id: s2
    title: Find the accounts still blank
    summary: >-
      Accounts created in the last 90 days with at least one known user and no industry, headcount or
      country. This is what the daily backfill works through.
    builds: segment
    description: >-
      Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry,
      employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at
      least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time
      enrichment. Use the result of "Score the fit once enriched".
    dependsOn:
      - s1
  - id: s3
    title: Enrich on creation, then daily
    summary: >-
      Runs on account creation and again daily over the blank ones. It calls your enrichment provider
      with the domain, writes back the firmographics and tech stack, scores the fit, routes ideal accounts
      with no AE by territory, and posts to the data quality channel when the match was weak. Accounts
      enriched in the last 90 days are skipped.
    builds: workflow
    description: >-
      Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and
      (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment
      API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics
      (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score
      = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality
      channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already
      enriched in last 90 days. Use the result of "Score the fit once enriched", "Find the accounts still
      blank".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Check coverage and fit mix
    summary: >-
      The share of active accounts fully enriched against a 95% target, how fit scores are spread, the
      provider's success rate, the median time from creation to enriched, which should be under five minutes,
      and the fit mix among new accounts.
    builds: dashboard
    description: >-
      Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution
      of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue
      or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes
      for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales
      targeting health). Use the result of "Score the fit once enriched", "Find the accounts still blank",
      "Enrich on creation, then daily".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Enrich new accounts automatically

Fills in industry, size, revenue and tech stack for every new account within minutes, scores the fit, and routes the best ones to an owner.

## Steps

1. **Score the fit once enriched** (builds attribute)

   A 0 to 100 score from industry against your target list, headcount band, revenue band, the tools they already run, and geography. Banded ideal at 80 and up, viable 50 to 79, marginal 20 to 49, poor below 20. It recalculates when the enrichment data changes.

2. **Find the accounts still blank** (builds segment)

   Accounts created in the last 90 days with at least one known user and no industry, headcount or country. This is what the daily backfill works through.

3. **Enrich on creation, then daily** (builds workflow)

   Runs on account creation and again daily over the blank ones. It calls your enrichment provider with the domain, writes back the firmographics and tech stack, scores the fit, routes ideal accounts with no AE by territory, and posts to the data quality channel when the match was weak. Accounts enriched in the last 90 days are skipped.

4. **Check coverage and fit mix** (builds dashboard)

   The share of active accounts fully enriched against a 95% target, how fit scores are spread, the provider's success rate, the median time from creation to enriched, which should be under five minutes, and the fit mix among new accounts.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
