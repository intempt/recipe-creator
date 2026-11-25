---
frontmatter_id: hero-static-vs-screenshot-test
slash_command: /hero-static-vs-screenshot-test
description: Compares your current hero image against a real product screenshot and a photo of customers or the team. Static images only.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests your current landing page hero image against a real product screenshot and a customer or team photo to find
    which image drives more form submissions and sign-ups.
  parameters:
  - name: experiment_title
    type: string
    label: Experiment title
    default: Hero Image Test
    required: false
  - name: landing_paths
    type: text
    label: Landing pages in the test (URL contains)
    default: /
    required: false
  - name: product_screenshot
    type: attachment
    label: Real product screenshot for variant B
    required: true
  - name: team_photo
    type: attachment
    label: Real photo of customers or the team for variant C
    required: true
  - name: test_duration_days
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: min_visitors_per_variant
    type: number
    label: Minimum visitors per variant
    default: 1500
    required: false
  - name: control_traffic_pct
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_pct
    type: number
    label: Product screenshot variant traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_pct
    type: number
    label: Customer/team photo variant traffic share (%)
    default: 33
    required: false
  - name: bounce_rate_guardrail_pct
    type: number
    label: Maximum allowed bounce rate increase (%)
    default: 5
    required: false
  - name: mobile_load_time_guardrail_ms
    type: number
    label: Maximum allowed mobile load time increase (ms)
    default: 200
    required: false
  requirements:
  - slot: demo_form_submitted
    kind: event
    meaning: A visitor submitted a demo, contact or signup form
  - slot: user_created
    kind: event
    meaning: A new user account was created
    optional: true
  - slot: primary_cta_clicked
    kind: event
    meaning: A visitor clicked the primary call-to-action on a landing page
  - slot: page_bounced
    kind: event
    meaning: A visitor left a landing page without any further interaction
  steps:
  - id: s1
    builds: experiment
    uses:
    - demo_form_submitted
    - user_created
    - primary_cta_clicked
    - page_bounced
    - experiment_title
    - landing_paths
    - product_screenshot
    - team_photo
    - test_duration_days
    - min_visitors_per_variant
    - control_traffic_pct
    - variant_b_traffic_pct
    - variant_c_traffic_pct
    - bounce_rate_guardrail_pct
    - mobile_load_time_guardrail_ms
    instruction: 'Create a website experiment named "{experiment_title}" on pages whose URL contains one of {landing_paths},
      all visitors, all devices, shown always, changing the .hero-image element. Control ({control_traffic_pct}%): the current
      hero image. Variant B ({variant_b_traffic_pct}%): the image {product_screenshot}. Variant C ({variant_c_traffic_pct}%):
      the image {team_photo}. Primary goal: {demo_form_submitted} or {user_created} in the session of exposure. Secondary:
      {primary_cta_clicked} rate, {page_bounced} rate, time on page and the share of visitors scrolling past 50%. Guardrails:
      the bounce rate must not rise more than {bounce_rate_guardrail_pct}% and mobile load time not more than {mobile_load_time_guardrail_ms}
      ms. Run {test_duration_days} and until each variant has {min_visitors_per_variant} visitors.'
---

# Landing page hero image test

Slash command: /hero-static-vs-screenshot-test

## Step 1: Set up the hero image test

Create a website experiment named "Hero Image Test" on pages whose URL contains one of /, all visitors, all devices, shown always, changing the .hero-image element. Control (34%): the current hero image. Variant B (33%): the image the real product screenshot for variant B. Variant C (33%): the image the real photo of customers or the team for variant C. Primary goal: demo form submitted or user created in the session of exposure. Secondary: primary cta clicked rate, page bounced rate, time on page and the share of visitors scrolling past 50%. Guardrails: the bounce rate must not rise more than 5% and mobile load time not more than 200 ms. Run 21 d and until each variant has 1500 visitors.
