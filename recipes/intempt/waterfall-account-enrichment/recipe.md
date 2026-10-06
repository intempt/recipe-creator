---
id: waterfall-account-enrichment
title: Waterfall account enrichment
slash_command: /waterfall-account-enrichment
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Enriches an account with a single provider. Returns a no-data status when the provider has no match.
description: >-
  Single-provider account enrichment workflow. It calls one enrichment provider and returns a clear no-data
  status if no record is found. It does not cascade across providers or track per-record cost.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
  industry:
    - ai
    - b2b-saas
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - enrichment
    - waterfall
    - data-quality
prerequisites:
  events:
    - value: account_created
      severity: blocking
  integrations:
    - value: enrichment_provider
      severity: blocking
touches:
  reads:
    - The account_created event in your project
    - Your connected enrichment provider
  writes:
    - A new workflow, from step 1 "Fill the gaps at lowest cost"
    - A new workflow, from step 2 "Try the cheap provider first"
    - A new workflow, from step 3 "Stop if nothing is missing"
    - A new workflow, from step 4 "Fall through to a specialist"
    - A new workflow, from step 5 "Research the long tail"
    - A new workflow, from step 6 "Record what it cost to find"
    - A new workflow, from step 7 "Publish and watch the mix"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Fill the gaps at lowest cost
    summary: >-
      Runs on account creation, and again on a schedule for accounts untouched for 90 days. The aim is
      to fill firmographics, technographics, decision makers and funding as completely as possible while
      only reaching for premium providers when the cheaper ones come up short.
    builds: workflow
    description: >-
      Create a workflow 'Waterfall account enrichment' triggered by account_created OR scheduled refresh
      for stale accounts (no enrichment update in 90 days). Goal: maximize fill rate on key account attributes
      (firmographics, technographics, decision-makers, funding) while minimizing cost by querying premium
      providers only when cheaper ones fail.
  - id: s2
    title: Try the cheap provider first
    summary: >-
      The primary provider, usually the cheapest with broad coverage, is asked for company name, size,
      industry, tech stack, revenue band and key decision makers. Whatever it fills is marked, so the
      later steps know what is still missing.
    builds: workflow
    description: >-
      Configure first enrichment step to query the primary provider (configurable: typically the cheapest
      provider with broad coverage, e.g. Apollo or Clearbit). Targets: company name, size, industry, tech
      stack, revenue band, key decision-makers. Outputs to account attributes. Mark fields successfully
      filled to inform downstream branching. Use the result of "Fill the gaps at lowest cost".
    dependsOn:
      - s1
  - id: s3
    title: Stop if nothing is missing
    summary: >-
      If the required fields came back filled, it goes straight to scoring. If the email format, the decision
      makers or the tech stack are still blank, it falls through to the next provider. This branch is
      where the money is saved.
    builds: workflow
    description: >-
      Branch step: did the primary enrichment fill the required fields? If YES to skip to AI-fit-scoring.
      If NO (missing email format, missing decision-maker, or missing tech stack) to continue to secondary
      provider. Saves money by not paying for premium providers unless needed. Use the result of "Fill
      the gaps at lowest cost", "Try the cheap provider first".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Fall through to a specialist
    summary: >-
      Only on the branch with gaps. A second provider, usually a specialist in whatever is missing, fills
      those fields and only those, without re-buying anything already known.
    builds: workflow
    description: >-
      Configure second enrichment step that fires only on the no-coverage branch. Query secondary provider
      (configurable, typically a specialist provider for the missing field type, e.g. ZoomInfo for decision-makers,
      BuiltWith for tech stack). Only fills fields the primary missed; doesn't re-query already-filled
      fields. Use the result of "Fill the gaps at lowest cost", "Stop if nothing is missing".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Research the long tail
    summary: >-
      When the second provider also comes up short, it reads the company website, summarises what they
      do, works out the likely buyers from the about and leadership pages, and looks up recent funding
      and hiring news, returning the industry, a fit description, and three to five names with titles.
      This is for the accounts no data provider covers.
    builds: workflow
    description: >-
      Configure AI research step that fires when secondary provider also fails to fill a key field. Tasks:
      scrape the company website, summarize what the company does, identify likely buyer personas from
      About/Team/Leadership pages, look up recent news for funding/hiring signals. Returns structured
      output (industry, ICP-fit description, 3-5 decision-maker names with titles). The Claygent-equivalent
      for the long tail where structured providers have no data. Use the result of "Fill the gaps at lowest
      cost", "Fall through to a specialist".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Record what it cost to find
    summary: >-
      Everything is written back to the account, along with which tier supplied it, primary, secondary
      or AI research, so RevOps can audit the cost per record, plus a confidence level based on where
      the data came from.
    builds: workflow
    description: >-
      Configure the update step that writes all enriched data back to the Account record. Includes a metadata
      field 'enrichment_source_used' (primary / secondary / ai-research) so RevOps can audit cost per
      record. Also writes enrichment_confidence (high/medium/low based on which tier filled the data).
      Use the result of "Fill the gaps at lowest cost", "Try the cheap provider first", "Fall through
      to a specialist", "Research the long tail".
    dependsOn:
      - s1
      - s2
      - s4
      - s5
  - id: s7
    title: Publish and watch the mix
    summary: >-
      Validated and published, with a daily summary of which tier filled what. A healthy profile looks
      like 80% at the primary tier, 15% at the secondary and 5% needing research.
    builds: workflow
    description: >-
      Validate the workflow DAG and publish for live execution. Set up a daily summary of enrichment-tier-usage
      so RevOps can monitor cost (e.g. '80% filled at primary tier, 15% at secondary, 5% needed AI research'
      = healthy cost profile). Use the result of "Fill the gaps at lowest cost", "Record what it cost
      to find".
    dependsOn:
      - s1
      - s6
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s6
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Waterfall account enrichment

