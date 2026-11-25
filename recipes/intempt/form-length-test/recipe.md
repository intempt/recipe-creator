---
frontmatter_id: form-length-test
slash_command: /form-length-test
description: Compares a 3, 5 and 7 field demo request form, so you can see what each extra field costs you in submissions
  and whether longer forms bring better-qualified leads.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Runs a split test of 3, 5 and 7 field demo request forms to show how many submissions each extra field costs, and
    whether longer forms produce better-qualified leads.
  parameters:
  - name: form_pages
    type: text
    label: Pages whose URL contains one of these hold the demo form
    default: /demo, /contact, /get-started
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: min_views_per_variant
    type: number
    label: Minimum form views per variant
    default: 500
    required: false
  - name: control_traffic_share
    type: number
    label: 3-field (control) traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic_share
    type: number
    label: 5-field traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic_share
    type: number
    label: 7-field traffic share (%)
    default: 33
    required: false
  - name: lead_quality_window
    type: duration
    label: Lead quality measurement window after form submit
    default: 14 d
    required: false
  requirements:
  - slot: demo_form_submitted
    kind: event
    meaning: A visitor submitted the demo request form
  - slot: deal_created
    kind: event
    meaning: A deal or sales opportunity was created for a lead
  steps:
  - id: s1
    builds: experiment
    uses:
    - demo_form_submitted
    - deal_created
    - form_pages
    - test_duration
    - min_views_per_variant
    - control_traffic_share
    - variant_b_traffic_share
    - variant_c_traffic_share
    - lead_quality_window
    instruction: 'Create a website experiment named "Demo Request Form Length" on pages whose URL contains one of {form_pages},
      for all visitors who reach the form, any device, shown always, changing the .demo-request-form element. Control ({control_traffic_share}%):
      3 fields, name, work email and company. Variant B ({variant_b_traffic_share}%): adds job title and a team size dropdown
      (1-10, 11-50, 51-200, 201-1000, 1000+). Variant C ({variant_c_traffic_share}%): adds an optional phone field and a required
      text box asking what they want to solve. The submit button keeps the same id in every variant. Primary goal: {demo_form_submitted}
      in the session of exposure. Secondary: per-field abandonment, and the share of submitters with a {deal_created} within
      {lead_quality_window}. Guardrail: the deal rate must not fall by more than the gain in submissions. Run {test_duration}
      and until each variant has {min_views_per_variant} form views.'
---

# Demo form length test

Slash command: /form-length-test

## Step 1: Set up the form length test

Create a website experiment named "Demo Request Form Length" on pages whose URL contains one of /demo, /contact, /get-started, for all visitors who reach the form, any device, shown always, changing the .demo-request-form element. Control (34%): 3 fields, name, work email and company. Variant B (33%): adds job title and a team size dropdown (1-10, 11-50, 51-200, 201-1000, 1000+). Variant C (33%): adds an optional phone field and a required text box asking what they want to solve. The submit button keeps the same id in every variant. Primary goal: demo form submitted in the session of exposure. Secondary: per-field abandonment, and the share of submitters with a deal created within 14 d. Guardrail: the deal rate must not fall by more than the gain in submissions. Run 21 d and until each variant has 500 form views.
