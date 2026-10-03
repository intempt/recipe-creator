---
id: pricing-page-intent-to-sdr-outreach
title: Pricing page intent to outreach
slash_command: /pricing-page-intent-to-sdr-outreach
group: Workflows
owner: intempt
summary: Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts
  it on an SDR with the visit context attached.
description: >-
  When a known user (or identified account) visits the pricing page repeatedly or after a deep product
  evaluation, fire an SDR task with the visit context, pricing-page visits are some of the strongest revenue
  intent signals.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - intent-signal
    - pricing-page
    - sdr-routing
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: pricing_page_viewed
      severity: blocking
steps:
  - id: s1
    title: Filter out the casual visits
    summary: >-
      Identified users with two or more pricing page views in the last 14 days, or a single view after
      at least five minutes in the product. Existing customers and anyone with an open deal are left out.
      The repeat and dwell tests are what remove the one click visitors.
    builds: segment
    description: >-
      Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed
      events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total
      product session time. Excludes existing paid customers and users with an open deal already. The
      repeat-visit and dwell-time qualifiers filter out casual one-click visits.
  - id: s2
    title: Send the visit to a rep
    summary: >-
      On an identified pricing view it checks the visit qualifies, enriches the account if needed, gathers
      how many times they have been, what they looked at beforehand, the features used in that session
      and the ICP tier, creates an SDR task tagged high intent, assigns it by territory and messages the
      rep. An anonymous visitor goes into the identification journey instead, which asks for an email
      in the app.
    builds: workflow
    description: >-
      Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1)
      check whether this is a qualifying visit per segment criteria; (2) enrich the user's account if
      not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features
      used in session, account ICP tier; (4) create a SDR task tagged 'high-intent: pricing' with the
      context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified
      (anonymous visitor), trigger the identification journey instead (request email via in-app prompt).
      Use the result of "Filter out the casual visits".
    dependsOn:
      - s1
  - id: s3
    title: Compare against cold sourcing
    summary: >-
      Signals per week, the median minutes from signal to first contact, and conversion to a booked demo
      and to a deal, set against deals sourced from cold outbound.
    builds: dashboard
    description: >-
      Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time
      (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled,
      conversion rate from pricing-intent to deal_created. Compare against baseline (deals sourced from
      cold outbound): pricing-intent leads should convert 3-5x better. Use the result of "Filter out the
      casual visits", "Send the visit to a rep".
    dependsOn:
      - s1
      - s2
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Pricing page intent to outreach

Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts it on an SDR with the visit context attached.

## Steps

1. **Filter out the casual visits** (builds segment)

   Identified users with two or more pricing page views in the last 14 days, or a single view after at least five minutes in the product. Existing customers and anyone with an open deal are left out. The repeat and dwell tests are what remove the one click visitors.

2. **Send the visit to a rep** (builds workflow)

   On an identified pricing view it checks the visit qualifies, enriches the account if needed, gathers how many times they have been, what they looked at beforehand, the features used in that session and the ICP tier, creates an SDR task tagged high intent, assigns it by territory and messages the rep. An anonymous visitor goes into the identification journey instead, which asks for an email in the app.

3. **Compare against cold sourcing** (builds dashboard)

   Signals per week, the median minutes from signal to first contact, and conversion to a booked demo and to a deal, set against deals sourced from cold outbound.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
