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
  title: 'Trial CTA copy test'
  shortDescription: 'Compares three wordings of the trial signup button to see which one gets more people to sign up.'
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
      title: 'Set up the CTA copy test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Splits landing page traffic three ways between your current button copy, Try It Free for 14 Days, and Get Started, No Credit Card. The winner is the copy with the most completed signups after exposure.'
      prompt: |
        Create a CLIENT EXPERIMENT on /experiences titled "Free Trial CTA Copy Test".

        This recipe has TWO creation paths: both must be completed:

        ═══ PATH 1: Top-level configuration (Setup tab) ═══

        Experience type: client_experiment (random traffic split, no per-variant targeting)

        Variants:
        - Control (33% traffic): existing CTA copy
        - Variant B (33% traffic): "Try It Free for 14 Days"
        - Variant C (34% traffic): "Get Started: No Credit Card"

        Targeting (experience-wide):
        - Pages: page URL contains "/" (the homepage/landing page): adjust to specific landing page paths as needed
        - Devices: any (desktop + mobile + tablet)
        - Audience: all visitors
        - Display frequency: always

        Primary metric: Completed an experience goal for this experience (the goal fires when the user completes signup after exposure)
        Secondary metrics:
        - Click on the "hero-cta" element (CTA click-through rate)
        - User created within 7 days of Exposed to experience (signup conversion)

        Guardrail: bounce rate (sessions with only one View page) must not increase by >5% vs. control

        Schedule: 14 days minimum, 95% statistical significance required to ship

        ═══ PATH 2: Variant HTML content (Visual Editor) ═══

        For CLIENT experiments, each variant ships an HTML object that the Visual Editor renders. Open each variant in the Visual Editor (/experience/:id/variants/:variantId/editor) and apply the DOM patches below.

        Variant: Control
          HTML (no change: measures the existing CTA):
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
            Get Started: No Credit Card
          </button>

        The Visual Editor lets the user refine the HTML (typography, color, animation) without leaving the canvas. Exposed to experience fires the moment the variant DOM is applied to the page; Completed an experience goal fires when the downstream conversion matches the configured goal. Both are recorded automatically once the experience is live, so nothing needs manual instrumentation. The click metric matches the button's id attribute, so keep the id "hero-cta" in every variant for consistent measurement.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Trial CTA copy test

Compares three wordings of the trial signup button to see which one gets more people to sign up.

## What it does

1. **Set up the CTA copy test** (`create_experiment`)

   Splits landing page traffic three ways between your current button copy, Try It Free for 14 Days, and Get Started, No Credit Card. The winner is the copy with the most completed signups after exposure.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
