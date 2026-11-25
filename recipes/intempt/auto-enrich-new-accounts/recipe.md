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
visibility: draft
rejected: Its core is filling firmographics from an outside company-data provider; Blu steps cannot call an enrichment API
  or write those fields.
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
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
    dependsOn:
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
    dependsOn:
    - s1
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
    dependsOn:
    - s1
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

Create an account-level AI-derived attribute named icp_fit_score on the Account object. Inputs, read after enrichment: industry matched against icp target industries, employee count band, annual revenue band, tech stack signals showing complementary tools that indicate fit, and geographic match. Output a 0-100 score with tier: ideal 80 and above, viable 50-79, marginal 20-49, poor below 20. Refresh whenever enrichment data on the account updates.

## Step 2: Find the accounts still blank

Build a segment named 'Unenriched accounts' containing accounts where (a) industry, employee count and country are all empty, AND (b) the account was created within 90 d, AND (c) the account has at least one identified user. This segment feeds the periodic backfill workflow for accounts that escaped real-time enrichment. Use the icp_fit_score attribute from "Score the fit once enriched" for scoring.

## Step 3: Enrich on creation, then daily

Create a workflow with two triggers: (a) when account created fires, run real-time enrichment; (b) run daily on the 'Unenriched accounts' segment from "Find the accounts still blank" for backfill. Steps in order: (1) call enrichment api with the account domain, skipping accounts enriched within 90 d; (2) update the account with industry, employee count, annual revenue, geography and tech stack; (3) recompute icp_fit_score from "Score the fit once enriched"; (4) if icp_fit_score tier is ideal and no account executive is assigned, route the account using territory rules; (5) if enrichment confidence is low, post an enrichment summary to data quality slack for manual review.

## Step 4: Check coverage and fit mix

Compose an enrichment coverage dashboard with these panels: percentage of active accounts fully enriched, against a target of 95 percent; distribution of icp_fit_score across active accounts from "Score the fit once enriched"; enrichment API success rate, where a low rate points to vendor or domain quality issues; median time from account creation to fully enriched, against a target of 5 min for the real-time path; and ICP tier mix among new accounts as a leading indicator of targeting health. Include the unenriched backlog from "Find the accounts still blank" and the outcomes of "Enrich on creation, then daily".
