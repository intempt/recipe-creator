---
frontmatter_id: abm-account-personalization
slash_command: /abm-account-personalization
description: Builds target account segments for enterprise SaaS, financial services and healthcare, and personalizes the homepage
  hero with industry-specific messaging for visitors from those accounts.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Builds three target account segments and shows visitors from those accounts a homepage hero tailored to their industry,
    while other visitors see the default hero.
  parameters:
  - name: primary_pages
    type: text
    label: Pages to personalize (homepage and key conversion pages)
    default: /, /pricing, /demo
    required: false
  - name: tier1_employee_min
    type: number
    label: Minimum employee count for tier-1 enterprise SaaS targets
    default: 1000
    required: false
  - name: tier1_fin_employee_min
    type: number
    label: Minimum employee count for tier-1 financial services targets
    default: 500
    required: false
  - name: tier2_health_employee_min
    type: number
    label: Minimum employee count for tier-2 healthcare targets
    default: 100
    required: false
  requirements:
  - slot: account_industry
    kind: attribute
    meaning: The account's industry, populated by enrichment
  - slot: account_employee_count
    kind: attribute
    meaning: The account's employee count, populated by enrichment
  - slot: demo_request_form_submitted
    kind: event
    meaning: A visitor submitted the demo-request form
  - slot: primary_cta_clicked
    kind: event
    meaning: A visitor clicked the primary call-to-action in the homepage hero
  steps:
  - id: s1
    builds: segment
    uses:
    - account_industry
    - account_employee_count
    - tier1_employee_min
    instruction: Build a new segment of accounts named "ABM Tier 1 Enterprise SaaS". An account is in it when its {account_industry}
      is Enterprise SaaS or Software and its {account_employee_count} is more than {tier1_employee_min}.
  - id: s2
    builds: segment
    uses:
    - account_industry
    - account_employee_count
    - tier1_fin_employee_min
    instruction: Build a new segment of accounts named "ABM Tier 1 Financial Services". An account is in it when its {account_industry}
      is Banking, Financial Services or Insurance and its {account_employee_count} is more than {tier1_fin_employee_min}.
  - id: s3
    builds: segment
    uses:
    - account_industry
    - account_employee_count
    - tier2_health_employee_min
    instruction: Build a new segment of accounts named "ABM Tier 2 Healthcare". An account is in it when its {account_industry}
      is Healthcare, Health Tech or Medical Devices and its {account_employee_count} is more than {tier2_health_employee_min}.
  - id: s4
    builds: personalization
    uses:
    - s1
    - s2
    - s3
    - primary_pages
    - demo_request_form_submitted
    - primary_cta_clicked
    dependsOn:
    - s1
    - s2
    - s3
    instruction: 'Create a website personalization named "ABM Account Personalization" on the pages {primary_pages}, any device,
      shown always, running continuously, with variants by audience and no random split. Default: all other visitors see the
      current hero unchanged. For visitors from accounts in the segment from "Find enterprise SaaS target accounts", replace
      the hero with a headline naming the visitor''s company, a line on running at enterprise scale and a Book a demo button.
      For the segment from "Find financial services target accounts", a headline naming the company, a line on security and
      compliance for banks and insurers, and a Book a demo button. For the segment from "Find healthcare target accounts",
      the same with healthcare copy and a line on patient-data protection. Measure {demo_request_form_submitted} and {primary_cta_clicked}
      per audience.'
---

# Named-account homepage hero

Slash command: /abm-account-personalization

## Step 1: Find enterprise SaaS target accounts

Build a new segment of accounts named "ABM Tier 1 Enterprise SaaS". An account is in it when its account industry is Enterprise SaaS or Software and its account employee count is more than 1000.

## Step 2: Find financial services target accounts

Build a new segment of accounts named "ABM Tier 1 Financial Services". An account is in it when its account industry is Banking, Financial Services or Insurance and its account employee count is more than 500.

## Step 3: Find healthcare target accounts

Build a new segment of accounts named "ABM Tier 2 Healthcare". An account is in it when its account industry is Healthcare, Health Tech or Medical Devices and its account employee count is more than 100.

## Step 4: Personalize the homepage hero by account

Create a website personalization named "ABM Account Personalization" on the pages /, /pricing, /demo, any device, shown always, running continuously, with variants by audience and no random split. Default: all other visitors see the current hero unchanged. For visitors from accounts in the segment from "Find enterprise SaaS target accounts", replace the hero with a headline naming the visitor's company, a line on running at enterprise scale and a Book a demo button. For the segment from "Find financial services target accounts", a headline naming the company, a line on security and compliance for banks and insurers, and a Book a demo button. For the segment from "Find healthcare target accounts", the same with healthcare copy and a line on patient-data protection. Measure demo request form submitted and primary cta clicked per audience.
