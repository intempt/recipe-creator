---
frontmatter_id: auto-enrich-new-accounts
slash_command: /auto-enrich-new-accounts
description: Fills in industry, size, revenue and tech stack for every new account within minutes, scores the fit, and routes the best ones to an owner.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Automatically enriches each new account with industry, size, revenue and tech stack, scores its ICP fit, routes
    top accounts to an owner, and tracks enrichment coverage.
  parameters:
  - name: enrichment_window
    type: duration
    label: Skip re-enrichment if enriched within
    default: 90 d
    required: false
  - name: backfill_lookback
    type: duration
    label: Backfill lookback for accounts created within
    default: 90 d
    required: false
  - name: coverage_target
    type: number
    label: Target percentage of active accounts fully enriched
    default: 95
    required: false
  - name: realtime_target
    type: duration
    label: Target time from account creation to fully enriched
    default: 5 min
    required: false
  - name: data_quality_channel
    type: string
    label: Slack channel for low-confidence enrichment alerts
    default: '#data-quality'
    required: false
  requirements:
  - slot: account_created
    kind: event
    meaning: A new account was created in the CRM
    properties:
    - name: domain
      type: string
      meaning: Web domain of the account
      optional: false
  - slot: account_firmographics
    kind: attribute
    meaning: Account fields for industry, employee count, annual revenue, country and tech stack
  - slot: identified_user
    kind: attribute
    meaning: A user is identified and linked to an account
  - slot: ai_attribute_store
    kind: attribute
    meaning: Account-level AI-derived attribute store for computed scores
  - slot: icp_target_industries
    kind: knowledge
    meaning: Document listing the ideal customer profile target industries, size bands, revenue bands and geographies
  - slot: enrichment_api
    kind: integration
    meaning: Company data enrichment vendor connection that returns firmographics for a domain
    channel: email
  - slot: data_quality_slack
    kind: destination
    meaning: Slack channel where data quality alerts are posted
    channel: slack
  - slot: territory_rules
    kind: segment
    meaning: Territory assignment rules that route accounts to an owner
  - slot: active_accounts
    kind: segment
    meaning: Accounts currently active in the CRM
  steps:
  - id: s1
    builds: attribute
    uses:
    - icp_target_industries
    - account_firmographics
    - ai_attribute_store
    instruction: 'Create an account-level AI-derived attribute named icp_fit_score on the Account object. Inputs, read after
      enrichment: industry matched against {icp_target_industries}, employee count band, annual revenue band, tech stack signals
      showing complementary tools that indicate fit, and geographic match. Output a 0-100 score with tier: ideal 80 and above,
      viable 50-79, marginal 20-49, poor below 20. Refresh whenever enrichment data on the account updates.'
  - id: s2
    builds: segment
    uses:
    - account_firmographics
    - identified_user
    - backfill_lookback
    - s1
    instruction: Build a segment named 'Unenriched accounts' containing accounts where (a) industry, employee count and country
      are all empty, AND (b) the account was created within {backfill_lookback}, AND (c) the account has at least one identified
      user. This segment feeds the periodic backfill workflow for accounts that escaped real-time enrichment. Use the icp_fit_score
      attribute from "Score the fit once enriched" for scoring.
  - id: s3
    builds: automation
    uses:
    - account_created
    - enrichment_api
    - enrichment_window
    - account_firmographics
    - territory_rules
    - data_quality_slack
    - s1
    - s2
    instruction: 'Create a workflow with two triggers: (a) when {account_created} fires, run real-time enrichment; (b) run
      daily on the ''Unenriched accounts'' segment from "Find the accounts still blank" for backfill. Steps in order: (1)
      call {enrichment_api} with the account domain, skipping accounts enriched within {enrichment_window}; (2) update the
      account with industry, employee count, annual revenue, geography and tech stack; (3) recompute icp_fit_score from "Score
      the fit once enriched"; (4) if icp_fit_score tier is ideal and no account executive is assigned, route the account using
      {territory_rules}; (5) if enrichment confidence is low, post an enrichment summary to {data_quality_slack} for manual
      review.'
  - id: s4
    builds: dashboard
    uses:
    - active_accounts
    - coverage_target
    - realtime_target
    - s1
    - s2
    - s3
    instruction: 'Compose an enrichment coverage dashboard with these panels: percentage of {active_accounts} fully enriched,
      against a target of {coverage_target} percent; distribution of icp_fit_score across active accounts from "Score the
      fit once enriched"; enrichment API success rate, where a low rate points to vendor or domain quality issues; median
      time from account creation to fully enriched, against a target of {realtime_target} for the real-time path; and ICP
      tier mix among new accounts as a leading indicator of targeting health. Include the unenriched backlog from "Find the
      accounts still blank" and the outcomes of "Enrich on creation, then daily".'
---

# Enrich new accounts automatically

Slash command: /auto-enrich-new-accounts

## Step 1: Score the fit once enriched

Create an AI-derived attribute 'icp_fit_score' on the Account object. Inputs after enrichment: industry (match against ICP target industries), employee count band, annual revenue band, tech stack signals (does the account use complementary tools that signal fit?), geographic match. Output: 0-100 score with tier (ideal 80+, viable 50-79, marginal 20-49, poor <20). Refreshed when enrichment data updates.

## Step 2: Find the accounts still blank

Build a segment 'Unenriched accounts' capturing accounts where (a) firmographic fields (industry, employee_count, country) are null AND (b) account created in last 90 days AND (c) account has at least one identified user. Used for the periodic backfill workflow on accounts that escaped real-time enrichment. Use the result of "Score the fit once enriched".

## Step 3: Enrich on creation, then daily

Create a workflow with two triggers: (a) firing on account creation (real-time enrichment), and (b) scheduled daily for the unenriched-accounts segment (backfill). Step sequence: (1) call enrichment API (Apollo/ZoomInfo/Clearbit) with the account domain; (2) update account record with firmographics (industry, employee_count, revenue, geography, tech_stack); (3) compute icp_fit_score; (4) if score = ideal AND no AE assigned, route via territory rules; (5) post enrichment summary to Slack #data-quality channel if enrichment confidence is low (manual review needed). Skip enrichment for accounts already enriched in last 90 days. Use the result of "Score the fit once enriched", "Find the accounts still blank".

## Step 4: Check coverage and fit mix

Compose an enrichment coverage dashboard: % of active accounts fully enriched (target: 95%+), distribution of icp_fit_score across the active account base, enrichment API success rate (low = vendor issue or domain quality issue), median time from account-creation to fully-enriched (should be < 5 minutes for real-time path), and ICP-tier mix among new accounts (a leading indicator of marketing/sales targeting health). Use the result of "Score the fit once enriched", "Find the accounts still blank", "Enrich on creation, then daily".
