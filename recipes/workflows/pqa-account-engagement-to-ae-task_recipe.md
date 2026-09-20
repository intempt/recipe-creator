---
name: pqa-account-engagement-to-ae-task
description: Use when a user mentions "PQA detection", "product-qualified account", "multi-user account engagement", or asks for related help. When multiple users from the same account engage with the product in a short window (PQA signal) create an AE deal-creation task with the account's full engagement picture, because account-level signals are stronger than single-user signals.
arguments: []
intempt:
  id: pqa-account-engagement-to-ae-task
  title: "Account level signal to AE task"
  version: 1.0.0
  slashCommand: /pqa-account-engagement-to-ae-task
  group: Workflows
  shortDescription: "When several people from one company start using the product in the same fortnight, it briefs an AE and asks them to open a deal."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [pqa, account-signal, ae-routing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: user_signed_up, severity: blocking }
      - { value: feature_used, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Score the whole account"
      command: create_ai_attribute
      produces: attribute
      bindsAs: pqa_score
      description: "A 0 to 100 score per account from how many different people were active in the last 14 days, where three or more is a strong signal, the total feature events across them, whether any look like decision makers by title or email pattern, and how deeply the team uses it. 70 and above counts as qualified, updated daily and whenever someone new signs up from the domain."
      prompt: 'Create an AI-derived attribute ''pqa_score'' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain.'
    - step: 2
      title: "Find accounts crossing 70"
      command: create_segment
      produces: segment
      bindsAs: pqa_segment
      dependsOn:
      - pqa_score
      description: "Accounts that crossed 70 in the last 14 days with no open deal and no AE engaged in the last 60 days. Existing paying customers are left out, because expansion is a different play."
      prompt: 'Build a segment ''PQA: accounts score >= 70'' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion: see seat-expansion workflow).'
    - step: 3
      title: "Brief an AE to open a deal"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pqa_score
      - pqa_segment
      description: "On crossing 70 it refreshes the account's firmographics, technographics and decision maker contacts, writes a summary of who is active, what each of them uses, who can sign, the headcount and the ICP fit, creates a high priority task to open a deal and start outreach with that attached, and notifies the AE and their manager in Slack. Only accounts matching your ICP fire."
      prompt: 'Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts.'
    - step: 4
      title: "Compare against cold outbound"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - pqa_score
      - pqa_segment
      - workflow
      description: "Accounts crossing the threshold each month, how long AEs take to open a deal, conversion to deals and to meetings, the ARR behind them, and how they compare with cold sourced deals on win rate and cycle time."
      prompt: 'Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time: usually PQAs win 2-3x more reliably.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Account level signal to AE task

When several people from one company start using the product in the same fortnight, it briefs an AE and asks them to open a deal.

## Before you run it

- Connect slack
- Send the `user_signed_up` event
- Send the `feature_used` event

## What it does

1. **Score the whole account** (`create_ai_attribute`)

   A 0 to 100 score per account from how many different people were active in the last 14 days, where three or more is a strong signal, the total feature events across them, whether any look like decision makers by title or email pattern, and how deeply the team uses it. 70 and above counts as qualified, updated daily and whenever someone new signs up from the domain.

2. **Find accounts crossing 70** (`create_segment`)

   Accounts that crossed 70 in the last 14 days with no open deal and no AE engaged in the last 60 days. Existing paying customers are left out, because expansion is a different play.

3. **Brief an AE to open a deal** (`create_workflow`)

   On crossing 70 it refreshes the account's firmographics, technographics and decision maker contacts, writes a summary of who is active, what each of them uses, who can sign, the headcount and the ICP fit, creates a high priority task to open a deal and start outreach with that attached, and notifies the AE and their manager in Slack. Only accounts matching your ICP fire.

4. **Compare against cold outbound** (`create_dashboard`)

   Accounts crossing the threshold each month, how long AEs take to open a deal, conversion to deals and to meetings, the ARR behind them, and how they compare with cold sourced deals on win rate and cycle time.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
