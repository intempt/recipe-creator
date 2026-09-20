---
name: conditional-enrichment-by-tier
description: Use when a user mentions "conditional enrichment by tier", "tiered enrichment workflow", "cost-aware enrichment", or asks for related help. Multi-split enrichment by ICP tier, premium accounts get the full enrichment cascade (multiple providers + AI research), mid-market gets standard enrichment (single provider), low-fit accounts get basic firmographic only. Saves 60-80% on enrichment credits versus blanket enrichment.
arguments: []
intempt:
  id: conditional-enrichment-by-tier
  title: "Enrich by account tier"
  version: 1.0.0
  slashCommand: /conditional-enrichment-by-tier
  group: Workflows
  shortDescription: "Spends enrichment credits in proportion to the account: everything on the enterprise ones, a standard package mid market, and nothing more on poor fits."
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
      title: "Stop enriching everything alike"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Runs on account creation and spends credits in proportion to the value of the account, instead of the blanket enrichment that burns budget on accounts that never convert."
      prompt: 'Create a workflow ''Conditional enrichment by tier'' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern: most teams blanket-enrich, which burns budget on accounts that don''t convert.'
    - step: 2
      title: "Buy the cheapest look first"
      command: configure_enrich_step
      produces: step
      bindsAs: quick_lookup
      dependsOn:
      - workflow
      description: "One or two credits for company size, industry, country and domain reputation, from the cheapest provider. Just enough to decide which tier the account belongs in."
      prompt: Configure a cheap initial enrichment step, basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record.
    - step: 3
      title: "Sort into three tiers"
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: tier_split
      dependsOn:
      - workflow
      - quick_lookup
      description: "Enterprise is over 500 staff, on the target account list, or an enterprise domain. Mid market is 50 to 500 in a target industry. Everything else is marked low fit and gets nothing more."
      prompt: 'Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain (full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries) standard enrichment. LOW-FIT branch: everything else: skip further enrichment, mark as deprioritized.'
    - step: 4
      title: "Go deep on enterprise"
      command: configure_enrich_step
      produces: step
      bindsAs: enterprise_enrich
      dependsOn:
      - workflow
      - tier_split
      description: "Premium providers, full technographics, every decision maker and title, funding history and recent news. It costs 15 to 25 credits a record, which is why it is kept for accounts that justify it."
      prompt: Configure the enterprise-branch enrichment, premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend.
    - step: 5
      title: "Research the strategic angle"
      command: configure_ai_research_step
      produces: step
      bindsAs: enterprise_ai
      dependsOn:
      - workflow
      - enterprise_enrich
      description: "Enterprise accounts only: their current priorities, how they position against rivals, and the buying signals unique to them. The 30 minutes of research an SDR would do, in two."
      prompt: On the enterprise branch only, add an AI research step for the strategic angle, recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it.
    - step: 6
      title: "Keep mid market standard"
      command: configure_enrich_step
      produces: step
      bindsAs: mid_enrich
      dependsOn:
      - workflow
      - tier_split
      description: "One mid tier provider, the main contact or founder, and the tech stack at company level rather than per person. Five to eight credits a record."
      prompt: Configure the mid-market-branch enrichment, single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record.
    - step: 7
      title: "Publish and track the saving"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - enterprise_ai
      - mid_enrich
      description: "Validated and published, with a monthly report of credits spent per tier, which usually shows the whole account base covered for 30 to 40% of what blanket enrichment costs."
      prompt: Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier, typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report.
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Enrich by account tier

Spends enrichment credits in proportion to the account: everything on the enterprise ones, a standard package mid market, and nothing more on poor fits.

## Before you run it

- Send the `account_created` event

## What it does

1. **Stop enriching everything alike** (`create_workflow`)

   Runs on account creation and spends credits in proportion to the value of the account, instead of the blanket enrichment that burns budget on accounts that never convert.

2. **Buy the cheapest look first** (`configure_enrich_step`)

   One or two credits for company size, industry, country and domain reputation, from the cheapest provider. Just enough to decide which tier the account belongs in.

3. **Sort into three tiers** (`configure_workflow_multi_split_step`)

   Enterprise is over 500 staff, on the target account list, or an enterprise domain. Mid market is 50 to 500 in a target industry. Everything else is marked low fit and gets nothing more.

4. **Go deep on enterprise** (`configure_enrich_step`)

   Premium providers, full technographics, every decision maker and title, funding history and recent news. It costs 15 to 25 credits a record, which is why it is kept for accounts that justify it.

5. **Research the strategic angle** (`configure_ai_research_step`)

   Enterprise accounts only: their current priorities, how they position against rivals, and the buying signals unique to them. The 30 minutes of research an SDR would do, in two.

6. **Keep mid market standard** (`configure_enrich_step`)

   One mid tier provider, the main contact or founder, and the tech stack at company level rather than per person. Five to eight credits a record.

7. **Publish and track the saving** (`publish_workflow`)

   Validated and published, with a monthly report of credits spent per tier, which usually shows the whole account base covered for 30 to 40% of what blanket enrichment costs.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
