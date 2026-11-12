---
frontmatter_id: pricing-page-intent-to-sdr-outreach
slash_command: /pricing-page-intent-to-sdr-outreach
description: Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts it on an SDR with the visit context attached.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags repeat pricing page visitors, or visitors who pricing-viewed after real product use, as buying signals and
    hands each to a sales rep with visit context attached.
  parameters:
  - name: repeat_visit_count
    type: number
    label: Minimum pricing page views to count as repeat intent
    default: 2
    required: false
  - name: repeat_window
    type: duration
    label: Window for counting repeat pricing page views
    default: 14 d
    required: false
  - name: min_session_time
    type: duration
    label: Minimum total product session time before a single pricing view qualifies
    default: 5 min
    required: false
  - name: segment_lookback
    type: duration
    label: Lookback window for the intent segment
    default: 7 d
    required: false
  - name: task_tag
    type: string
    label: Tag applied to the SDR task
    default: 'high-intent: pricing'
    required: false
  - name: dashboard_comparison_multiple
    type: string
    label: Expected conversion lift of pricing intent over cold outbound
    default: 3-5x
    required: false
  requirements:
  - slot: pricing_page_viewed
    kind: event
    meaning: A visitor viewed the pricing page of the product
    properties:
    - name: user_id
      type: string
      meaning: Identifier of the visitor, present only when identified
      optional: false
    - name: page
      type: string
      meaning: Page path or name viewed before pricing in the session
      optional: true
  - slot: existing_paying_customer
    kind: segment
    meaning: Accounts or users who are already paying customers
  - slot: open_deal
    kind: segment
    meaning: Users linked to an account with an open sales deal
  - slot: product_session
    kind: event
    meaning: A user session in the product, with duration and features used
    properties:
    - name: duration
      type: duration
      meaning: Total session time
      optional: false
    - name: feature_used
      type: string
      meaning: Key product feature used during the session
      optional: true
  - slot: account_icp_tier
    kind: attribute
    meaning: The ideal customer profile tier of the user's account
    optional: true
  - slot: sdr_rep_territory
    kind: attribute
    meaning: The sales rep assigned to the account's territory
  - slot: sales_crm
    kind: integration
    meaning: Connected CRM where SDR tasks and deals are created
    channel: hubspot
  - slot: sales_slack
    kind: integration
    meaning: Connected Slack workspace used to notify reps
    channel: slack
  - slot: account_enrichment
    kind: integration
    meaning: Connected service that enriches a user's account data
    optional: true
    channel: email
  - slot: identification_prompt
    kind: destination
    meaning: In-app channel for asking an anonymous visitor for their email
    optional: true
    channel: email
  - slot: demo_scheduled
    kind: event
    meaning: A prospect scheduled a sales demo
  - slot: deal_created
    kind: event
    meaning: A sales deal was created
  - slot: cold_outbound_deals
    kind: segment
    meaning: Deals sourced from cold outbound prospecting
  steps:
  - id: s1
    builds: segment
    uses:
    - pricing_page_viewed
    - product_session
    - existing_paying_customer
    - open_deal
    - repeat_visit_count
    - repeat_window
    - min_session_time
    - segment_lookback
    instruction: Build a segment named 'Pricing-page intent - {segment_lookback}' of identified users who have either {repeat_visit_count}+
      {pricing_page_viewed} events in the last {repeat_window}, OR one {pricing_page_viewed} event after at least {min_session_time}
      of total {product_session.duration} in product sessions. Exclude users in {existing_paying_customer} and users in {open_deal}.
      The repeat-visit and dwell-time qualifiers filter out casual one-click visits.
  - id: s2
    builds: automation
    uses:
    - s1
    - sales_crm
    - sales_slack
    - account_enrichment
    - identification_prompt
    - sdr_rep_territory
    - account_icp_tier
    - task_tag
    instruction: 'Create a workflow triggered by {pricing_page_viewed} when the user is identified. Step 1: check whether
      the visit qualifies using the result of "Filter out the casual visits". Step 2: enrich the user''s account with {account_enrichment}
      if not already done. Step 3: compute a context blob with visit count, pages viewed before {pricing_page_viewed.page},
      key features from {product_session.feature_used} in session, and {account_icp_tier}. Step 4: create an SDR task in {sales_crm}
      tagged ''{task_tag}'' with the context, assigned by {sdr_rep_territory}. Step 5: post a Slack notification to the assigned
      rep in {sales_slack}. If the visitor is anonymous (not identified), start the identification journey instead by requesting
      their email through {identification_prompt}.'
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - demo_scheduled
    - deal_created
    - cold_outbound_deals
    - dashboard_comparison_multiple
    instruction: Build a pricing-intent dashboard showing weekly volume of signals from "Filter out the casual visits", median
      minutes from signal to first SDR touch from "Send the visit to a rep", conversion rate from pricing-intent signal to
      {demo_scheduled}, and conversion rate from pricing-intent signal to {deal_created}. Add a comparison against {cold_outbound_deals},
      where pricing-intent leads are expected to convert {dashboard_comparison_multiple} better.
---

# Pricing page intent to outreach

Slash command: /pricing-page-intent-to-sdr-outreach

## Step 1: Filter out the casual visits

Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits.

## Step 2: Send the visit to a rep

Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user's account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged 'high-intent: pricing' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt). Use the result of "Filter out the casual visits".

## Step 3: Compare against cold sourcing

Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to Deal created. Compare against baseline (deals sourced from cold outbound): pricing-intent leads should convert 3-5x better. Use the result of "Filter out the casual visits", "Send the visit to a rep".
