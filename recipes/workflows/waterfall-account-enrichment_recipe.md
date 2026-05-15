---
name: waterfall-account-enrichment
description: Use when a user mentions "waterfall account enrichment", "multi-source enrichment cascade", "fallback enrichment workflow", or asks for related help. Multi-source enrichment cascade — try primary provider, if it misses fall through to secondary, then tertiary, then AI-research fallback for unstructured discovery. Maximizes coverage while minimizing per-record cost. The Clay-style waterfall pattern.
arguments: []
intempt:
  id: waterfall-account-enrichment
  version: 1.0.0
  slashCommand: /waterfall-account-enrichment
  group: Workflows
  shortDescription: "Multi-source enrichment cascade — try primary provider, if it misses fall through to secondary, then tertiary, then AI-research fallback for unstructured discovery. Maximizes coverage while minimizing per-record cost. The Clay-style waterfall pattern."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [enrichment, waterfall, data-quality]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: account_created, severity: blocking }
    integrations:
      - { value: enrichment_provider, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_enrich_step
    - configure_workflow_branch_step
    - configure_ai_research_step
    - configure_update_attribute_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Waterfall Enrichment Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Waterfall account enrichment'' triggered by account_created OR scheduled refresh for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail.'
      prompt: 'Create a workflow ''Waterfall account enrichment'' triggered by account_created OR scheduled refresh for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail.'
    - step: 2
      title: Primary Enrichment Pass
      command: configure_enrich_step
      produces: step
      bindsAs: primary_enrich
      dependsOn:
      - workflow
      description: 'Configure first enrichment step to query the primary provider (configurable — typically the cheapest provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully filled to inform downstream branching.'
      prompt: 'Configure first enrichment step to query the primary provider (configurable — typically the cheapest provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully filled to inform downstream branching.'
    - step: 3
      title: Branch on Primary Coverage
      command: configure_workflow_branch_step
      produces: step
      bindsAs: coverage_check
      dependsOn:
      - workflow
      - primary_enrich
      description: 'Branch step: did the primary enrichment fill the required fields? If YES → skip to AI-fit-scoring. If NO (missing email format, missing decision-maker, or missing tech stack) → continue to secondary provider. Saves money by not paying for premium providers unless needed.'
      prompt: 'Branch step: did the primary enrichment fill the required fields? If YES → skip to AI-fit-scoring. If NO (missing email format, missing decision-maker, or missing tech stack) → continue to secondary provider. Saves money by not paying for premium providers unless needed.'
    - step: 4
      title: Secondary Enrichment Pass
      command: configure_enrich_step
      produces: step
      bindsAs: secondary_enrich
      dependsOn:
      - workflow
      - coverage_check
      description: Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider (configurable — typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers, BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled fields.
      prompt: Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider (configurable — typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers, BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled fields.
    - step: 5
      title: AI Research Fallback
      command: configure_ai_research_step
      produces: step
      bindsAs: ai_research
      dependsOn:
      - workflow
      - secondary_enrich
      description: 'Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks: scrape the company website, summarize what the company does, identify likely buyer personas from About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent for the long tail where structured providers have no data.'
      prompt: 'Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks: scrape the company website, summarize what the company does, identify likely buyer personas from About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent for the long tail where structured providers have no data.'
    - step: 6
      title: Update Account Record
      command: configure_update_attribute_step
      produces: step
      bindsAs: update_account
      dependsOn:
      - workflow
      - primary_enrich
      - secondary_enrich
      - ai_research
      description: Configure the update step that writes all enriched data back to the Account record. Includes a metadata field 'enrichment_source_used' (primary / secondary / ai-research) so RevOps can audit cost per record. Also writes enrichment_confidence (high/medium/low based on which tier filled the data).
      prompt: Configure the update step that writes all enriched data back to the Account record. Includes a metadata field 'enrichment_source_used' (primary / secondary / ai-research) so RevOps can audit cost per record. Also writes enrichment_confidence (high/medium/low based on which tier filled the data).
    - step: 7
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - update_account
      description: Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research' = healthy cost profile).
      prompt: Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research' = healthy cost profile).
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Waterfall Account Enrichment

## Procedure

1. **Build the Waterfall Enrichment Workflow** [`create_workflow`] — Create a workflow 'Waterfall account enrichment' triggered by account_created OR scheduled refresh for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail. → produces: workflow
2. **Primary Enrichment Pass** [`configure_enrich_step`] — Configure first enrichment step to query the primary provider (configurable — typically the cheapest provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully filled to inform downstream branching. → produces: step
3. **Branch on Primary Coverage** [`configure_workflow_branch_step`] — Branch step: did the primary enrichment fill the required fields? If YES → skip to AI-fit-scoring. If NO (missing email format, missing decision-maker, or missing tech stack) → continue to secondary provider. Saves money by not paying for premium providers unless needed. → produces: step
4. **Secondary Enrichment Pass** [`configure_enrich_step`] — Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider (configurable — typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers, BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled fields. → produces: step
5. **AI Research Fallback** [`configure_ai_research_step`] — Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks: scrape the company website, summarize what the company does, identify likely buyer personas from About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent for the long tail where structured providers have no data. → produces: step
6. **Update Account Record** [`configure_update_attribute_step`] — Configure the update step that writes all enriched data back to the Account record. Includes a metadata field 'enrichment_source_used' (primary / secondary / ai-research) so RevOps can audit cost per record. Also writes enrichment_confidence (high/medium/low based on which tier filled the data). → produces: step
7. **Validate and Publish** [`publish_workflow`] — Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research' = healthy cost profile). → produces: workflow
