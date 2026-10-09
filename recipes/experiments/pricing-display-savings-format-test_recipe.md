---
name: pricing-display-savings-format-test
description: |
  Use when a user mentions "pricing display savings format test", or asks for related help. Test how savings are displayed on pricing pages: dollar amount ($24 off) vs. percentage (20% off) vs. compare-at framing ($120 to $96). Universally cited as one of the highest-impact pricing tests.
arguments: []
intempt:
  id: pricing-display-savings-format-test
  version: 1.0.0
  slashCommand: /pricing-display-savings-format-test
  group: Experiments
  title: 'Savings format test'
  shortDescription: 'Compares showing a discount as a dollar amount, as a percentage, or as a struck-through compare-at price, scored on revenue.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [saas, ecommerce]
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
      title: 'Set up the savings format test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits pricing and discounted product page traffic four ways: your current display, Save 24 dollars, 20 percent off, and a struck-through 120 next to 96. The winner is the framing with the most revenue within 7 days of exposure.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Pricing Display Savings Format".

        ═══ PATH 1: Top-level configuration (Setup tab) ═══

        Experience type: client_experiment

        Variants:
        - Control (25% traffic): existing savings display (whatever the current page shows)
        - Variant B (25%): dollar-amount framing: "Save $24" with the discount value as the headline
        - Variant C (25%): percentage framing: "20% off" with the percentage as the headline
        - Variant D (25%): compare-at framing: "$120" struck through with "$96" displayed prominently

        Targeting (experience-wide):
        - Pages: page URL contains "/pricing" OR product detail pages where discounts are shown
        - Devices: any
        - Audience: all visitors
        - Display frequency: always

        Primary metric: Completed an experience goal for this experience with value > 0 (revenue from Subscription started OR Placed order within 7 days of exposure; for ecommerce the value is the order total, for SaaS the subscription amount)
        Secondary metrics:
        - Click on where the target ID starts with "plan-select-" or "add-to-cart-button" (CTA click-through per variant)
        - Checkout created within 7 days
        - AOV: average value of orders attributed to the variant

        Guardrail: bounce rate on the page must not increase >5%

        Schedule: 21 days, require 1,000 unique visitors per variant minimum

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes)

        Variant: B (dollar-amount framing)
          HTML target selector: .pricing-savings-display (or whatever wraps the existing savings text)
          Replacement HTML:
          <div class="savings-display" data-variant="b" data-format="dollar-amount">
            <span class="savings-headline">Save $24</span>
            <span class="savings-context">on annual billing</span>
          </div>

        Variant: C (percentage framing)
          HTML target selector: .pricing-savings-display
          Replacement HTML:
          <div class="savings-display" data-variant="c" data-format="percentage">
            <span class="savings-headline">20% off</span>
            <span class="savings-context">with annual billing</span>
          </div>

        Variant: D (compare-at framing)
          HTML target selector: .pricing-savings-display
          Replacement HTML:
          <div class="savings-display" data-variant="d" data-format="compare-at">
            <span class="original-price"><s>$120</s></span>
            <span class="current-price">$96</span>
            <span class="savings-context">/year</span>
          </div>

        The Visual Editor allows the user to refine typography, color (red vs. green for savings), and exact dollar/percentage values to match their actual pricing.

        The savings amounts ($24, 20%, $120 to $96) are placeholders and must reflect the merchant's real pricing. Compare-at pricing requires the merchant's actual original price to be available; if pricing varies dynamically, the recipe assumes a stable comparison baseline.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Savings format test

Compares showing a discount as a dollar amount, as a percentage, or as a struck-through compare-at price, scored on revenue.

## What it does

1. **Set up the savings format test** (`create_experiment`)

   Splits pricing and discounted product page traffic four ways: your current display, Save 24 dollars, 20 percent off, and a struck-through 120 next to 96. The winner is the framing with the most revenue within 7 days of exposure.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
