---
name: pqa-account-engagement-to-ae-task
description: Use when a user mentions "PQA detection", "product-qualified account", "multi-user account engagement", or asks for related help. When multiple users from the same account engage with the product in a short window — PQA signal — create an AE deal-creation task with the account's full engagement picture, because account-level signals are stronger than single-user signals.
arguments: []
intempt:
  id: pqa-account-engagement-to-ae-task
  version: 1.0.0
  slashCommand: /pqa-account-engagement-to-ae-task
  group: Workflows
  shortDescription: "When multiple users from the same account engage with the product in a short window — PQA signal — create an AE deal-creation task with the account's full engagement picture, because account-level signals are stronger than single-user signals."
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
      title: Compute Account Engagement Score
      command: create_ai_attribute
      produces: attribute
      bindsAs: pqa_score
      description: 'Create an AI-derived attribute ''pqa_score'' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain.'
      prompt: 'Create an AI-derived attribute ''pqa_score'' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain.'
    - step: 2
      title: Identify PQA Accounts
      command: create_segment
      produces: segment
      bindsAs: pqa_segment
      dependsOn:
      - pqa_score
      description: 'Build a segment ''PQA: accounts score >= 70'' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion — see seat-expansion workflow).'
      prompt: 'Build a segment ''PQA: accounts score >= 70'' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion — see seat-expansion workflow).'
    - step: 3
      title: Build PQA Detection Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - pqa_score
      - pqa_segment
      description: 'Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts.'
      prompt: 'Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts.'
    - step: 4
      title: Build PQA Conversion Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - pqa_score
      - pqa_segment
      - workflow
      description: 'Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time — usually PQAs win 2-3x more reliably.'
      prompt: 'Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time — usually PQAs win 2-3x more reliably.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Pqa Account Engagement To Ae Task

## Procedure

1. **Compute Account Engagement Score** [`create_ai_attribute`] — Create an AI-derived attribute 'pqa_score' on the Account object. Composite: (a) count of distinct users from the account active in last 14 days (3+ users = strong PQA signal); (b) total feature events across the account; (c) seniority of users (any decision-makers based on title/email pattern); (d) usage depth across the account team. Output: numeric score 0-100. Score >= 70 = PQA. Updated daily and on new user signups from the domain. → produces: attribute
2. **Identify PQA Accounts** [`create_segment`] — Build a segment 'PQA: accounts score >= 70' capturing accounts where pqa_score crossed 70 in the last 14 days AND no open deal currently exists for the account AND no AE has been actively engaged in the last 60 days. Excludes existing paid customers (different motion — see seat-expansion workflow). → produces: segment
3. **Build PQA Detection Workflow** [`create_workflow`] — Create a workflow firing when pqa_score crosses 70. Step sequence: (1) refresh account enrichment (firmographics, technographics, decision-maker contacts via Apollo/ZoomInfo if connected); (2) compute account context summary: active user count, key features used per user, decision-makers identified, employee count, ICP fit; (3) create a high-priority AE task to create a deal record and start outreach, with the full account context pre-attached; (4) notify AE manager and assigned AE via Slack with a one-paragraph summary and link to the account record. Only fire for ICP-matched accounts. → produces: workflow
4. **Build PQA Conversion Dashboard** [`create_dashboard`] — Compose a PQA dashboard tracking: PQA detection volume (accounts crossing threshold per month), AE response time (median time from PQA-flag to deal_created), PQA-to-deal conversion rate, PQA-to-meeting rate, ARR-weighted PQA value (deals from PQAs vs. non-PQA outbound). Compare PQA-sourced deals vs. cold-outbound-sourced deals on win-rate and cycle time — usually PQAs win 2-3x more reliably. → produces: dashboard
