---
name: pricing-page-intent-to-sdr-outreach
description: Use when a user mentions "pricing page intent", "pricing-page-visit workflow", "intent signal SDR", or asks for related help. When a known user (or identified account) visits the pricing page repeatedly or after a deep product evaluation, fire an SDR task with the visit context, pricing-page visits are some of the strongest revenue intent signals.
arguments: []
intempt:
  id: pricing-page-intent-to-sdr-outreach
  title: "Pricing page intent to outreach"
  version: 1.0.0
  slashCommand: /pricing-page-intent-to-sdr-outreach
  group: Workflows
  shortDescription: "Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts it on an SDR with the visit context attached."
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
      title: "Filter out the casual visits"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Identified users with two or more pricing page views in the last 14 days, or a single view after at least five minutes in the product. Existing customers and anyone with an open deal are left out. The repeat and dwell tests are what remove the one click visitors."
      prompt: Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ Pricing page viewed events in the last 14 days, OR a single Pricing page viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits.
    - step: 2
      title: "Send the visit to a rep"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      description: "On an identified pricing view it checks the visit qualifies, enriches the account if needed, gathers how many times they have been, what they looked at beforehand, the features used in that session and the ICP tier, creates an SDR task tagged high intent, assigns it by territory and messages the rep. An anonymous visitor goes into the identification journey instead, which asks for an email in the app."
      prompt: 'Create a workflow firing on Pricing page viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user''s account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged ''high-intent: pricing'' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt).'
    - step: 3
      title: "Compare against cold sourcing"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - workflow
      description: "Signals per week, the median minutes from signal to first contact, and conversion to a booked demo and to a deal, set against deals sourced from cold outbound."
      prompt: 'Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to Deal created. Compare against baseline (deals sourced from cold outbound): pricing-intent leads should convert 3-5x better.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Pricing page intent to outreach

Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts it on an SDR with the visit context attached.

## Before you run it

- Connect slack
- Send the `pricing_page_viewed` event

## What it does

1. **Filter out the casual visits** (`create_segment`)

   Identified users with two or more pricing page views in the last 14 days, or a single view after at least five minutes in the product. Existing customers and anyone with an open deal are left out. The repeat and dwell tests are what remove the one click visitors.

2. **Send the visit to a rep** (`create_workflow`)

   On an identified pricing view it checks the visit qualifies, enriches the account if needed, gathers how many times they have been, what they looked at beforehand, the features used in that session and the ICP tier, creates an SDR task tagged high intent, assigns it by territory and messages the rep. An anonymous visitor goes into the identification journey instead, which asks for an email in the app.

3. **Compare against cold sourcing** (`create_dashboard`)

   Signals per week, the median minutes from signal to first contact, and conversion to a booked demo and to a deal, set against deals sourced from cold outbound.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
