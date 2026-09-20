---
name: pricing-page-layout-test
description: |
  Use when a user mentions "pricing page layout test", or asks for related help. Test which pricing page layout maximizes plan selection and checkout starts. Client experiment with three variants.
arguments: []
intempt:
  id: pricing-page-layout-test
  version: 1.0.0
  slashCommand: /pricing-page-layout-test
  group: Experiments
  title: 'Pricing page layout test'
  shortDescription: 'Compares your current pricing layout against side-by-side cards with a recommended plan and an interactive usage slider.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [experiment, client]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the pricing layout test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits pricing page traffic three ways: the existing layout, side-by-side cards with a Recommended badge on the middle plan, and a usage slider that recommends a plan. The winner is the layout with the most subscription revenue within 7 days.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Pricing Page Layout Test".

        ═══ PATH 1: Top-level configuration (Setup tab) ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): existing pricing layout
        - Variant B (33%): side-by-side cards with "Recommended" badge on the middle plan
        - Variant C (33%): interactive usage slider with dynamic plan recommendation

        Targeting:
        - Pages: page URL equals "/pricing" (or "/pricing/*" for nested routes)
        - Devices: any
        - Audience: all visitors
        - Display frequency: always

        Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from subscription_created within 7 days of exposure)
        Secondary metrics:
        - click_on where target_id starts with "plan-select-" (per-plan click-through)
        - checkout_created within 7 days of exposed_to_experience
        - subscription_created within 14 days

        Guardrail: bounce rate on /pricing must not increase >5%

        Schedule: 21 days minimum, require 1,000 unique visitors per variant

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control
          No DOM changes: measures the existing pricing page.

        Variant: B (side-by-side cards)
          HTML target selector: .pricing-section (or whatever wraps the existing plan grid)
          Replacement HTML:
          <section class="pricing-cards-grid">
            <article class="plan-card" data-plan="starter">
              <h3>Starter</h3>
              <div class="plan-price">$X/mo</div>
              <ul class="plan-features"><!-- features --></ul>
              <button class="plan-select" id="plan-select-starter" data-variant="b">Choose Starter</button>
            </article>
            <article class="plan-card plan-card--recommended" data-plan="pro">
              <span class="recommended-badge">Recommended</span>
              <h3>Pro</h3>
              <div class="plan-price">$Y/mo</div>
              <ul class="plan-features"><!-- features --></ul>
              <button class="plan-select" id="plan-select-pro" data-variant="b">Choose Pro</button>
            </article>
            <article class="plan-card" data-plan="enterprise">
              <h3>Enterprise</h3>
              <div class="plan-price">Contact us</div>
              <ul class="plan-features"><!-- features --></ul>
              <button class="plan-select" id="plan-select-enterprise" data-variant="b">Contact Sales</button>
            </article>
          </section>

        Variant: C (interactive slider)
          HTML target selector: .pricing-section
          Replacement HTML:
          <section class="pricing-slider-layout">
            <div class="usage-slider">
              <label for="usage-input">How many users do you have?</label>
              <input type="range" id="usage-input" min="1" max="500" value="10" />
              <output class="usage-value">10 users</output>
            </div>
            <div class="dynamic-plan-display">
              <h3 class="recommended-plan-name">Pro</h3>
              <div class="dynamic-price">$Y/mo</div>
              <button class="plan-select" id="plan-select-dynamic" data-variant="c">Get Started</button>
            </div>
            <!-- include lightweight JS to update the displayed plan as the slider moves -->
          </section>

        The Visual Editor renders the variant HTML with the user's existing site styles applied; the user refines copy, color, and spacing in the canvas before publishing.

        Taxonomy notes:
        - All click_on target_id values starting with "plan-select-" are tracked uniformly so per-plan click rates can be compared across variants.
        - value on goal_completed_in_experience is set by the platform when the downstream subscription_created.amount is captured.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Pricing page layout test

Compares your current pricing layout against side-by-side cards with a recommended plan and an interactive usage slider.

## What it does

1. **Set up the pricing layout test** (`create_experiment`)

   Splits pricing page traffic three ways: the existing layout, side-by-side cards with a Recommended badge on the middle plan, and a usage slider that recommends a plan. The winner is the layout with the most subscription revenue within 7 days.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
