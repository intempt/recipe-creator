---
name: conditional-enrichment-by-tier
description: Use when a user mentions "conditional enrichment by tier", "tiered enrichment workflow", "cost-aware enrichment", or asks for related help. Multi-split enrichment by ICP tier — premium accounts get the full enrichment cascade (multiple providers + AI research), mid-market gets standard enrichment (single provider), low-fit accounts get basic firmographic only. Saves 60-80% on enrichment credits versus blanket enrichment.
arguments: []
intempt:
  id: conditional-enrichment-by-tier
  version: 1.0.0
  slashCommand: /conditional-enrichment-by-tier
  group: Workflows
  shortDescription: 'Multi-split enrichment by ICP tier: premium accounts get the full enrichment cascade (multiple providers + AI research), mid-market gets standard enrichment (single provider), low-fit accounts get basic firmographic only. Saves 60-80% on enrichment credits versus blanket enrichment.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [enrichment, cost-control, tiered-routing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: account_created, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_enrich_step
    - configure_workflow_multi_split_step
    - configure_ai_research_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Tiered Enrichment Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Conditional enrichment by tier'' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern — most teams blanket-enrich, which burns budget on accounts that don''t convert.'
      prompt: 'Create a workflow ''Conditional enrichment by tier'' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern — most teams blanket-enrich, which burns budget on accounts that don''t convert.'
    - step: 2
      title: Quick Firmographic Lookup
      command: configure_enrich_step
      produces: step
      bindsAs: quick_lookup
      dependsOn:
      - workflow
      description: Configure a cheap initial enrichment step — basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record.
      prompt: Configure a cheap initial enrichment step — basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record.
    - step: 3
      title: Multi-Split by Tier
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: tier_split
      dependsOn:
      - workflow
      - quick_lookup
      description: 'Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain — full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries — standard enrichment. LOW-FIT branch: everything else — skip further enrichment, mark as deprioritized.'
      prompt: 'Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain — full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries — standard enrichment. LOW-FIT branch: everything else — skip further enrichment, mark as deprioritized.'
    - step: 4
      title: 'Enterprise Branch: Full Cascade'
      command: configure_enrich_step
      produces: step
      bindsAs: enterprise_enrich
      dependsOn:
      - workflow
      - tier_split
      description: Configure the enterprise-branch enrichment — premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend.
      prompt: Configure the enterprise-branch enrichment — premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend.
    - step: 5
      title: 'Enterprise Branch: AI Research'
      command: configure_ai_research_step
      produces: step
      bindsAs: enterprise_ai
      dependsOn:
      - workflow
      - enterprise_enrich
      description: On the enterprise branch only, add an AI research step for the strategic angle — recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it.
      prompt: On the enterprise branch only, add an AI research step for the strategic angle — recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it.
    - step: 6
      title: 'Mid-Market Branch: Standard Enrichment'
      command: configure_enrich_step
      produces: step
      bindsAs: mid_enrich
      dependsOn:
      - workflow
      - tier_split
      description: Configure the mid-market-branch enrichment — single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record.
      prompt: Configure the mid-market-branch enrichment — single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record.
    - step: 7
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - enterprise_ai
      - mid_enrich
      description: Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier — typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report.
      prompt: Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier — typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report.
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Conditional Enrichment By Tier

## Procedure

1. **Build the Tiered Enrichment Workflow** [`create_workflow`] — Create a workflow 'Conditional enrichment by tier' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern — most teams blanket-enrich, which burns budget on accounts that don't convert. → produces: workflow
2. **Quick Firmographic Lookup** [`configure_enrich_step`] — Configure a cheap initial enrichment step — basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record. → produces: step
3. **Multi-Split by Tier** [`configure_workflow_multi_split_step`] — Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain — full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries — standard enrichment. LOW-FIT branch: everything else — skip further enrichment, mark as deprioritized. → produces: step
4. **Enterprise Branch: Full Cascade** [`configure_enrich_step`] — Configure the enterprise-branch enrichment — premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend. → produces: step
5. **Enterprise Branch: AI Research** [`configure_ai_research_step`] — On the enterprise branch only, add an AI research step for the strategic angle — recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it. → produces: step
6. **Mid-Market Branch: Standard Enrichment** [`configure_enrich_step`] — Configure the mid-market-branch enrichment — single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record. → produces: step
7. **Validate and Publish** [`publish_workflow`] — Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier — typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report. → produces: workflow
