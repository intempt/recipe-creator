---
id: conditional-enrichment-by-tier
title: Enrich by account tier
slash_command: /conditional-enrichment-by-tier
group: Workflows
owner: intempt
summary: 'Spends enrichment credits in proportion to the account: everything on the enterprise ones, a
  standard package mid market, and nothing more on poor fits.'
description: >-
  Multi-split enrichment by ICP tier, premium accounts get the full enrichment cascade (multiple providers
  + AI research), mid-market gets standard enrichment (single provider), low-fit accounts get basic firmographic
  only. Saves 60-80% on enrichment credits versus blanket enrichment.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - enrichment
    - cost-control
    - tiered-routing
prerequisites:
  events:
    - value: account_created
      severity: blocking
touches:
  reads:
    - The account_created event in your project
  writes:
    - A new workflow, from step 1 "Stop enriching everything alike"
    - A new workflow, from step 2 "Buy the cheapest look first"
    - A new workflow, from step 3 "Sort into three tiers"
    - A new workflow, from step 4 "Go deep on enterprise"
    - A new workflow, from step 5 "Research the strategic angle"
    - A new workflow, from step 6 "Keep mid market standard"
    - A new workflow, from step 7 "Publish and track the saving"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Stop enriching everything alike
    summary: >-
      Runs on account creation and spends credits in proportion to the value of the account, instead of
      the blanket enrichment that burns budget on accounts that never convert.
    builds: workflow
    description: >-
      Create a workflow 'Conditional enrichment by tier' triggered by account_created. Goal: only spend
      enrichment credits proportional to account value. The cost-saving Clay pattern: most teams blanket-enrich,
      which burns budget on accounts that don't convert.
  - id: s2
    title: Buy the cheapest look first
    summary: >-
      One or two credits for company size, industry, country and domain reputation, from the cheapest
      provider. Just enough to decide which tier the account belongs in.
    builds: workflow
    description: >-
      Configure a cheap initial enrichment step, basic firmographics only (company size, industry, country,
      domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account
      falls into. Costs about 1-2 credits per record. Use the result of "Stop enriching everything alike".
    dependsOn:
      - s1
  - id: s3
    title: Sort into three tiers
    summary: >-
      Enterprise is over 500 staff, on the target account list, or an enterprise domain. Mid market is
      50 to 500 in a target industry. Everything else is marked low fit and gets nothing more.
    builds: workflow
    description: >-
      Configure a multi-split step routing accounts into 3 branches based on the basic firmographics +
      any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR
      enterprise domain (full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target
      industries) standard enrichment. LOW-FIT branch: everything else: skip further enrichment, mark
      as deprioritized. Use the result of "Stop enriching everything alike", "Buy the cheapest look first".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Go deep on enterprise
    summary: >-
      Premium providers, full technographics, every decision maker and title, funding history and recent
      news. It costs 15 to 25 credits a record, which is why it is kept for accounts that justify it.
    builds: workflow
    description: >-
      Configure the enterprise-branch enrichment, premium providers, deep technographic, full decision-maker
      map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record
      but reserved only for high-value accounts where the data justifies the spend. Use the result of
      "Stop enriching everything alike", "Sort into three tiers".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Research the strategic angle
    summary: >-
      Enterprise accounts only: their current priorities, how they position against rivals, and the buying
      signals unique to them. The 30 minutes of research an SDR would do, in two.
    builds: workflow
    description: >-
      On the enterprise branch only, add an AI research step for the strategic angle, recent priorities,
      competitive positioning, unique buying signals. The kind of research a human SDR would spend 30
      minutes on, done in 2 minutes for accounts that warrant it. Use the result of "Stop enriching everything
      alike", "Go deep on enterprise".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Keep mid market standard
    summary: >-
      One mid tier provider, the main contact or founder, and the tech stack at company level rather than
      per person. Five to eight credits a record.
    builds: workflow
    description: >-
      Configure the mid-market-branch enrichment, single mid-tier provider, basic decision-maker (CEO/founder/main
      contact), tech stack at company level (not per-person). Costs 5-8 credits per record. Use the result
      of "Stop enriching everything alike", "Sort into three tiers".
    dependsOn:
      - s1
      - s3
  - id: s7
    title: Publish and track the saving
    summary: >-
      Validated and published, with a monthly report of credits spent per tier, which usually shows the
      whole account base covered for 30 to 40% of what blanket enrichment costs.
    builds: workflow
    description: >-
      Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per
      tier, typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps
      loves this report. Use the result of "Stop enriching everything alike", "Research the strategic
      angle", "Keep mid market standard".
    dependsOn:
      - s1
      - s5
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

# Enrich by account tier

Spends enrichment credits in proportion to the account: everything on the enterprise ones, a standard package mid market, and nothing more on poor fits.

## Steps

1. **Stop enriching everything alike** (builds workflow)

   Runs on account creation and spends credits in proportion to the value of the account, instead of the blanket enrichment that burns budget on accounts that never convert.

2. **Buy the cheapest look first** (builds workflow)

   One or two credits for company size, industry, country and domain reputation, from the cheapest provider. Just enough to decide which tier the account belongs in.

3. **Sort into three tiers** (builds workflow)

   Enterprise is over 500 staff, on the target account list, or an enterprise domain. Mid market is 50 to 500 in a target industry. Everything else is marked low fit and gets nothing more.

4. **Go deep on enterprise** (builds workflow)

   Premium providers, full technographics, every decision maker and title, funding history and recent news. It costs 15 to 25 credits a record, which is why it is kept for accounts that justify it.

5. **Research the strategic angle** (builds workflow)

   Enterprise accounts only: their current priorities, how they position against rivals, and the buying signals unique to them. The 30 minutes of research an SDR would do, in two.

6. **Keep mid market standard** (builds workflow)

   One mid tier provider, the main contact or founder, and the tech stack at company level rather than per person. Five to eight credits a record.

7. **Publish and track the saving** (builds workflow)

   Validated and published, with a monthly report of credits spent per tier, which usually shows the whole account base covered for 30 to 40% of what blanket enrichment costs.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- The account_created event in your project

Writes:

- A new workflow, from step 1 "Stop enriching everything alike"
- A new workflow, from step 2 "Buy the cheapest look first"
- A new workflow, from step 3 "Sort into three tiers"
- A new workflow, from step 4 "Go deep on enterprise"
- A new workflow, from step 5 "Research the strategic angle"
- A new workflow, from step 6 "Keep mid market standard"
- A new workflow, from step 7 "Publish and track the saving"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
