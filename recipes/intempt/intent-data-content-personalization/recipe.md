---
frontmatter_id: intent-data-content-personalization
slash_command: /intent-data-content-personalization
description: Visitors who have been reading pricing, security, integrations or case-study pages see matching content blocks
  on the homepage and key landing pages, with generic content for everyone else.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Visitors who have been reading pricing, security, integrations or case-study pages see matching content blocks
    on the homepage and key landing pages, with generic content for everyone else.
  parameters:
  - name: pricing_window
    type: duration
    label: Pricing page lookback
    default: 7 d
    required: false
  - name: pricing_min_views
    type: number
    label: Pricing page views needed
    default: 2
    required: false
  - name: security_window
    type: duration
    label: Security page lookback
    default: 14 d
    required: false
  - name: security_min_views
    type: number
    label: Security page views needed
    default: 1
    required: false
  - name: integrations_window
    type: duration
    label: Integrations page lookback
    default: 7 d
    required: false
  - name: integrations_min_views
    type: number
    label: Integrations page views needed
    default: 2
    required: false
  - name: case_study_window
    type: duration
    label: Case study page lookback
    default: 14 d
    required: false
  - name: case_study_min_views
    type: number
    label: Case study page views needed
    default: 2
    required: false
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A visitor viewed a page on the website
    properties:
    - name: page_url
      type: string
      meaning: URL of the viewed page
      optional: false
  - slot: demo_request_form_event
    kind: event
    meaning: A visitor submitted a demo-request or contact form
  steps:
  - id: s1
    builds: personalization
    uses:
    - page_view_event
    - demo_request_form_event
    - pricing_window
    - pricing_min_views
    - security_window
    - security_min_views
    - integrations_window
    - integrations_min_views
    - case_study_window
    - case_study_min_views
    instruction: 'Create a client-side personalization named "Intent-Data Content Personalization" that replaces the featured
      content block on the homepage and key landing pages, all devices, always, continuously. Check variants in this order.
      Pricing: visitors with {page_view_event} where {page_view_event.page_url} contains /pricing at least {pricing_min_views}
      times in the last {pricing_window}; show an ROI calculator and plan comparison. Security: {page_view_event.page_url}
      containing /security or /compliance at least {security_min_views} time in the last {security_window}; show a security
      case study and compliance content. Integrations: {page_view_event.page_url} containing /integrations at least {integrations_min_views}
      times in the last {integrations_window}; show the integration directory and integration case studies. Case studies:
      {page_view_event.page_url} containing /case-studies or /customers at least {case_study_min_views} times in the last
      {case_study_window}; show more case studies and customer logos. Control: the current content for everyone else. Track
      content block clicks and {demo_request_form_event} per variant.'
---

# Content blocks by browsing behavior

Slash command: /intent-data-content-personalization

## Step 1: Set up the behavior variants

Create a client-side personalization named "Intent-Data Content Personalization" that replaces the featured content block on the homepage and key landing pages, all devices, always, continuously. Check variants in this order. Pricing: visitors with page view event where page url contains /pricing at least 2 times in the last 7 d; show an ROI calculator and plan comparison. Security: page url containing /security or /compliance at least 1 time in the last 14 d; show a security case study and compliance content. Integrations: page url containing /integrations at least 2 times in the last 7 d; show the integration directory and integration case studies. Case studies: page url containing /case-studies or /customers at least 2 times in the last 14 d; show more case studies and customer logos. Control: the current content for everyone else. Track content block clicks and demo request form event per variant.
