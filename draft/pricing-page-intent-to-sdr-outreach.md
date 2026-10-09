---
description: Treats a repeat pricing page visit, or one after real product use, as a buying signal and puts it on an SDR with the visit context attached.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
---

# Pricing page intent to outreach

Slash command: /pricing-page-intent-to-sdr-outreach

## Step 1: Filter out the casual visits

Build a segment 'Pricing-page intent - last 7 days' capturing identified users with 2+ pricing_page_viewed events in the last 14 days, OR a single pricing_page_viewed event after at least 5 minutes of total product session time. Excludes existing paid customers and users with an open deal already. The repeat-visit and dwell-time qualifiers filter out casual one-click visits.

## Step 2: Send the visit to a rep

Create a workflow firing on pricing_page_viewed when the user is identified. Step sequence: (1) check whether this is a qualifying visit per segment criteria; (2) enrich the user's account if not done already; (3) compute a context blob: visit count, pages viewed prior to pricing, key features used in session, account ICP tier; (4) create a SDR task tagged 'high-intent: pricing' with the context, assigned by territory; (5) post Slack notification to the rep. If the account is unidentified (anonymous visitor), trigger the identification journey instead (request email via in-app prompt). Use the result of "Filter out the casual visits".

## Step 3: Compare against cold sourcing

Compose a pricing-intent dashboard: pricing-page intent signal volume per week, SDR response time (median minutes from signal to first touch), conversion rate from pricing-intent signal to demo-scheduled, conversion rate from pricing-intent to Deal created. Compare against baseline (deals sourced from cold outbound): pricing-intent leads should convert 3-5x better. Use the result of "Filter out the casual visits", "Send the visit to a rep".
