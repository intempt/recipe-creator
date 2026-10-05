---
name: cart-abandonment-popup-timing
description: |
  Use when a user mentions "cart abandonment popup timing", or asks for related help. Test when to show the save-your-cart popup: exit-intent vs. delay vs. no popup. Client experiment.
arguments: []
intempt:
  id: cart-abandonment-popup-timing
  version: 1.0.1
  slashCommand: /experiment-recipe
  group: Experiments
  shortDescription: "Create a client experiment on /experiences comparing exit-intent, 30-second delay, and no popup, reporting cart recovery conversion."
  availability: coming-soon
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
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Cart Popup Timing".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: client_experiment

        Variants:
        - Control (34%): exit-intent popup (mouse leaves viewport)
        - Variant B (33%): 30-second delay popup after cart is idle
        - Variant C (33%): no popup (control baseline — measures intrinsic recovery rate)

        Targeting:
        - Pages: page URL contains "/cart" OR cart_created has occurred in the current session
        - Devices: desktop only (exit-intent requires mouse tracking; mobile doesn't have hover events)
        - Audience: visitors with at least one cart_created in the current session
        - Display frequency: once_per_session

        Primary metric: goal_completed_in_experience where experience_id = <this> (goal: order_created within 24 hours of exposure)
        Secondary metrics:
        - click_on where target_id = "popup-save-cart" (popup engagement rate)
        - click_on where target_id = "popup-dismiss" (dismissal rate)
        - Email capture rate from popup (submit_on the popup form)
        - order_created within 24 hours

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
              <p>Save your cart and we'll send you a reminder — no pressure.</p>
              <form class="popup-email-form" id="popup-email-form">
                <input type="email" name="email" placeholder="your@email.com" required />
                <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
              </form>
            </div>
          </div>

          Trigger logic: when cart_created fires, start a 30-second timer. If no cart_updated, click_on within the cart context, or page_viewed event occurs within that window, the popup shows. Reset the timer on any cart interaction so active shoppers aren't interrupted.

        Variant: C (no popup — baseline)
          No DOM changes — measures the intrinsic recovery rate without any popup intervention. This baseline is critical: without it you can't tell whether the popups CAUSE recovery or whether users would have returned anyway.

        The Visual Editor allows the user to refine the popup copy, styling, animation (slide-up vs. fade-in), and the email-capture handoff to the merchant's email tool.

        Taxonomy notes:
        - cart_created is canonical (fires when items are added).
        - target_id values "popup-save-cart" and "popup-dismiss" are preserved across Variants Control and B for consistent click_on aggregation. Variant C has neither (no popup rendered).
        - The "popup engagement rate" = click_on (target_id = "popup-save-cart") count / total exposures with that variant.
        - Variant C's baseline is essential and not optional. Skipping it makes the experiment unable to distinguish causal lift from return-anyway behavior.
        - For Variant B's "cart idle" detection, the timer resets on any cart-related interaction. The 30-second window is a starting point; tune based on your audience's typical cart-decision time.
        - Email capture from the popup feeds into your existing abandoned-cart email journey — this experiment tests whether the popup adds value above intrinsic return, not whether email recovery itself works.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Cart Abandonment Popup Timing

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Cart Popup Timing".

   ═══ PATH 1: Top-level configuration ═══

   Experience type: client_experiment

   Variants:
   - Control (34%): exit-intent popup (mouse leaves viewport)
   - Variant B (33%): 30-second delay popup after cart is idle
   - Variant C (33%): no popup (control baseline — measures intrinsic recovery rate)

   Targeting:
   - Pages: page URL contains "/cart" OR cart_created has occurred in the current session
   - Devices: desktop only (exit-intent requires mouse tracking; mobile doesn't have hover events)
   - Audience: visitors with at least one cart_created in the current session
   - Display frequency: once_per_session

   Primary metric: goal_completed_in_experience where experience_id = <this> (goal: order_created within 24 hours of exposure)
   Secondary metrics:
   - click_on where target_id = "popup-save-cart" (popup engagement rate)
   - click_on where target_id = "popup-dismiss" (dismissal rate)
   - Email capture rate from popup (submit_on the popup form)
   - order_created within 24 hours

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
         <p>Save your cart and we'll send you a reminder — no pressure.</p>
         <form class="popup-email-form" id="popup-email-form">
           <input type="email" name="email" placeholder="your@email.com" required />
           <button type="submit" class="popup-cta" id="popup-save-cart">Save my cart</button>
         </form>
       </div>
     </div>

     Trigger logic: when cart_created fires, start a 30-second timer. If no cart_updated, click_on within the cart context, or page_viewed event occurs within that window, the popup shows. Reset the timer on any cart interaction so active shoppers aren't interrupted.

   Variant: C (no popup — baseline)
     No DOM changes — measures the intrinsic recovery rate without any popup intervention. This baseline is critical: without it you can't tell whether the popups CAUSE recovery or whether users would have returned anyway.

   The Visual Editor allows the user to refine the popup copy, styling, animation (slide-up vs. fade-in), and the email-capture handoff to the merchant's email tool.

   Taxonomy notes:
   - cart_created is canonical (fires when items are added).
   - target_id values "popup-save-cart" and "popup-dismiss" are preserved across Variants Control and B for consistent click_on aggregation. Variant C has neither (no popup rendered).
   - The "popup engagement rate" = click_on (target_id = "popup-save-cart") count / total exposures with that variant.
   - Variant C's baseline is essential and not optional. Skipping it makes the experiment unable to distinguish causal lift from return-anyway behavior.
   - For Variant B's "cart idle" detection, the timer resets on any cart-related interaction. The 30-second window is a starting point; tune based on your audience's typical cart-decision time.
   - Email capture from the popup feeds into your existing abandoned-cart email journey — this experiment tests whether the popup adds value above intrinsic return, not whether email recovery itself works.
   ```
