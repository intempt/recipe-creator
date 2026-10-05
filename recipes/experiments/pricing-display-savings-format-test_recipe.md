---
name: pricing-display-savings-format-test
description: |
  Use when a user mentions "pricing display savings format test", or asks for related help. Test how savings are displayed on pricing pages: dollar amount ($24 off) vs. percentage (20% off) vs. compare-at framing ($120 → $96). Universally cited as one of the highest-impact pricing tests.
arguments: []
intempt:
  id: pricing-display-savings-format-test
  version: 1.0.0
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Creates a client experiment on /experiences splitting pricing-page traffic across control, dollar-off ($24), and percentage-off (20%) savings framings."
  availability: coming-soon
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
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Pricing Display Savings Format".

        ═══ PATH 1: Top-level configuration (Setup tab) ═══

        Experience type: client_experiment

        Variants:
        - Control (25% traffic): existing savings display (whatever the current page shows)
        - Variant B (25%): dollar-amount framing — "Save $24" with the discount value as the headline
        - Variant C (25%): percentage framing — "20% off" with the percentage as the headline
        - Variant D (25%): compare-at framing — "$120" struck through with "$96" displayed prominently

        Targeting (experience-wide):
        - Pages: page URL contains "/pricing" OR product detail pages where discounts are shown
        - Devices: any
        - Audience: all visitors
        - Display frequency: always

        Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from subscription_created OR order_created within 7 days of exposure)
        Secondary metrics:
        - click_on where target_id starts with "plan-select-" or "add-to-cart-button" (CTA click-through per variant)
        - checkout_created within 7 days
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

        Taxonomy notes:
        - The actual savings amounts ($24, 20%, $120→$96) must reflect the merchant's real pricing — these are placeholders that the user adjusts in the Visual Editor.
        - For ecommerce, the goal fires on order_created.total_price; for saas, on subscription_created.amount.
        - Compare-at pricing requires the merchant's actual original price to be available; if pricing varies dynamically, the recipe assumes a stable comparison baseline.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Pricing Display Savings Format Test

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Pricing Display Savings Format".

   ═══ PATH 1: Top-level configuration (Setup tab) ═══

   Experience type: client_experiment

   Variants:
   - Control (25% traffic): existing savings display (whatever the current page shows)
   - Variant B (25%): dollar-amount framing — "Save $24" with the discount value as the headline
   - Variant C (25%): percentage framing — "20% off" with the percentage as the headline
   - Variant D (25%): compare-at framing — "$120" struck through with "$96" displayed prominently

   Targeting (experience-wide):
   - Pages: page URL contains "/pricing" OR product detail pages where discounts are shown
   - Devices: any
   - Audience: all visitors
   - Display frequency: always

   Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from subscription_created OR order_created within 7 days of exposure)
   Secondary metrics:
   - click_on where target_id starts with "plan-select-" or "add-to-cart-button" (CTA click-through per variant)
   - checkout_created within 7 days
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

   Taxonomy notes:
   - The actual savings amounts ($24, 20%, $120→$96) must reflect the merchant's real pricing — these are placeholders that the user adjusts in the Visual Editor.
   - For ecommerce, the goal fires on order_created.total_price; for saas, on subscription_created.amount.
   - Compare-at pricing requires the merchant's actual original price to be available; if pricing varies dynamically, the recipe assumes a stable comparison baseline.
   ```
