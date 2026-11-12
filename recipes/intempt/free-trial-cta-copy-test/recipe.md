---
frontmatter_id: free-trial-cta-copy-test
slash_command: /free-trial-cta-copy-test
description: Compares three wordings of the trial signup button to see which one gets more people to sign up.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests three wordings of the free-trial signup button on the landing page to find which one gets more people to
    sign up, with a bounce-rate guardrail.
  parameters:
  - name: landing_path
    type: string
    label: Landing page URL contains
    default: /
  - name: variant_b_copy
    type: string
    label: Variant B button copy
    default: Try It Free for 14 Days
  - name: variant_c_copy
    type: string
    label: Variant C button copy
    default: 'Get Started: No Credit Card'
  - name: control_traffic_pct
    type: number
    label: Control traffic share (%)
    default: 33
  - name: variant_b_traffic_pct
    type: number
    label: Variant B traffic share (%)
    default: 33
  - name: variant_c_traffic_pct
    type: number
    label: Variant C traffic share (%)
    default: 34
  - name: min_test_days
    type: duration
    label: Minimum test duration
    default: 14 d
  - name: significance_level
    type: number
    label: Required statistical significance (%)
    default: 95
  - name: signup_window
    type: duration
    label: Signup conversion window after exposure
    default: 7 d
  - name: bounce_guardrail_pct
    type: number
    label: Maximum allowed bounce rate increase vs. control (%)
    default: 5
  requirements:
  - slot: cta_experiment_exposure_event
    kind: event
    meaning: A visitor was exposed to an experience variant on the page
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the visitor was exposed to
      optional: false
  - slot: goal_completed_event
    kind: event
    meaning: A visitor completed the goal of an experience after exposure (signup)
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experience the goal belongs to
      optional: false
  - slot: cta_click_event
    kind: event
    meaning: A visitor clicked a page element
    properties:
    - name: target_id
      type: string
      meaning: The id attribute of the clicked element
      optional: false
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page
  - slot: hero_cta_button
    kind: knowledge
    meaning: The trial signup button on the landing page with id hero-cta
  steps:
  - id: s1
    builds: experiment
    uses:
    - cta_experiment_exposure_event
    - goal_completed_event
    - cta_click_event
    - user_created_event
    - page_view_event
    - hero_cta_button
    - landing_path
    - variant_b_copy
    - variant_c_copy
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - min_test_days
    - significance_level
    - signup_window
    - bounce_guardrail_pct
    instruction: 'Create a client experiment titled "Free Trial CTA Copy Test" on the experiences page with random traffic
      split and no per-variant targeting. Variants: Control ({control_traffic_pct}% traffic) keeps the existing CTA copy;
      Variant B ({variant_b_traffic_pct}% traffic) uses "{variant_b_copy}"; Variant C ({variant_c_traffic_pct}% traffic) uses
      "{variant_c_copy}". Experience-wide targeting: page URL contains "{landing_path}" (adjust to specific landing page paths
      as needed), all devices (desktop, mobile, tablet), all visitors, display frequency always. Primary metric: goal_completed_event
      for this experience (the goal fires when the user completes signup after exposure). Secondary metrics: click on cta_click_event
      where target_id equals the hero_cta_button id (hero-cta) as CTA click-through rate; user_created_event within {signup_window}
      of exposure to the experience as signup conversion. Guardrail: bounce rate (sessions with only one page_view_event)
      must not increase by more than {bounce_guardrail_pct}% versus control. Schedule: run at least {min_test_days}; require
      {significance_level}% statistical significance before shipping. For each variant, open it in the Visual Editor and apply
      the HTML patches: Control keeps the existing button markup with class hero-cta, id hero-cta, and data-variant control,
      with no copy change. Variant B replaces the element with id hero-cta (class hero-cta, data-variant b) containing "{variant_b_copy}".
      Variant C replaces the element with id hero-cta (class hero-cta, data-variant c) containing "{variant_c_copy}". Keep
      the id hero-cta on every variant so click measurement stays consistent. Designers may refine typography, color, and
      animation in the editor without changing the id or the copy.'
---

# Trial CTA copy test

Slash command: /free-trial-cta-copy-test

## Step 1: Set up the CTA copy test

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
Primary metric: goal_completed_in_experience where experience_id = <this experience> (the goal fires when the user completes signup after exposure)
Secondary metrics:
- Click on where target_id = "hero-cta" (CTA click-through rate)
- User created within 7 days of exposed_to_experience (signup conversion)
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
The Visual Editor lets the user refine the HTML (typography, color, animation) without leaving the canvas. The exposed_to_experience event fires the moment the variant DOM is applied to the page; goal_completed_in_experience fires when the downstream conversion event matches the configured goal.
Taxonomy notes:
- exposed_to_experience and goal_completed_in_experience are canonical platform events; they are emitted automatically by the SDK once the experience is live. The recipe does not need to instrument these manually.
- Click on.target_id matches the button's id attribute. Ensure the id is preserved across all variants for consistent measurement.
- User created is the canonical signup event.
