---
id: pricing-toggle-default-test
title: Billing toggle default test
slash_command: /pricing-toggle-default-test
group: Experiments
owner: intempt
curator: rana
summary: Tests whether defaulting the pricing toggle to annual rather than monthly earns more, counting
  annual plans at full annual value.
description: >-
  monthly)", or asks for related help. Default to annual vs. monthly billing on the pricing toggle. Direct
  revenue impact (annual default to higher LTV). Distinct from pricing-page-layout-test.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - finance
  vertical:
    - payments
  complexity: standard
  executionMode: live
  tags:
    - experiment
    - client
  experimentType: a-b
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new A/B experiment, from step 1 "Set up the toggle default test"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the toggle default test
    summary: >-
      Splits pricing page traffic three ways: the current default, annual selected with a savings highlight,
      and monthly selected explicitly. Judged on subscription revenue within 7 days, with annual plans
      counted at their full annual value rather than one month.
    builds: experiment
    description: |-
      Create a CLIENT EXPERIMENT on /experiences titled "Pricing Toggle Default".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_experiment
      Variants:
      - Control (33%): existing default state (whatever the page currently shows: most often monthly)
      - Variant B (33%): default to ANNUAL billing toggle position with savings highlight ("Save 20% with annual")
      - Variant C (34%): default to MONTHLY billing toggle position (most-likely current state, but explicit)
      Targeting:
      - Pages: page URL contains "/pricing"
      - Devices: any
      - Audience: all visitors
      - Display frequency: always
      Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from subscription_created within 7 days, weighted by billing-period: annual subscriptions count for full annual value)
      Secondary metrics:
      - subscription_created where billing_period = "annual" (annual conversion rate per variant)
      - subscription_created where billing_period = "monthly" (monthly conversion rate per variant)
      - Toggle-interaction rate (click_on where target_id = "pricing-toggle")
      - AOV per signup (annual signups have ~12x higher first-payment value than monthly)
      Guardrail: total subscription_created rate must not drop >3% (the test shouldn't suppress overall conversion; it should shift mix toward annual)
      Schedule: 21 days, 1,000 visitors per variant minimum
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (no DOM changes)
      Variant: B (annual default + savings highlight)
       HTML target selector: .pricing-toggle (the toggle UI between monthly and annual)
       Replacement HTML:
       <div class="pricing-toggle" data-variant="b" data-default="annual">
       <div class="toggle-buttons">
       <button class="toggle-option" data-period="monthly" id="pricing-toggle-monthly">Monthly</button>
       <button class="toggle-option toggle-option--active" data-period="annual" id="pricing-toggle-annual">
       Annual
       <span class="savings-badge">Save 20%</span>
       </button>
       </div>
       </div>
       Lightweight JS:
       - On page load, programmatically set the toggle to "annual" position
       - Update all displayed prices to annual values
       - Add a `data-billing-default="annual"` attribute on body for analytics
      Variant: C (monthly default: explicit baseline for comparison)
       HTML target selector: .pricing-toggle
       Replacement HTML:
       <div class="pricing-toggle" data-variant="c" data-default="monthly">
       <div class="toggle-buttons">
       <button class="toggle-option toggle-option--active" data-period="monthly" id="pricing-toggle-monthly">Monthly</button>
       <button class="toggle-option" data-period="annual" id="pricing-toggle-annual">
       Annual
       <span class="savings-badge">Save 20%</span>
       </button>
       </div>
       </div>
      The Visual Editor allows the user to refine the savings-badge copy, toggle styling, and animation. Ensure the toggle-button click_on events fire properly in both variants so the toggle-interaction rate metric works.
      Taxonomy notes:
      - Most modern SaaS pricing pages already have a monthly/annual toggle: this experiment changes the *default* state on page load.
      - subscription_created.billing_period (or equivalent) must be populated to measure the annual-vs-monthly mix shift. If your subscription event doesn't track billing period, add it.
      - Annual default tends to lift annual conversion rate by 30-50% with little impact on overall conversion: the savings come almost entirely from mix shift, not from new conversions.
      - For trial signups (which usually start as a free trial then convert to paid), this experiment is more impactful at the trial to paid step than at the trial-signup step. Plan your downstream measurement window accordingly.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Billing toggle default test

Tests whether defaulting the pricing toggle to annual rather than monthly earns more, counting annual plans at full annual value.

## Steps

1. **Set up the toggle default test** (builds experiment)

   Splits pricing page traffic three ways: the current default, annual selected with a savings highlight, and monthly selected explicitly. Judged on subscription revenue within 7 days, with annual plans counted at their full annual value rather than one month.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new A/B experiment, from step 1 "Set up the toggle default test"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build experiment.
