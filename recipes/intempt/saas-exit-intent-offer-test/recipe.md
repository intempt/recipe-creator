---
frontmatter_id: saas-exit-intent-offer-test
slash_command: /saas-exit-intent-offer-test
description: Tests which offer to show desktop visitors leaving SaaS marketing pages (discount, comparison guide, content
  download, exit survey, or nothing) to find the best lead-generating exit popup.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tests which offer to show desktop visitors leaving SaaS marketing pages (discount, comparison guide, content download,
    exit survey, or nothing) to find the best lead-generating exit popup.
  parameters:
  - name: experimentName
    type: string
    label: Experiment name
    default: SaaS Exit-Intent Offer
    required: false
  - name: testDurationDays
    type: duration
    label: Test duration
    default: 21 d
    required: false
  - name: minExitIntentsPerVariant
    type: number
    label: Minimum exit intents per variant
    default: 1000
    required: false
  - name: engagementThresholdSeconds
    type: number
    label: Seconds on page before the popup can show
    default: 30
    required: false
  - name: displayFrequency
    type: enum
    label: Display frequency
    default: once_per_session
    required: false
    options:
    - once_per_session
    - always
  - name: discountOffer
    type: string
    label: Discount offer headline
    default: Get 50% off your first month
    required: false
  - name: dismissRateGuardrailPercent
    type: number
    label: Max popup dismiss rate (%)
    default: 80
    required: false
  requirements:
  - slot: form_submitted
    kind: event
    meaning: A visitor submitted a form on the website, such as a demo request, download or survey form
    properties:
    - name: form_name
      type: string
      meaning: Name of the submitted form
      optional: false
  - slot: demo_request_form_event
    kind: event
    meaning: A visitor submitted the demo-request form
  steps:
  - id: s1
    builds: experiment
    uses:
    - form_submitted
    - demo_request_form_event
    - experimentName
    - testDurationDays
    - minExitIntentsPerVariant
    - engagementThresholdSeconds
    - displayFrequency
    - discountOffer
    - dismissRateGuardrailPercent
    instruction: 'Create a client-side experiment named "{experimentName}" for desktop visitors who have not submitted a form,
      on pages whose URL contains /pricing, /features or /solutions or is the homepage, never on checkout or signup pages,
      shown {displayFrequency}. The popup opens when the mouse leaves the top of the window after {engagementThresholdSeconds}
      seconds on the page. Five variants at 20% each: Control shows no popup; Variant B shows the offer "{discountOffer}"
      with a claim form; Variant C offers a comparison guide download; Variant D offers a content download for an email address;
      Variant E asks what stopped the visitor from booking a demo today. Primary metric: visitors who did {form_submitted}
      from the popup. Secondary metrics: {form_submitted} per {form_submitted.form_name}; visitors who did {demo_request_form_event}
      within 14 days of exposure. Guardrail: the popup dismiss rate must stay under {dismissRateGuardrailPercent}%. Run for
      {testDurationDays} and at least {minExitIntentsPerVariant} exit intents per variant.'
---

# Exit-intent offer test

Slash command: /saas-exit-intent-offer-test

## Step 1: Set up the exit-intent test

Create a client-side experiment named "SaaS Exit-Intent Offer" for desktop visitors who have not submitted a form, on pages whose URL contains /pricing, /features or /solutions or is the homepage, never on checkout or signup pages, shown once_per_session. The popup opens when the mouse leaves the top of the window after 30 seconds on the page. Five variants at 20% each: Control shows no popup; Variant B shows the offer "Get 50% off your first month" with a claim form; Variant C offers a comparison guide download; Variant D offers a content download for an email address; Variant E asks what stopped the visitor from booking a demo today. Primary metric: visitors who did form submitted from the popup. Secondary metrics: form submitted per form name; visitors who did demo request form event within 14 days of exposure. Guardrail: the popup dismiss rate must stay under 80%. Run for 21 d and at least 1000 exit intents per variant.
