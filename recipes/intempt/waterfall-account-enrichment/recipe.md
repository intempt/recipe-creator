---
frontmatter_id: waterfall-account-enrichment
slash_command: /waterfall-account-enrichment
description: Enriches an account with a single provider. Returns a no-data status when the provider has no match.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Enriches each account in a waterfall: cheap provider first, then a specialist and AI research only when data is
    missing, recording which tier filled it and a daily cost-mix summary.'
  parameters:
  - name: stale_days
    type: duration
    label: Refresh accounts with no enrichment update in
    default: 90 d
    required: false
  - name: primary_provider_name
    type: string
    label: Primary (cheap, broad coverage) enrichment provider
    default: Apollo
    required: false
  - name: secondary_provider_name
    type: string
    label: Secondary (specialist) enrichment provider
    default: ZoomInfo
    required: false
  - name: tech_stack_provider_name
    type: string
    label: Specialist provider for tech stack
    default: BuiltWith
    required: false
  requirements:
  - slot: account_created_event
    kind: event
    meaning: A new account was created
  - slot: enrichment_primary_integration
    kind: integration
    meaning: Connection to the primary account enrichment provider
    channel: email
  - slot: enrichment_secondary_integration
    kind: integration
    meaning: Connection to the specialist enrichment provider for decision-makers and missing fields
    channel: email
  - slot: account_enrichment_updated_attribute
    kind: attribute
    meaning: Date of the last enrichment update on an account
  - slot: account_enrichment_record
    kind: attribute
    meaning: 'Account fields that receive enriched data: company name, size, industry, tech stack, revenue band, decision-makers,
      funding, and enrichment source and confidence'
  - slot: stale_accounts_segment
    kind: segment
    meaning: Accounts with no enrichment update in the stale window
    creatable: true
    definition: accounts with no enrichment update in the last {stale_days}
  steps:
  - id: s1
    builds: automation
    uses:
    - account_created_event
    - stale_accounts_segment
    - stale_days
    instruction: 'Create a workflow named ''Waterfall account enrichment'' that triggers when {account_created_event} occurs
      or on a scheduled refresh for accounts in {stale_accounts_segment} (no enrichment update in {stale_days}). Goal: maximize
      fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost
      by querying premium providers only when cheaper ones fail.'
  - id: s2
    builds: automation
    uses:
    - s1
    - enrichment_primary_integration
    - primary_provider_name
    - account_enrichment_record
    instruction: 'Within the workflow from "Waterfall account enrichment", configure the first enrichment step to query {primary_provider_name}
      through {enrichment_primary_integration}. Targets: company name, size, industry, tech stack, revenue band, key decision-makers.
      Write outputs to {account_enrichment_record}. Mark which fields were successfully filled to inform downstream branching.'
  - id: s3
    builds: automation
    uses:
    - s2
    - account_enrichment_record
    instruction: 'After "Try the cheap provider first", add a branch: if all required fields are filled (company size, industry,
      tech stack, decision-maker, valid email format) skip directly to AI fit scoring. Otherwise, if any of decision-maker,
      tech stack, or email format is missing, continue to the secondary provider step.'
  - id: s4
    builds: automation
    uses:
    - s3
    - enrichment_secondary_integration
    - secondary_provider_name
    - tech_stack_provider_name
    - account_enrichment_record
    instruction: On the missing-data branch from "Stop if nothing is missing", configure a second enrichment step querying
      {secondary_provider_name} for decision-makers and missing contact fields, and {tech_stack_provider_name} for tech stack.
      Only fill fields the primary step missed; do not re-query fields already filled. Write results to {account_enrichment_record}.
  - id: s5
    builds: agent
    uses:
    - s2
    - s4
    - account_enrichment_record
    instruction: 'After "Fall through to a specialist", if a key field is still missing, run an AI research step: scrape the
      company website, summarize what the company does, identify likely buyer personas from About, Team and Leadership pages,
      and look up recent news for funding and hiring signals. Return structured output: industry, ICP-fit description, and
      3 to 5 decision-maker names with titles. Write results to {account_enrichment_record}.'
  - id: s6
    builds: attribute
    uses:
    - s2
    - s4
    - s5
    - account_enrichment_record
    instruction: Add an update step that writes all enriched data back to {account_enrichment_record}. Set metadata field
      enrichment_source_used to primary, secondary, or ai-research based on the tier that filled the data, and set enrichment_confidence
      to high, medium, or low based on which tier filled the data. Use the results from "Try the cheap provider first", "Fall
      through to a specialist", "Research the long tail", and "Fill the gaps at lowest cost".
  - id: s7
    builds: report
    uses:
    - s1
    - s6
    instruction: Validate the workflow graph from "Waterfall account enrichment" and publish it for live execution. Create
      a daily summary report of enrichment tier usage so RevOps can monitor cost, showing the share of accounts filled at
      the primary, secondary, and AI-research tiers (for example 80% primary, 15% secondary, 5% AI research indicates a healthy
      cost profile).
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
