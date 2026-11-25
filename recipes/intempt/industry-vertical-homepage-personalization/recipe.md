---
frontmatter_id: industry-vertical-homepage-personalization
slash_command: /industry-vertical-homepage-personalization
description: Visitors you can identify, such as known accounts or logged in users, see a homepage hero and proof points matched to their segment. Unidentified visitors see the generic one.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Identified visitors from known accounts or logged-in users see a homepage hero and proof points for their industry;
    unidentified visitors see the generic homepage.
  parameters:
  - name: experience_title
    type: string
    label: Experience title
    default: Industry Vertical Homepage
    required: false
  - name: target_pages
    type: text
    label: Target pages
    default: /, /solutions, /pricing
    required: false
  - name: display_frequency
    type: enum
    label: Display frequency
    default: always
    required: false
    options:
    - always
    - once_per_session
    - once_per_day
  - name: schedule
    type: enum
    label: Schedule
    default: continuous
    required: false
    options:
    - continuous
    - time_bound
  - name: tech_industries
    type: text
    label: Technology / SaaS industry values
    default: Technology, SaaS, Software
    required: false
  - name: finance_industries
    type: text
    label: Financial Services industry values
    default: Banking, Financial Services, Insurance, Fintech
    required: false
  - name: healthcare_industries
    type: text
    label: Healthcare industry values
    default: Healthcare, Health Tech, Pharmaceuticals, Medical Devices
    required: false
  - name: manufacturing_industries
    type: text
    label: Manufacturing / Industrial industry values
    default: Manufacturing, Industrial, Logistics, Supply Chain
    required: false
  requirements:
  - slot: industry_attribute
    kind: attribute
    meaning: The account industry of a visitor's company, populated through firmographic enrichment
  - slot: demo_request_event
    kind: event
    meaning: A visitor submitted the demo-request form
    properties:
    - name: industry
      type: string
      meaning: Industry segment of the visitor at submission
      optional: true
  - slot: primary_cta_event
    kind: event
    meaning: A visitor clicked the primary call-to-action on a marketing page
    properties:
    - name: industry
      type: string
      meaning: Industry segment of the visitor at click
      optional: true
    optional: true
  steps:
  - id: s1
    builds: personalization
    uses:
    - industry_attribute
    - demo_request_event
    - primary_cta_event
    - target_pages
    - display_frequency
    - schedule
    - tech_industries
    - finance_industries
    - healthcare_industries
    - manufacturing_industries
    - experience_title
    instruction: 'Create a client personalization titled "{experience_title}" on the experiences page. Each variant shows
      to one industry audience; there is no random split. Control (audience: all visitors) shows the generic homepage hero
      and proof points, including to visitors with no known industry. Variant B (Technology / SaaS) shows to visitors whose
      {industry_attribute} is one of {tech_industries}. Variant C (Financial Services) to {industry_attribute} in {finance_industries}.
      Variant D (Healthcare) to {industry_attribute} in {healthcare_industries}. Variant E (Manufacturing / Industrial) to
      {industry_attribute} in {manufacturing_industries}. Each industry variant replaces the hero headline, sub-headline and
      the three proof points (customer logos and one customer quote) with ones from that industry. Targeting: pages {target_pages},
      any device, display frequency {display_frequency}. Metrics: {demo_request_event} submissions per industry audience,
      {primary_cta_event} clicks per audience, and demo-request conversion rate per industry. Schedule: {schedule}.'
---

# Homepage by visitor industry

Slash command: /industry-vertical-homepage-personalization

## Step 1: Set up the four industry heroes

Create a client personalization titled "Industry Vertical Homepage" on the experiences page. Each variant shows to one industry audience; there is no random split. Control (audience: all visitors) shows the generic homepage hero and proof points, including to visitors with no known industry. Variant B (Technology / SaaS) shows to visitors whose industry attribute is one of Technology, SaaS, Software. Variant C (Financial Services) to industry attribute in Banking, Financial Services, Insurance, Fintech. Variant D (Healthcare) to industry attribute in Healthcare, Health Tech, Pharmaceuticals, Medical Devices. Variant E (Manufacturing / Industrial) to industry attribute in Manufacturing, Industrial, Logistics, Supply Chain. Each industry variant replaces the hero headline, sub-headline and the three proof points (customer logos and one customer quote) with ones from that industry. Targeting: pages /, /solutions, /pricing, any device, display frequency always. Metrics: demo request event submissions per industry audience, primary cta event clicks per audience, and demo-request conversion rate per industry. Schedule: continuous.
