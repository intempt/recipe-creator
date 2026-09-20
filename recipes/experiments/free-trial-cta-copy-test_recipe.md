---
name: free-trial-cta-copy-test
description: |
  Use when a user mentions "free trial cta copy test", or asks for related help. Test which CTA button copy drives more trial signups on a landing page. Client experiment with random traffic split.
arguments: []
intempt:
  id: free-trial-cta-copy-test
  version: 1.0.0
  slashCommand: /free-trial-cta-copy-test
  group: Experiments
  shortDescription: "Test which CTA button copy drives more trial signups on a landing page. Client experiment with random traffic split."
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
      title: "Configure Website Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: "Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2)."
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Free Trial CTA Copy Test".

        This recipe has TWO creation paths — both must be completed:

        ═══ PATH 1: Top-level configuration (Setup tab) ═══

        Experience type: client_experiment (random traffic split, no per-variant targeting)

        Variants:
        - Control (33% traffic): existing CTA copy
        - Variant B (33% traffic): "Try It Free for 14 Days"
        - Variant C (34% traffic): "Get Started — No Credit Card"

        Targeting (experience-wide):
        - Pages: page URL contains "/" (the homepage/landing page) — adjust to specific landing page paths as needed
        - Devices: any (desktop + mobile + tablet)
        - Audience: all visitors
        - Display frequency: always

        Primary metric: goal_completed_in_experience where experience_id = <this experience> (the goal fires when the user completes signup after exposure)
        Secondary metrics:
        - click_on where target_id = "hero-cta" (CTA click-through rate)
        - user_created within 7 days of exposed_to_experience (signup conversion)

        Guardrail: bounce rate (sessions with only one page_viewed) must not increase by >5% vs. control

        Schedule: 14 days minimum, 95% statistical significance required to ship

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        For CLIENT experiments, each variant ships an HTML object that the Visual Editor renders. Open each variant in the Visual Editor (/experience/:id/variants/:variantId/editor) and apply the DOM patches below.

        Variant: Control
          HTML (no change — measures the existing CTA):
          <button class="hero-cta" id="hero-cta" data-variant="control">
            [keeps existing CTA copy]
          </button>

        Variant: B
          HTML target selector: #hero-cta
          Replacement HTML:
          <button class="hero-cta" id="hero-cta" data-variant="b">
            Try It Free for 14 Days
          </button>

        Variant: C
          HTML target selector: #hero-cta
          Replacement HTML:
          <button class="hero-cta" id="hero-cta" data-variant="c">
            Get Started — No Credit Card
          </button>

        The Visual Editor lets the user refine the HTML (typography, color, animation) without leaving the canvas. The exposed_to_experience event fires the moment the variant DOM is applied to the page; goal_completed_in_experience fires when the downstream conversion event matches the configured goal.

        Taxonomy notes:
        - exposed_to_experience and goal_completed_in_experience are canonical platform events; they are emitted automatically by the SDK once the experience is live. The recipe does not need to instrument these manually.
        - click_on.target_id matches the button's id attribute. Ensure the id is preserved across all variants for consistent measurement.
        - user_created is the canonical signup event.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---

# Free Trial CTA Copy Test

## Procedure

1. **Configure Website Experiment** [`create_experiment`] — Follow the two-path setup below: configure the experience top-level (Path 1), then author the variant content (Path 2). → produces: experiment

   ```text
   Create a CLIENT EXPERIMENT on /experiences titled "Free Trial CTA Copy Test".

   This recipe has TWO creation paths — both must be completed:

   ═══ PATH 1: Top-level configuration (Setup tab) ═══

   Experience type: client_experiment (random traffic split, no per-variant targeting)

   Variants:
   - Control (33% traffic): existing CTA copy
   - Variant B (33% traffic): "Try It Free for 14 Days"
   - Variant C (34% traffic): "Get Started — No Credit Card"

   Targeting (experience-wide):
   - Pages: page URL contains "/" (the homepage/landing page) — adjust to specific landing page paths as needed
   - Devices: any (desktop + mobile + tablet)
   - Audience: all visitors
   - Display frequency: always

   Primary metric: goal_completed_in_experience where experience_id = <this experience> (the goal fires when the user completes signup after exposure)
   Secondary metrics:
   - click_on where target_id = "hero-cta" (CTA click-through rate)
   - user_created within 7 days of exposed_to_experience (signup conversion)

   Guardrail: bounce rate (sessions with only one page_viewed) must not increase by >5% vs. control

   Schedule: 14 days minimum, 95% statistical significance required to ship

   ═══ PATH 2: Variant HTML content (Visual Editor) ═══

   For CLIENT experiments, each variant ships an HTML object that the Visual Editor renders. Open each variant in the Visual Editor (/experience/:id/variants/:variantId/editor) and apply the DOM patches below.

   Variant: Control
     HTML (no change — measures the existing CTA):
     <button class="hero-cta" id="hero-cta" data-variant="control">
       [keeps existing CTA copy]
     </button>

   Variant: B
     HTML target selector: #hero-cta
     Replacement HTML:
     <button class="hero-cta" id="hero-cta" data-variant="b">
       Try It Free for 14 Days
     </button>

   Variant: C
     HTML target selector: #hero-cta
     Replacement HTML:
     <button class="hero-cta" id="hero-cta" data-variant="c">
       Get Started — No Credit Card
     </button>

   The Visual Editor lets the user refine the HTML (typography, color, animation) without leaving the canvas. The exposed_to_experience event fires the moment the variant DOM is applied to the page; goal_completed_in_experience fires when the downstream conversion event matches the configured goal.

   Taxonomy notes:
   - exposed_to_experience and goal_completed_in_experience are canonical platform events; they are emitted automatically by the SDK once the experience is live. The recipe does not need to instrument these manually.
   - click_on.target_id matches the button's id attribute. Ensure the id is preserved across all variants for consistent measurement.
   - user_created is the canonical signup event.
   ```
