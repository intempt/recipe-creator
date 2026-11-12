---
frontmatter_id: conditional-enrichment-by-tier
slash_command: /conditional-enrichment-by-tier
description: Routes accounts by ICP tier and runs enrichment only on the tiers you choose. Provider selection stays the same across all branches.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Enriches new accounts in tiers by fit, so enrichment credits go mostly to high-value accounts, with a monthly report
    of credits used per tier.
  parameters:
  - name: trigger_event
    type: string
    label: Trigger event
    default: account_created
    required: false
  - name: enterprise_min_company_size
    type: number
    label: Enterprise minimum company size (employees, exclusive)
    default: 500
    required: false
  - name: mid_market_min_company_size
    type: number
    label: Mid-market minimum company size
    default: 50
    required: false
  - name: mid_market_max_company_size
    type: number
    label: Mid-market maximum company size
    default: 500
    required: false
  - name: cost_report_window
    type: duration
    label: Cost report cadence
    default: 30 d
    required: false
  requirements:
  - slot: account_created_event
    kind: event
    meaning: An account was created
    properties:
    - name: company_size
      type: number
      meaning: Number of employees at the company
      optional: false
    - name: industry
      type: string
      meaning: Industry of the company
      optional: false
    - name: country
      type: string
      meaning: Country of the company
      optional: false
    - name: domain
      type: string
      meaning: Company web domain
      optional: false
  - slot: target_account_list
    kind: segment
    meaning: Accounts on the target account list
  - slot: target_industries
    kind: segment
    meaning: Accounts in the target industries
  - slot: enterprise_domain_list
    kind: segment
    meaning: Accounts with an enterprise domain
  - slot: cheap_enrichment_provider
    kind: integration
    meaning: A low-cost firmographic enrichment provider connection
    channel: email
  - slot: premium_enrichment_provider
    kind: integration
    meaning: A premium enrichment provider connection for deep company and people data
    channel: email
  - slot: mid_tier_enrichment_provider
    kind: integration
    meaning: A single mid-tier enrichment provider connection
    channel: email
  - slot: ai_research_knowledge
    kind: knowledge
    meaning: Knowledge source for AI account research on strategic priorities and competitive positioning
    optional: true
  - slot: enrichment_cost_report_destination
    kind: destination
    meaning: Destination where the monthly enrichment cost report is delivered
    optional: true
    channel: email
  steps:
  - id: s1
    builds: workflow
    instruction: 'Create a workflow named ''Conditional enrichment by tier'', triggered by {account_created_event}. Goal:
      spend enrichment credits only in proportion to account value rather than blanket-enriching every account.'
  - id: s2
    builds: workflow
    uses:
    - account_created_event
    - cheap_enrichment_provider
    - s1
    instruction: 'Within ''Conditional enrichment by tier'', add a basic firmographic enrichment step using {cheap_enrichment_provider}.
      Retrieve only company size, industry, country and domain reputation for {account_created_event.company_size}, {account_created_event.industry},
      {account_created_event.country} and {account_created_event.domain}. Purpose: determine the account''s tier. Expected
      cost is about 1-2 credits per record.'
  - id: s3
    builds: workflow
    uses:
    - target_account_list
    - target_industries
    - enterprise_domain_list
    - enterprise_min_company_size
    - mid_market_min_company_size
    - mid_market_max_company_size
    - s1
    - s2
    instruction: 'Within ''Conditional enrichment by tier'', add a multi-split step using the result of ''Buy the cheapest
      look first'' with three branches. ENTERPRISE branch: company size greater than {enterprise_min_company_size}, OR account
      is in {target_account_list}, OR account is in {enterprise_domain_list}. MID-MARKET branch: company size from {mid_market_min_company_size}
      to {mid_market_max_company_size} AND account is in {target_industries}. LOW-FIT branch: all other accounts; take no
      further enrichment and mark the account as deprioritized.'
  - id: s4
    builds: workflow
    uses:
    - premium_enrichment_provider
    - s1
    - s3
    instruction: 'In the ENTERPRISE branch of ''Sort into three tiers'', run full enrichment using {premium_enrichment_provider}:
      deep technographic data, a full decision-maker map with multiple titles per account, funding history and recent news.
      Expected cost is 15-25 credits per record; reserve this for high-value accounts only.'
  - id: s5
    builds: workflow
    uses:
    - ai_research_knowledge
    - s1
    - s4
    instruction: On the ENTERPRISE branch only, after 'Go deep on enterprise', add an AI research step using {ai_research_knowledge}
      covering the account's strategic angle, recent priorities, competitive positioning and unique buying signals. Produce
      a concise brief per account in about two minutes of processing.
  - id: s6
    builds: workflow
    uses:
    - mid_tier_enrichment_provider
    - s1
    - s3
    instruction: 'In the MID-MARKET branch of ''Sort into three tiers'', run standard enrichment using {mid_tier_enrichment_provider}:
      one basic decision-maker lookup (CEO, founder or main contact) and company-level tech stack (not per person). Expected
      cost is 5-8 credits per record.'
  - id: s7
    builds: report
    uses:
    - enrichment_cost_report_destination
    - cost_report_window
    - s1
    - s5
    - s6
    instruction: Validate the workflow graph for 'Conditional enrichment by tier' and publish it. Add a cost-tracking report,
      delivered every {cost_report_window}, showing credits consumed per tier (ENTERPRISE, MID-MARKET, LOW-FIT) so the team
      can compare spend against blanket enrichment.
---

# Enrich by account tier

Slash command: /conditional-enrichment-by-tier

## Step 1: Stop enriching everything alike

Create a workflow 'Conditional enrichment by tier' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern: most teams blanket-enrich, which burns budget on accounts that don't convert.

## Step 2: Buy the cheapest look first

This step builds a workflow.
Configure a cheap initial enrichment step, basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record. Use the result of "Stop enriching everything alike".

## Step 3: Sort into three tiers

This step builds a workflow.
Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain (full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries) standard enrichment. LOW-FIT branch: everything else: skip further enrichment, mark as deprioritized. Use the result of "Stop enriching everything alike", "Buy the cheapest look first".

## Step 4: Go deep on enterprise

This step builds a workflow.
Configure the enterprise-branch enrichment, premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend. Use the result of "Stop enriching everything alike", "Sort into three tiers".

## Step 5: Research the strategic angle

This step builds a workflow.
On the enterprise branch only, add an AI research step for the strategic angle, recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it. Use the result of "Stop enriching everything alike", "Go deep on enterprise".

## Step 6: Keep mid market standard

This step builds a workflow.
Configure the mid-market-branch enrichment, single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record. Use the result of "Stop enriching everything alike", "Sort into three tiers".

## Step 7: Publish and track the saving

Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier, typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report. Use the result of "Stop enriching everything alike", "Research the strategic angle", "Keep mid market standard".
