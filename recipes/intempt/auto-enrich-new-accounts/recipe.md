---
description: Fills in industry, size, revenue and tech stack for every new account within minutes, scores the fit, and routes the best ones to an owner.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
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
