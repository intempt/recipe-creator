---
frontmatter_id: landing-page-sticky-cta-test
slash_command: /landing-page-sticky-cta-test
description: Compares an always-visible sticky CTA bar, one that fades in after the hero, and no sticky bar at all on marketing pages.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Runs a three-way test of a sticky call-to-action bar on marketing pages (none, always visible, or fades in after
    the hero) to find which lifts demo requests and signups without hurting bounce or scroll.
  parameters:
  - name: test_name
    type: string
    label: Experiment title
    default: Landing Page Sticky CTA
    required: false
  - name: control_traffic_pct
    type: number
    label: Control variant traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_pct
    type: number
    label: Variant B (always-visible bar) traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_pct
    type: number
    label: Variant C (fade-in bar) traffic share (%)
    default: 33
    required: false
  - name: fade_in_scroll_threshold_px
    type: number
    label: Scroll depth that triggers Variant C fade-in (px)
    default: 600
    required: false
  - name: fade_in_duration_ms
    type: number
    label: Variant C fade-in transition (ms)
    default: 300
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 14 d
    required: false
  - name: min_visitors_per_variant
    type: number
    label: Minimum unique visitors per variant
    default: 1500
    required: false
  - name: bounce_rate_guardrail_pct
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  - name: scroll_50_guardrail_pct
    type: number
    label: Maximum allowed drop in scroll-to-50% rate (%)
    default: 10
    required: false
  - name: cta_bar_message
    type: text
    label: Sticky bar message
    default: '[Brand]: see it in action in 15 minutes'
    required: false
  - name: cta_button_label
    type: string
    label: Sticky bar button label
    default: Book a demo
    required: false
  requirements:
  - slot: experiment_platform
    kind: integration
    meaning: An experimentation platform that can run client-side experiments with visual editor variants on web pages
    channel: email
  - slot: demo_request_form_submitted
    kind: event
    meaning: A visitor submitted the demo-request form
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment the visitor was exposed to
      optional: false
  - slot: user_signed_up
    kind: event
    meaning: A user created an account through signup
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment the visitor was exposed to
      optional: false
  - slot: goal_completed_in_experience
    kind: event
    meaning: A visitor completed a goal while exposed to an experiment
    properties:
    - name: experience_id
      type: string
      meaning: Identifier of the experiment the visitor was exposed to
      optional: false
  - slot: cta_click
    kind: event
    meaning: A visitor clicked a tracked call-to-action element on the page
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element, e.g. sticky-cta-button or hero-cta-button
      optional: false
  - slot: page_scroll_depth
    kind: event
    meaning: A visitor reached a tracked scroll depth on a page
    properties:
    - name: depth_pct
      type: number
      meaning: Scroll depth reached as a percentage of the page
      optional: false
  - slot: marketing_landing_pages
    kind: attribute
    meaning: Visitor is on a marketing landing page (homepage, solutions, features, product, or pricing)
  steps:
  - id: s1
    builds: experiment
    uses:
    - experiment_platform
    - goal_completed_in_experience
    - cta_click
    - page_scroll_depth
    - marketing_landing_pages
    - demo_request_form_submitted
    - user_signed_up
    - test_name
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - fade_in_scroll_threshold_px
    - fade_in_duration_ms
    - test_duration
    - min_visitors_per_variant
    - bounce_rate_guardrail_pct
    - scroll_50_guardrail_pct
    - cta_bar_message
    - cta_button_label
    instruction: 'Create a client-side experiment titled "{test_name}" on the experiences page of {experiment_platform}. Variants:
      Control ({control_traffic_pct}%) with no sticky CTA, where the CTA appears only in the hero; Variant B ({variant_b_traffic_pct}%)
      with an always-visible sticky CTA bar fixed at the top of the page, shown immediately on load; Variant C ({variant_c_traffic_pct}%)
      with a fade-in sticky CTA bar that appears after the user scrolls past {fade_in_scroll_threshold_px} px and fades in
      over {fade_in_duration_ms} ms, hiding again when the user scrolls back above the threshold. Both sticky variants use
      the same markup: a bar with the message "{cta_bar_message}" and a button labeled "{cta_button_label}" with target_id
      "sticky-cta-button" (keep this identifier identical across B and C). Add body padding-top equal to the bar height so
      content is not hidden. Make the bar respect the mobile browser URL bar and avoid stacking with mobile browser chrome.
      Targeting: marketing landing pages only (homepage, /solutions, /features, /product, /pricing), all devices, all visitors,
      shown always within session. Primary metric: {goal_completed_in_experience} where experience_id equals this experiment,
      counting demo request submissions ({demo_request_form_submitted}) or signups ({user_signed_up}) within session of exposure.
      Secondary metrics: {cta_click} with target_id sticky-cta-button; {cta_click} with target_id hero-cta-button; bounce
      rate per variant; {page_scroll_depth}. Guardrails: bounce rate must not increase more than {bounce_rate_guardrail_pct}%;
      scroll-to-50% rate ({page_scroll_depth} at 50%) must not drop more than {scroll_50_guardrail_pct}%. Run for {test_duration}
      with at least {min_visitors_per_variant} unique visitors per variant.'
---

# Sticky CTA bar test

Slash command: /landing-page-sticky-cta-test

## Step 1: Set up the sticky CTA test

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
Primary metric: goal_completed_in_experience where experience_id = <this> (goal: Form submitted on demo-request OR User created via signup, within session of exposure)
Secondary metrics:
- Click on where target_id = "sticky-cta-button" (sticky CTA engagement rate)
- Click on where target_id = "hero-cta-button" (does sticky cannibalize hero clicks?)
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
- target_id="sticky-cta-button" must be preserved across variants B and C for consistent Click on aggregation.
- Variant C's fade-in is generally less intrusive but has slightly lower engagement than Variant B's always-visible. The test answers: which tradeoff wins for your audience?
- For dark-launching: ship Variant B first to a small traffic slice (5%) to confirm no layout regressions before full experiment ramp.
