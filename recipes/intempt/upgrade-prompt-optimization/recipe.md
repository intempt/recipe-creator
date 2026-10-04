---
id: upgrade-prompt-optimization
title: Upgrade prompt test
slash_command: /upgrade-prompt-optimization
group: Experiments
owner: intempt
curator: rana
summary: Compares four places to show the upgrade prompt to free users, with timing layered in through
  audience targeting.
description: >-
  Combined test of upgrade prompt placement (where) and timing (when) for free SaaS users. Two creation
  flows: client variants for placement, server payload for timing.
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - saas
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
    - A new A/B experiment, from step 1 "Set up the upgrade prompt test"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Set up the upgrade prompt test
    summary: >-
      Splits free users four ways on placement: the existing dashboard banner, an inline prompt at the
      feature-limit gate, a persistent card in the sidebar, and a floating pill in the bottom-right corner.
      Timing is layered on through audience targeting by account age and activity. The winner is the placement
      with the most upgrades within 14 days.
    builds: experiment
    description: |-
      Create a CLIENT EXPERIMENT on /experiences titled "Upgrade Prompt Optimization".
      This recipe merges what was historically two separate experiments (placement + timing) into one. The PLACEMENT dimension is tested via client variants (different on-page locations); the TIMING dimension is layered via the experience's audience targeting (segment-based: account age + activity).
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_experiment
      Variants (placement axis):
      - Control (25%): existing upgrade banner at top of dashboard
      - Variant B (25%): inline upgrade prompt at the feature-limit gate (shown when user clicks a paywalled feature)
      - Variant C (25%): persistent upgrade card in sidebar navigation
      - Variant D (25%): floating upgrade pill in the bottom-right corner
      Targeting (timing dimension applied as audience filter):
      - Pages: any in-app page where the dashboard chrome renders
      - Audience: free plan users only: segment definition: subscription is null OR plan_name = "free", AND account_age >= 3 days
       - Run this experiment in three sequential cohorts to test timing:
       - Cohort 1: account_age 3-7 days
       - Cohort 2: account_age 8-14 days
       - Cohort 3: account_age >14 days
       - Each cohort gets the same 4 placement variants; comparing across cohorts answers the timing question.
      - Devices: any
      - Display frequency: once_per_session (avoid prompt fatigue within a session)
      Primary metric: goal_completed_in_experience where experience_id = <this> (goal fires on subscription_created within 14 days of exposure)
      Secondary metrics:
      - click_on where target_id = "upgrade-prompt-cta" (per-placement click rate)
      - click_on where target_id = "upgrade-prompt-dismiss" (dismissal rate: friction signal)
      - subscription_created within 14 days
      Guardrail: NPS feedback (feedback_submitted with score property) must not drop more than 5 points in trailing-30d trend
      Schedule: 21 days
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (top banner)
       HTML target selector: .dashboard-header (insert before)
       Variant DOM (existing):
       <div class="upgrade-banner" data-variant="control" data-placement="top-banner">
       <p>Upgrade to Pro for unlimited features</p>
       <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="top">Upgrade now</button>
       <button class="dismiss" id="upgrade-prompt-dismiss" aria-label="Dismiss">×</button>
       </div>
      Variant: B (inline at feature-limit gate)
       HTML target selector: .feature-gate-overlay (the modal/overlay that appears when a free user hits a feature limit)
       Variant DOM:
       <div class="upgrade-inline-prompt" data-variant="b" data-placement="inline-gate">
       <h3>You've hit your free plan limit</h3>
       <p>Upgrade to Pro to continue with unlimited access.</p>
       <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="inline">Upgrade now</button>
       <button class="dismiss" id="upgrade-prompt-dismiss">Maybe later</button>
       </div>
      Variant: C (sidebar card)
       HTML target selector: .sidebar-nav (append at bottom)
       Variant DOM:
       <div class="upgrade-sidebar-card" data-variant="c" data-placement="sidebar">
       <span class="upgrade-icon">⚡</span>
       <p>Unlock Pro features</p>
       <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="sidebar">See plans</button>
       </div>
      Variant: D (floating pill)
       HTML target selector: body (append fixed-position element)
       Variant DOM:
       <div class="upgrade-floating-pill" data-variant="d" data-placement="floating-pill" style="position:fixed;bottom:24px;right:24px;">
       <button class="upgrade-cta" id="upgrade-prompt-cta" data-placement="floating">Upgrade ↗</button>
       <button class="dismiss" id="upgrade-prompt-dismiss" aria-label="Dismiss">×</button>
       </div>
      The Visual Editor lets the user adjust copy, colors, animation, and exact positioning per variant. Ensure target_id values "upgrade-prompt-cta" and "upgrade-prompt-dismiss" are preserved across all variants so click_on aggregation is consistent.
      Taxonomy notes:
      - The 4-variant design tests placement; the 3-cohort schedule tests timing. Total observations: 4 placements × 3 timings = 12 cells. Plan sample sizes accordingly: you'll want at least 500 exposures per cell, so ~6,000 free users in the experiment.
      - click_on.target_id = "upgrade-prompt-cta" is shared across placements, with target_id and the data-placement attribute on the button enabling per-placement segmentation in analysis.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Upgrade prompt test

Compares four places to show the upgrade prompt to free users, with timing layered in through audience targeting.

## Steps

1. **Set up the upgrade prompt test** (builds experiment)

   Splits free users four ways on placement: the existing dashboard banner, an inline prompt at the feature-limit gate, a persistent card in the sidebar, and a floating pill in the bottom-right corner. Timing is layered on through audience targeting by account age and activity. The winner is the placement with the most upgrades within 14 days.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new A/B experiment, from step 1 "Set up the upgrade prompt test"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build experiment.
