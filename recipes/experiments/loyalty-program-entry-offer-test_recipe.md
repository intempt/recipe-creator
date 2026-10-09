---
name: loyalty-program-entry-offer-test
description: |
  Use when a user mentions "loyalty programme entry offer test", or asks for related help. Test the best entry offer to drive loyalty programme sign-ups at checkout. Client experiment with random split.
arguments: []
intempt:
  id: loyalty-program-entry-offer-test
  version: 1.0.1
  slashCommand: /loyalty-program-entry-offer-test
  group: Experiments
  title: 'Loyalty signup offer test'
  shortDescription: 'Compares four checkout offers for joining the loyalty programme, scored on how many first-time buyers actually join.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
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
      title: 'Set up the loyalty offer test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Shows first-time buyers at checkout one of four things: no prompt, 10 percent off their next order, double points on this order, or free shipping on the next three orders. The winner signs up the most members, with 90-day repeat purchase as the check that it was worth it.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Loyalty Programme Entry Offer".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (25%): no loyalty prompt at checkout
        - Variant B (25%): 10% discount on next order for joining
        - Variant C (25%): 2× points on this order for joining
        - Variant D (25%): free shipping on next 3 orders for joining

        Targeting:
        - Pages: page URL contains "/checkout"
        - Devices: any
        - Audience: first-time buyers only: segment definition: lifetime value is 0 or order count is 0 (this is their first checkout)
        - Display frequency: once per order

        Primary metric: Completed an experience goal for this experience (goal fires when the "loyalty_member" tag is added to the user within the session)
        Secondary metrics:
        - 90-day repeat purchase rate per joined cohort (see cohort tagging below: this is the most important downstream signal)
        - Order total on the current order (does the offer increase basket size? Free shipping on the next order shouldn't move the current order total; double points might)
        - Per-variant loyalty join rate (loyalty_member tag added / Checkout created within experiment)

        Guardrail: checkout completion rate must not drop >3% (offer banner shouldn't slow conversion)

        Schedule: 30 days for the experiment itself; 90 additional days for cohort-tracking the repeat-purchase rate.

        ═══ Cohort tagging for 90-day repeat purchase measurement ═══

        The "90-day repeat purchase rate per variant" is the most informative signal but requires cohort tagging at signup. The recipe expects the loyalty-join firing logic to capture which variant the user joined under:

        When the user checks the loyalty checkbox in any variant, fire BOTH events together:
          1. User tags added with tag = "loyalty_member"
          2. User tags added with tag = "loyalty_offer:b" (or "c" or "d" matching the variant they joined under)

        The variant-specific tag persists on the user record. Then 90 days later, segment cohorts:
          - Cohort B = users with both "loyalty_member" AND "loyalty_offer:b" tags
          - Cohort C = users with both "loyalty_member" AND "loyalty_offer:c" tags
          - Cohort D = users with both "loyalty_member" AND "loyalty_offer:d" tags
          - Cohort Control = first-time-buyers in Variant Control who completed checkout (didn't see a prompt)

        90-day repeat-purchase rate per cohort = count(users in cohort with a Placed order after their join time and within 90 days of it) / cohort size.

        The 90-day window is the standard repeat-purchase measurement window for ecommerce; some categories (apparel) may need 60 days, others (consumables) may need 30.

        Cohort Control (first-time buyers who saw no prompt and didn't join) is essential for measuring the causal repeat-purchase lift: without it you only know which offer cohort returns most often, not whether the program itself moves the needle vs. doing nothing.

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (no DOM changes: no prompt)
          Existing checkout flow. Measures intrinsic loyalty join rate via other channels.

        Variant: B (10% off next order)
          HTML target selector: .checkout-summary (insert before submit button)
          Variant DOM:
          <div class="loyalty-offer-banner" data-variant="b" data-offer-code="loyalty_offer_b">
            <h3>Join our rewards program</h3>
            <p>Get <strong>10% off your next order</strong></p>
            <label class="loyalty-checkbox-label">
              <input type="checkbox" id="loyalty-join-checkbox" data-variant="b" data-offer-code="loyalty_offer_b" />
              <span>Yes, sign me up for [Brand] rewards</span>
            </label>
          </div>

        Variant: C (2× points this order)
          HTML target selector: .checkout-summary
          Variant DOM:
          <div class="loyalty-offer-banner" data-variant="c" data-offer-code="loyalty_offer_c">
            <h3>Join our rewards program</h3>
            <p>Earn <strong>double points on this order</strong></p>
            <label class="loyalty-checkbox-label">
              <input type="checkbox" id="loyalty-join-checkbox" data-variant="c" data-offer-code="loyalty_offer_c" />
              <span>Yes, sign me up for [Brand] rewards</span>
            </label>
          </div>

        Variant: D (free shipping next 3 orders)
          HTML target selector: .checkout-summary
          Variant DOM:
          <div class="loyalty-offer-banner" data-variant="d" data-offer-code="loyalty_offer_d">
            <h3>Join our rewards program</h3>
            <p>Get <strong>free shipping on your next 3 orders</strong></p>
            <label class="loyalty-checkbox-label">
              <input type="checkbox" id="loyalty-join-checkbox" data-variant="d" data-offer-code="loyalty_offer_d" />
              <span>Yes, sign me up for [Brand] rewards</span>
            </label>
          </div>

        When the user submits checkout with the loyalty-join-checkbox checked, fire User tags added twice: once with "loyalty_member" and once with the variant-specific tag from the data-offer-code attribute. The Completed an experience goal event fires automatically based on the loyalty_member tag addition.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Loyalty signup offer test

Compares four checkout offers for joining the loyalty programme, scored on how many first-time buyers actually join.

## What it does

1. **Set up the loyalty offer test** (`create_experiment`)

   Shows first-time buyers at checkout one of four things: no prompt, 10 percent off their next order, double points on this order, or free shipping on the next three orders. The winner signs up the most members, with 90-day repeat purchase as the check that it was worth it.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
