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
    required: false
  - name: cta_element_id
    type: string
    label: Id of the trial signup button
    default: hero-cta
    required: false
  - name: variant_b_copy
    type: string
    label: Variant B button copy
    default: Try It Free for 14 Days
    required: false
  - name: variant_c_copy
    type: string
    label: Variant C button copy
    default: 'Get Started: No Credit Card'
    required: false
  - name: control_traffic_pct
    type: number
    label: Control traffic share (%)
    default: 33
    required: false
  - name: variant_b_traffic_pct
    type: number
    label: Variant B traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_pct
    type: number
    label: Variant C traffic share (%)
    default: 34
    required: false
  - name: min_test_days
    type: duration
    label: Minimum test duration
    default: 14 d
    required: false
  - name: significance_level
    type: number
    label: Required statistical significance (%)
    default: 95
    required: false
  - name: signup_window
    type: duration
    label: Signup conversion window after exposure
    default: 7 d
    required: false
  - name: bounce_guardrail_pct
    type: number
    label: Maximum allowed bounce rate increase vs. control (%)
    default: 5
    required: false
  requirements:
  - slot: cta_click_event
    kind: event
    meaning: A visitor clicked a page element
    properties:
    - name: target_id
      type: string
      meaning: Id of the clicked element
      optional: false
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page
  steps:
  - id: s1
    builds: experiment
    uses:
    - cta_click_event
    - user_created_event
    - page_view_event
    - landing_path
    - cta_element_id
    - variant_b_copy
    - variant_c_copy
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - min_test_days
    - significance_level
    - signup_window
    - bounce_guardrail_pct
    instruction: 'Create a website experiment named "Free Trial CTA Copy Test" on pages whose URL contains "{landing_path}",
      all visitors, all devices, shown always, with a random split. It changes only the text of the button with id {cta_element_id},
      keeping the id on every variant. Control ({control_traffic_pct}%): the current text. Variant B ({variant_b_traffic_pct}%):
      "{variant_b_copy}". Variant C ({variant_c_traffic_pct}%): "{variant_c_copy}". Primary goal: {user_created_event} within
      {signup_window} of exposure. Secondary: click-through on the button, {cta_click_event} where {cta_click_event.target_id}
      is {cta_element_id}. Guardrail: the bounce rate (sessions with one {page_view_event}) must not rise more than {bounce_guardrail_pct}%
      against control. Run at least {min_test_days} and call a winner only at {significance_level}% significance.'
---

# Trial CTA copy test

Slash command: /free-trial-cta-copy-test

## Step 1: Set up the CTA copy test

Create a website experiment named "Free Trial CTA Copy Test" on pages whose URL contains "/", all visitors, all devices, shown always, with a random split. It changes only the text of the button with id hero-cta, keeping the id on every variant. Control (33%): the current text. Variant B (33%): "Try It Free for 14 Days". Variant C (34%): "Get Started: No Credit Card". Primary goal: user created event within 7 d of exposure. Secondary: click-through on the button, cta click event where target id is hero-cta. Guardrail: the bounce rate (sessions with one page view event) must not rise more than 5% against control. Run at least 14 d and call a winner only at 95% significance.