Enriches an account with a single provider. Returns a no-data status when the provider has no match.

## Steps

1. **Fill the gaps at lowest cost** (builds workflow)

   Runs on account creation, and again on a schedule for accounts untouched for 90 days. The aim is to fill firmographics, technographics, decision makers and funding as completely as possible while only reaching for premium providers when the cheaper ones come up short.

2. **Try the cheap provider first** (builds workflow)

   The primary provider, usually the cheapest with broad coverage, is asked for company name, size, industry, tech stack, revenue band and key decision makers. Whatever it fills is marked, so the later steps know what is still missing.

3. **Stop if nothing is missing** (builds workflow)

   If the required fields came back filled, it goes straight to scoring. If the email format, the decision makers or the tech stack are still blank, it falls through to the next provider. This branch is where the money is saved.

4. **Fall through to a specialist** (builds workflow)

   Only on the branch with gaps. A second provider, usually a specialist in whatever is missing, fills those fields and only those, without re-buying anything already known.

5. **Research the long tail** (builds workflow)

   When the second provider also comes up short, it reads the company website, summarises what they do, works out the likely buyers from the about and leadership pages, and looks up recent funding and hiring news, returning the industry, a fit description, and three to five names with titles. This is for the accounts no data provider covers.

6. **Record what it cost to find** (builds workflow)

   Everything is written back to the account, along with which tier supplied it, primary, secondary or AI research, so RevOps can audit the cost per record, plus a confidence level based on where the data came from.

7. **Publish and watch the mix** (builds workflow)

   Validated and published, with a daily summary of which tier filled what. A healthy profile looks like 80% at the primary tier, 15% at the secondary and 5% needing research.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- The account_created event in your project
- Your connected enrichment provider

Writes:

- A new workflow, from step 1 "Fill the gaps at lowest cost"
- A new workflow, from step 2 "Try the cheap provider first"
- A new workflow, from step 3 "Stop if nothing is missing"
- A new workflow, from step 4 "Fall through to a specialist"
- A new workflow, from step 5 "Research the long tail"
- A new workflow, from step 6 "Record what it cost to find"
- A new workflow, from step 7 "Publish and watch the mix"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
