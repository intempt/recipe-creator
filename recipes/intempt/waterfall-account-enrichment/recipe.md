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
visibility: draft
rejected: Its purpose is filling account fields from paid third-party enrichment providers in a cost waterfall plus per-account
  web research; provider enrichment writes and research agents are not a Blu recipe capability.
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
---

# Waterfall account enrichment

Slash command: /waterfall-account-enrichment

## Step 1: Fill the gaps at lowest cost

Create a workflow named 'Waterfall account enrichment' that triggers when account created event occurs or on a scheduled refresh for accounts in stale accounts segment (no enrichment update in 90 d). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail.
