---
frontmatter_id: onboarding-flow-guided-vs-self-serve
slash_command: /onboarding-flow-guided-vs-self-serve
description: Runs an A/B/C test of three onboarding flows (self-serve checklist, guided wizard, video-first) for new signups
  and scores which drives activation within 7 days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Runs an A/B/C test of three onboarding flows (self-serve checklist, guided wizard, video-first) for new signups
    and scores which drives activation within 7 days.
  parameters:
  - name: control_traffic
    type: number
    label: Control traffic share (%)
    default: 34
    required: false
  - name: variant_b_traffic
    type: number
    label: Guided wizard traffic share (%)
    default: 33
    required: false
  - name: variant_c_traffic
    type: number
    label: Video-first traffic share (%)
    default: 33
    required: false
  - name: new_user_window
    type: duration
    label: How new a user must be
    default: 1 h
    required: false
  - name: activation_window
    type: duration
    label: Activation window after exposure
    default: 7 d
    required: false
  - name: test_duration
    type: duration
    label: Test duration
    default: 30 d
    required: false
  - name: return_window
    type: duration
    label: Return visit window
    default: 2 d
    required: false
  - name: onboarding_page_path
    type: string
    label: Onboarding page path
    default: /onboarding
    required: false
  - name: key_feature_target_id
    type: string
    label: target_id of the key feature click
    default: key-feature
    required: false
  requirements:
  - slot: activation_event
    kind: event
    meaning: A user reached the product's activation milestone
  - slot: ui_click
    kind: event
    meaning: A user clicked a tracked element in the product
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked element
      optional: false
  - slot: session_start
    kind: event
    meaning: A user started a session in the product
  steps:
  - id: s1
    builds: experiment
    uses:
    - activation_event
    - ui_click
    - session_start
    - control_traffic
    - variant_b_traffic
    - variant_c_traffic
    - new_user_window
    - activation_window
    - test_duration
    - return_window
    - onboarding_page_path
    - key_feature_target_id
    instruction: 'Create a client-side experiment named "Onboarding Flow: Guided vs Self-Serve" on the page {onboarding_page_path},
      all devices, for users created in the last {new_user_window}, shown once per user. Variants: Control ({control_traffic}%)
      keeps the self-serve checklist; Variant B ({variant_b_traffic}%) is a guided wizard with progressive steps and tooltips;
      Variant C ({variant_c_traffic}%) is video-first with an embedded walkthrough. Primary metric: users who did {activation_event}
      within {activation_window} of exposure. Secondary metrics: median time from exposure to the first {ui_click} with {ui_click.target_id}
      equal to {key_feature_target_id}; users who did {session_start} again within {return_window} of signup. Run for at least
      {test_duration}.'
---

# Guided vs self-serve onboarding

Slash command: /onboarding-flow-guided-vs-self-serve

## Step 1: Set up the onboarding test

Create a client-side experiment named "Onboarding Flow: Guided vs Self-Serve" on the page /onboarding, all devices, for users created in the last 1 h, shown once per user. Variants: Control (34%) keeps the self-serve checklist; Variant B (33%) is a guided wizard with progressive steps and tooltips; Variant C (33%) is video-first with an embedded walkthrough. Primary metric: users who did activation event within 7 d of exposure. Secondary metrics: median time from exposure to the first ui click with target id equal to key-feature; users who did session start again within 2 d of signup. Run for at least 30 d.
