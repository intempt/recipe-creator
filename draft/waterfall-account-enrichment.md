---
description: Enriches an account with a single provider. Returns a no-data status when the provider has no match.
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
---

# Waterfall account enrichment

Slash command: /waterfall-account-enrichment

## Step 1: Fill the gaps at lowest cost

Create a workflow 'Waterfall account enrichment' triggered by account_created OR scheduled refresh for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail.

## Step 2: Try the cheap provider first

This step builds a workflow.
Configure first enrichment step to query the primary provider (configurable: typically the cheapest provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully filled to inform downstream branching. Use the result of "Fill the gaps at lowest cost".

## Step 3: Stop if nothing is missing

This step builds a workflow.
Branch step: did the primary enrichment fill the required fields? If YES to skip to AI-fit-scoring. If NO (missing email format, missing decision-maker, or missing tech stack) to continue to secondary provider. Saves money by not paying for premium providers unless needed. Use the result of "Fill the gaps at lowest cost", "Try the cheap provider first".

## Step 4: Fall through to a specialist

This step builds a workflow.
Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider (configurable, typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers, BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled fields. Use the result of "Fill the gaps at lowest cost", "Stop if nothing is missing".

## Step 5: Research the long tail

This step builds a workflow.
Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks: scrape the company website, summarize what the company does, identify likely buyer personas from About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent for the long tail where structured providers have no data. Use the result of "Fill the gaps at lowest cost", "Fall through to a specialist".

## Step 6: Record what it cost to find

This step builds a workflow.
Configure the update step that writes all enriched data back to the Account record. Includes a metadata field 'enrichment_source_used' (primary / secondary / ai-research) so RevOps can audit cost per record. Also writes enrichment_confidence (high/medium/low based on which tier filled the data). Use the result of "Fill the gaps at lowest cost", "Try the cheap provider first", "Fall through to a specialist", "Research the long tail".

## Step 7: Publish and watch the mix

Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research' = healthy cost profile). Use the result of "Fill the gaps at lowest cost", "Record what it cost to find".
