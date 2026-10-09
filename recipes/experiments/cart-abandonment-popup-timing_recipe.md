---
name: cart-abandonment-popup-timing
description: |
  Use when a user mentions "cart abandonment popup timing", or asks for related help. Test when to show the save-your-cart popup: exit-intent vs. delay vs. no popup. Client experiment.
arguments: []
intempt:
  id: cart-abandonment-popup-timing
  version: 1.0.1
  slashCommand: /cart-abandonment-popup-timing
  group: Experiments
  title: 'Cart popup timing test'
  shortDescription: 'Compares exit-intent, a 30 second delay and no popup at all on cart pages, scored on orders placed within 24 hours.'
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
      title: 'Set up the popup timing test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits desktop cart visitors three ways: an exit-intent popup, a popup after 30 seconds of an idle cart, and no popup as a baseline. The winner is the variant with the most orders within 24 hours of being shown. Desktop only, because exit-intent needs mouse tracking, and once per session.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Cart Popup Timing".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): exit-intent popup (mouse leaves viewport)
        - Variant B (33%): 30-second delay popup after cart is idle
        - Variant C (33%): no popup (control baseline: measures intrinsic recovery rate)

        Targeting:
        - Pages: page URL contains "/cart" OR Cart created has occurred in the current session
        - Devices: desktop only (exit-intent requires mouse tracking; mobile doesn't have hover events)
        - Audience: visitors with at least one Cart created in the current session
        - Display frequency: once_per_session

        Primary metric: Completed an experience goal for this experience (goal: Placed order within 24 hours of exposure)
        Secondary metrics:
        - Click on where the target is "popup-save-cart" (popup engagement rate)
        - Click on where the target is "popup-dismiss" (dismissal rate)
        - Email capture rate from popup (Submit on the popup form)
        - Placed order within 24 hours

        Guardrail: bounce rate (sessions ending immediately after popup display) must not increase >10%

        Schedule: 14 days

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        Variant: Control (exit-intent popup)
          HTML target selector: body (append fixed-position element on exit-intent trigger)
          Variant DOM (rendered when mouse leaves viewport top):
          <div class="cart-save-popup" data-variant="control" data-trigger="exit-intent" hidden>
            <div class="popup-overlay"></div>
            <div class="popup-content">
              <button class="popup-close" id="popup-dismiss" aria-label="Close">×</button>
              <h2>Wait! Save your cart</h2>
              <p>We'll save your items and email you a reminder.</p>
              <form class="popup-email-form" id="popup-email-form">
                <input type="email" name="email" placeholder="your@email.com" required />
                <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
              </form>
            </div>
          </div>

          Trigger logic: attach mouseleave listener to document.documentElement. When the cursor leaves the top edge of the viewport (e.target === document.documentElement && e.clientY <= 0), set the popup's hidden attribute to false and store a sessionStorage flag so it doesn't fire again in the same session.

        Variant: B (30-second delay popup)
          HTML target selector: body (append fixed-position element)
          Variant DOM:
          <div class="cart-save-popup" data-variant="b" data-trigger="delay-30s" hidden>
            <div class="popup-overlay"></div>
            <div class="popup-content">
              <button class="popup-close" id="popup-dismiss" aria-label="Close">×</button>
              <h2>Still thinking it over?</h2>
              <p>Save your cart and we'll send you a reminder: no pressure.</p>
              <form class="popup-email-form" id="popup-email-form">
                <input type="email" name="email" placeholder="your@email.com" required />
                <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
              </form>
            </div>
          </div>

          Trigger logic: when Cart created fires, start a 30-second timer. If no Cart updated, Click on within the cart context, or View page event occurs within that window, the popup shows. Reset the timer on any cart interaction so active shoppers aren't interrupted.

        Variant: C (no popup: baseline)
          No DOM changes: measures the intrinsic recovery rate without any popup intervention. This baseline is critical: without it you can't tell whether the popups CAUSE recovery or whether users would have returned anyway.

        The Visual Editor allows the user to refine the popup copy, styling, animation (slide-up vs. fade-in), and the email-capture handoff to the merchant's email tool.

        Notes:
        - The element ids "popup-save-cart" and "popup-dismiss" stay the same across Control and Variant B so engagement aggregates cleanly. Variant C has neither (no popup rendered).
        - Popup engagement rate = clicks on "popup-save-cart" divided by total exposures for that variant.
        - Variant C's no-popup baseline is essential, not optional. Without it the experiment cannot separate causal lift from return-anyway behavior.
        - For Variant B's "cart idle" detection, the timer resets on any cart-related interaction. The 30-second window is a starting point; tune it to your audience's typical cart-decision time.
        - Email captured from the popup feeds your existing abandoned-cart email journey: this experiment tests whether the popup adds value above intrinsic return, not whether email recovery itself works.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Cart popup timing test

Compares exit-intent, a 30 second delay and no popup at all on cart pages, scored on orders placed within 24 hours.

## What it does

1. **Set up the popup timing test** (`create_experiment`)

   Splits desktop cart visitors three ways: an exit-intent popup, a popup after 30 seconds of an idle cart, and no popup as a baseline. The winner is the variant with the most orders within 24 hours of being shown. Desktop only, because exit-intent needs mouse tracking, and once per session.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
