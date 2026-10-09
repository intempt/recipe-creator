---
name: waterfall-account-enrichment
description: Use when a user mentions "waterfall account enrichment", "multi-source enrichment cascade", "fallback enrichment workflow", or asks for related help. Multi-source enrichment cascade, try primary provider, if it misses fall through to secondary, then tertiary, then AI-research fallback for unstructured discovery. Maximizes coverage while minimizing per-record cost. The Clay-style waterfall pattern.
arguments: []
intempt:
  id: waterfall-account-enrichment
  title: "Waterfall account enrichment"
  version: 1.0.0
  slashCommand: /waterfall-account-enrichment
  group: Workflows
  shortDescription: "Tries the cheap provider first and only pays for the expensive one when a field is still missing, with AI research as the last resort."
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
      title: "Fill the gaps at lowest cost"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Runs on account creation, and again on a schedule for accounts untouched for 90 days. The aim is to fill firmographics, technographics, decision makers and funding as completely as possible while only reaching for premium providers when the cheaper ones come up short."
      prompt: 'Create a workflow ''Waterfall account enrichment'' triggered by Account created OR scheduled refresh for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium providers only when cheaper ones fail.'
    - step: 2
      title: "Try the cheap provider first"
      command: configure_enrich_step
      produces: step
      bindsAs: primary_enrich
      dependsOn:
      - workflow
      description: "The primary provider, usually the cheapest with broad coverage, is asked for company name, size, industry, tech stack, revenue band and key decision makers. Whatever it fills is marked, so the later steps know what is still missing."
      prompt: 'Configure first enrichment step to query the primary provider (configurable: typically the cheapest provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully filled to inform downstream branching.'
    - step: 3
      title: "Stop if nothing is missing"
      command: configure_workflow_branch_step
      produces: step
      bindsAs: coverage_check
      dependsOn:
      - workflow
      - primary_enrich
      description: "If the required fields came back filled, it goes straight to scoring. If the email format, the decision makers or the tech stack are still blank, it falls through to the next provider. This branch is where the money is saved."
      prompt: 'Branch step: did the primary enrichment fill the required fields? If YES to skip to AI-fit-scoring. If NO (missing email format, missing decision-maker, or missing tech stack) to continue to secondary provider. Saves money by not paying for premium providers unless needed.'
    - step: 4
      title: "Fall through to a specialist"
      command: configure_enrich_step
      produces: step
      bindsAs: secondary_enrich
      dependsOn:
      - workflow
      - coverage_check
      description: "Only on the branch with gaps. A second provider, usually a specialist in whatever is missing, fills those fields and only those, without re-buying anything already known."
      prompt: Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider (configurable, typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers, BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled fields.
    - step: 5
      title: "Research the long tail"
      command: configure_ai_research_step
      produces: step
      bindsAs: ai_research
      dependsOn:
      - workflow
      - secondary_enrich
      description: "When the second provider also comes up short, it reads the company website, summarises what they do, works out the likely buyers from the about and leadership pages, and looks up recent funding and hiring news, returning the industry, a fit description, and three to five names with titles. This is for the accounts no data provider covers."
      prompt: 'Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks: scrape the company website, summarize what the company does, identify likely buyer personas from About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent for the long tail where structured providers have no data.'
    - step: 6
      title: "Record what it cost to find"
      command: configure_update_attribute_step
      produces: step
      bindsAs: update_account
      dependsOn:
      - workflow
      - primary_enrich
      - secondary_enrich
      - ai_research
      description: "Everything is written back to the account, along with which tier supplied it, primary, secondary or AI research, so RevOps can audit the cost per record, plus a confidence level based on where the data came from."
      prompt: Configure the update step that writes all enriched data back to the Account record. Includes a metadata field 'enrichment source used' (primary / secondary / ai-research) so RevOps can audit cost per record. Also writes enrichment confidence (high/medium/low based on which tier filled the data).
    - step: 7
      title: "Publish and watch the mix"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - update_account
      description: "Validated and published, with a daily summary of which tier filled what. A healthy profile looks like 80% at the primary tier, 15% at the secondary and 5% needing research."
      prompt: Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research' = healthy cost profile).
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Waterfall account enrichment

Tries the cheap provider first and only pays for the expensive one when a field is still missing, with AI research as the last resort.

## Before you run it

- Connect enrichment_provider
- Send the `account_created` event

## What it does

1. **Fill the gaps at lowest cost** (`create_workflow`)

   Runs on account creation, and again on a schedule for accounts untouched for 90 days. The aim is to fill firmographics, technographics, decision makers and funding as completely as possible while only reaching for premium providers when the cheaper ones come up short.

2. **Try the cheap provider first** (`configure_enrich_step`)

   The primary provider, usually the cheapest with broad coverage, is asked for company name, size, industry, tech stack, revenue band and key decision makers. Whatever it fills is marked, so the later steps know what is still missing.

3. **Stop if nothing is missing** (`configure_workflow_branch_step`)

   If the required fields came back filled, it goes straight to scoring. If the email format, the decision makers or the tech stack are still blank, it falls through to the next provider. This branch is where the money is saved.

4. **Fall through to a specialist** (`configure_enrich_step`)

   Only on the branch with gaps. A second provider, usually a specialist in whatever is missing, fills those fields and only those, without re-buying anything already known.

5. **Research the long tail** (`configure_ai_research_step`)

   When the second provider also comes up short, it reads the company website, summarises what they do, works out the likely buyers from the about and leadership pages, and looks up recent funding and hiring news, returning the industry, a fit description, and three to five names with titles. This is for the accounts no data provider covers.

6. **Record what it cost to find** (`configure_update_attribute_step`)

   Everything is written back to the account, along with which tier supplied it, primary, secondary or AI research, so RevOps can audit the cost per record, plus a confidence level based on where the data came from.

7. **Publish and watch the mix** (`publish_workflow`)

   Validated and published, with a daily summary of which tier filled what. A healthy profile looks like 80% at the primary tier, 15% at the secondary and 5% needing research.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
