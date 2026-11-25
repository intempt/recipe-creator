---
frontmatter_id: pricing-page-intent-to-sdr-outreach
slash_command: /pricing-page-intent-to-sdr-outreach
description: Treats a repeat pricing page visit, or one after real product use, as a buying signal and emails an SDR the visit
  context, with a weekly digest of what the signals turn into.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags repeat pricing page visitors, or visitors who viewed pricing after real product use, and emails a sales rep
    each one with the visit context, plus a weekly digest.
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
  - name: alert_recipients
    type: string
    label: Email addresses of the SDRs who get the buying signals
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  - slot: demo_scheduled
    kind: event
    meaning: A prospect scheduled a sales demo
  - slot: deal_created
    kind: event
    meaning: A sales deal was created
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
    instruction: Build a new segment of users named "Pricing Page Intent". A user is in it when they are identified and either
      they did {pricing_page_viewed} {repeat_visit_count} or more times in the last {repeat_window}, or they did {pricing_page_viewed}
      at least once in the last {repeat_window} after a total {product_session.duration} of {min_session_time} or more. Users
      in {existing_paying_customer} or in {open_deal} are left out.
  - id: s2
    builds: automation
    uses:
    - s1
    - pricing_page_viewed
    - product_session
    - account_icp_tier
    - repeat_window
    - alert_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation triggered when a user enters the segment from "Filter out the casual visits". An analysis
      step writes: how many times they did {pricing_page_viewed} in the last {repeat_window}; the {pricing_page_viewed.page}
      values they viewed before pricing; their top {product_session.feature_used} values; their {account_icp_tier}. Then it
      emails {alert_recipients} the user''s name, email and this context, marked high intent: pricing.'
  - id: s3
    builds: automation
    uses:
    - s1
    - demo_scheduled
    - deal_created
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered
      the segment from "Filter out the casual visits" and writes these figures: the count in the last 7 days and in each of
      the 4 weeks before; of users who entered in the last 60 days, the share who did {demo_scheduled} within 14 days of entering,
      and the share who did {deal_created} within 30 days. Then it emails these figures as plain-text lines, each with its
      window, to {digest_recipients}. Nothing else is sent.'
---

# Pricing page intent to outreach

Slash command: /pricing-page-intent-to-sdr-outreach

## Step 1: Filter out the casual visits

Build a new segment of users named "Pricing Page Intent". A user is in it when they are identified and either they did pricing page viewed 2 or more times in the last 14 d, or they did pricing page viewed at least once in the last 14 d after a total duration of 5 min or more. Users in existing paying customer or in open deal are left out.

## Step 2: Send the visit to a rep

Build an automation triggered when a user enters the segment from "Filter out the casual visits". An analysis step writes: how many times they did pricing page viewed in the last 14 d; the page values they viewed before pricing; their top feature used values; their account icp tier. Then it emails the email addresses of the SDRs who get the buying signals the user's name, email and this context, marked high intent: pricing.

## Step 3: Email the weekly pricing intent digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the users who entered the segment from "Filter out the casual visits" and writes these figures: the count in the last 7 days and in each of the 4 weeks before; of users who entered in the last 60 days, the share who did demo scheduled within 14 days of entering, and the share who did deal created within 30 days. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
