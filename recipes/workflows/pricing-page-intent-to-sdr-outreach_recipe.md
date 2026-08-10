---
name: pricing-page-intent-to-sdr-outreach
description: Use when a user mentions "pricing page intent", "pricing-page-visit workflow", "intent signal SDR", or asks for related help. When a known user (or identified account) visits the pricing page repeatedly or after a deep product evaluation, fire an SDR task with the visit context — pricing-page visits are some of the strongest revenue intent signals.
arguments: []
intempt:
  id: pricing-page-intent-to-sdr-outreach
  version: 1.0.0
  slashCommand: /pricing-page-intent-to-sdr-outreach
  group: Workflows
  shortDescription: "When a known user (or identified account) visits the pricing page repeatedly or after a deep product evaluation, fire an SDR task with the visit context — pricing-page visits are some of the strongest revenue intent signals."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [intent-signal, pricing-page, sdr-routing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: pricing_page_viewed, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Identify Pricing Page Visitors
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits.
      prompt: Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits.
    - step: 2
      title: Build Pricing Intent Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      description: 'Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user''s account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged ''high-intent: pricing'' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt).'
      prompt: 'Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user''s account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged ''high-intent: pricing'' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt).'
    - step: 3
      title: Build Pricing Intent Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - workflow
      description: 'Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to deal_created. Compare against baseline (deals sourced from cold outbound) — pricing-intent leads should convert 3-5x better.'
      prompt: 'Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to deal_created. Compare against baseline (deals sourced from cold outbound) — pricing-intent leads should convert 3-5x better.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Pricing Page Intent To Sdr Outreach

## Procedure

1. **Identify Pricing Page Visitors** [`create_segment`] — Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits. → produces: segment
2. **Build Pricing Intent Workflow** [`create_workflow`] — Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user's account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged 'high-intent: pricing' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt). → produces: workflow
3. **Build Pricing Intent Dashboard** [`create_dashboard`] — Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to deal_created. Compare against baseline (deals sourced from cold outbound) — pricing-intent leads should convert 3-5x better. → produces: dashboard
