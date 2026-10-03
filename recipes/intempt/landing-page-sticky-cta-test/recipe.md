---
id: landing-page-sticky-cta-test
title: Sticky CTA bar test
slash_command: /landing-page-sticky-cta-test
group: Experiments
owner: intempt
summary: Compares an always-visible sticky CTA bar, one that fades in after the hero, and no sticky bar
  at all on marketing pages.
description: >-
  Test sticky CTA bar on SaaS marketing pages: always-visible vs. fade-in-on-scroll vs. no sticky. 8-15%
  lift cited; distinct from mobile-sticky-add-to-cart (ecom PDP).
version: 2.0.0
classification:
  product:
    - experiences
  agent: experiment-strategist
  mode:
    - saas
    - b2b
  complexity: standard
  executionMode: live
  tags:
    - experiment
    - client
  experimentType: a-b
steps:
  - id: s1
    title: Set up the sticky CTA test
    summary: >-
      Splits marketing page traffic three ways: no sticky bar, a bar visible from page load, and a bar
      that appears once the visitor scrolls past the hero. The winner is the variant with the most demo
      requests or signups in the same session.
    builds: experiment
    description: |-
      Create a CLIENT EXPERIMENT on /experiences titled "Landing Page Sticky CTA".
      ═══ PATH 1: Top-level configuration ═══
      Experience type: client_experiment
      Variants:
      - Control (34%): no sticky CTA (existing landing page: CTA only in hero)
      - Variant B (33%): always-visible sticky CTA bar at top of page (appears immediately on page load)
      - Variant C (33%): fade-in sticky CTA bar (appears after the user scrolls past the hero, ~600px scroll depth)
      Targeting:
      - Pages: marketing landing pages: homepage "/", /solutions, /features, /product, /pricing
      - Devices: any (mobile + desktop both benefit; mobile especially given long-scroll pages)
      - Audience: all visitors
      - Display frequency: always (within session)
      Primary metric: goal_completed_in_experience where experience_id = <this> (goal: form_submitted on demo-request OR user_created via signup, within session of exposure)
      Secondary metrics:
      - click_on where target_id = "sticky-cta-button" (sticky CTA engagement rate)
      - click_on where target_id = "hero-cta-button" (does sticky cannibalize hero clicks?)
      - Bounce rate per variant (variant B's always-visible may feel pushy)
      - Scroll depth (does sticky reduce scroll engagement?)
      Guardrail: bounce rate must not increase >5%; scroll-depth-to-50% rate must not drop >10%
      Schedule: 14 days, 1,500 unique visitors per variant minimum
      ═══ PATH 2: Variant HTML content (Visual Editor) ═══
      Variant: Control (no DOM changes)
      Variant: B (always-visible sticky CTA)
       HTML target selector: body (prepend fixed-position bar)
       Variant DOM:
       <div class="sticky-cta-bar sticky-cta-bar--top" data-variant="b" data-trigger="immediate" style="position:fixed;top:0;left:0;right:0;background:#fff;border-bottom:1px solid #eee;padding:12px 24px;z-index:1000;display:flex;align-items:center;justify-content:space-between;">
       <div class="sticky-cta-message">
       <strong>[Brand]</strong>: see it in action in 15 minutes
       </div>
       <button class="sticky-cta-button" id="sticky-cta-button" data-variant="b">Book a demo</button>
       </div>
       Adjust body padding-top to compensate for the bar's height (so existing content isn't hidden behind it).
      Variant: C (fade-in sticky CTA)
       Same DOM as Variant B but with data-variant="c" and data-trigger="scroll-600px".
       Lightweight JS the user refines in the Visual Editor:
       - Listen for scroll events
       - When window.scrollY > 600 (or after the hero CTA scrolls out of view), set the bar visible with a smooth fade-in transition (300ms)
       - When the user scrolls back above the threshold, hide the bar smoothly
      The Visual Editor allows the user to refine the sticky bar's color, copy, button styling, and animation timing. Mobile note: ensure the sticky bar respects the iOS Safari URL bar and doesn't double-stack with mobile browser chrome.
      Taxonomy notes:
      - This is distinct from mobile-sticky-add-to-cart-test (which is ecommerce PDP-specific, mobile-only). Landing-page sticky CTA applies to SaaS marketing pages on all devices.
      - target_id="sticky-cta-button" must be preserved across variants B and C for consistent click_on aggregation.
      - Variant C's fade-in is generally less intrusive but has slightly lower engagement than Variant B's always-visible. The test answers: which tradeoff wins for your audience?
      - For dark-launching: ship Variant B first to a small traffic slice (5%) to confirm no layout regressions before full experiment ramp.
outputs:
  - key: experiment
    producedByStep: s1
    type: experiment
    description: Website experiment created on /experiences.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Sticky CTA bar test

Compares an always-visible sticky CTA bar, one that fades in after the hero, and no sticky bar at all on marketing pages.

## Steps

1. **Set up the sticky CTA test** (builds experiment)

   Splits marketing page traffic three ways: no sticky bar, a bar visible from page load, and a bar that appears once the visitor scrolls past the hero. The winner is the variant with the most demo requests or signups in the same session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.

## Availability

Coming soon: waiting on the engine to build experiment.
