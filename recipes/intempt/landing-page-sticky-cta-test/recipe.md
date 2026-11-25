---
frontmatter_id: landing-page-sticky-cta-test
slash_command: /landing-page-sticky-cta-test
description: Compares an always-visible sticky CTA bar, one that fades in after the hero, and no sticky bar at all on marketing
  pages, scored on demo requests and signups.
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
    the hero) to find which lifts demo requests and signups.
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
  - name: scroll_50_guardrail_pct
    type: number
    label: Maximum allowed drop in scroll-to-50% rate (%)
    default: 10
    required: false
  - name: cta_bar_message
    type: text
    label: Sticky bar message
    default: See it in action in 15 minutes
    required: false
  - name: cta_button_label
    type: string
    label: Sticky bar button label
    default: Book a demo
    required: false
  requirements:
  - slot: demo_request_form_submitted
    kind: event
    meaning: A visitor submitted the demo-request form
  - slot: user_signed_up
    kind: event
    meaning: A user created an account through signup
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
  steps:
  - id: s1
    builds: experiment
    uses:
    - demo_request_form_submitted
    - user_signed_up
    - cta_click
    - page_scroll_depth
    - test_name
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - fade_in_scroll_threshold_px
    - test_duration
    - min_visitors_per_variant
    - scroll_50_guardrail_pct
    - cta_bar_message
    - cta_button_label
    instruction: 'Create a client-side experiment named "{test_name}" for all visitors on all devices, on pages whose URL
      is the homepage or contains /solutions, /features, /product or /pricing. Variants: Control ({control_traffic_pct}%)
      with no sticky bar; Variant B ({variant_b_traffic_pct}%) with a sticky bar fixed to the top of the page from page load;
      Variant C ({variant_c_traffic_pct}%) with the same bar fading in once the visitor scrolls past {fade_in_scroll_threshold_px}
      px and hiding above it. The bar shows "{cta_bar_message}" and a button "{cta_button_label}" with target_id sticky-cta-button
      in both B and C. Primary metric: visitors who did {demo_request_form_submitted} or {user_signed_up} in the same session
      as exposure. Secondary metrics: {cta_click} with {cta_click.target_id} equal to sticky-cta-button, and equal to hero-cta-button.
      Guardrail: the share of visitors with {page_scroll_depth} where {page_scroll_depth.depth_pct} is 50 or more must not
      drop more than {scroll_50_guardrail_pct}%. Run for {test_duration} and at least {min_visitors_per_variant} unique visitors
      per variant.'
---

# Sticky CTA bar test

Slash command: /landing-page-sticky-cta-test

## Step 1: Set up the sticky CTA test

Create a client-side experiment named "Landing Page Sticky CTA" for all visitors on all devices, on pages whose URL is the homepage or contains /solutions, /features, /product or /pricing. Variants: Control (34%) with no sticky bar; Variant B (33%) with a sticky bar fixed to the top of the page from page load; Variant C (33%) with the same bar fading in once the visitor scrolls past 600 px and hiding above it. The bar shows "See it in action in 15 minutes" and a button "Book a demo" with target_id sticky-cta-button in both B and C. Primary metric: visitors who did demo request form submitted or user signed up in the same session as exposure. Secondary metrics: cta click with target id equal to sticky-cta-button, and equal to hero-cta-button. Guardrail: the share of visitors with page scroll depth where depth pct is 50 or more must not drop more than 10%. Run for 14 d and at least 1500 unique visitors per variant.
