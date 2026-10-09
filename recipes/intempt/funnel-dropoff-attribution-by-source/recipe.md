---
description: Runs the same acquisition to retention funnel separately for each traffic source, so you can see which channels bring people who actually stick.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - finance
  - media
---

# Funnel drop off by source

Slash command: /funnel-dropoff-attribution-by-source

## Step 1: Run one funnel per source

Create a Funnel report called "Funnel Drop-off by Acquisition Source".
This is a configurable funnel: the user specifies which canonical events make up the funnel. Defaults if unspecified:
1. Event "User created": "Acquired"
2. Event "Completed a journey goal" (configurable journey_id): "Activated"
3. Event "Subscription started" (saas) OR "Placed order" (ecommerce): "Converted"
4. Event "Session start" with date 30+ days after the conversion event: "Retained 30 days"
Conversion window: 60 days
Breakdown: By Users.UTM source (top 8 sources by Step 1 volume)
Compare: Previous period (prior 60 days)
Render as small-multiples: one funnel per source, sorted by end-to-end conversion rate descending.
Also include a summary table:
- Source · Volume at Step 1 · End-to-end conversion % · Volume at final step · Per-source revenue (sum of Subscription started.amount or Placed order.total_price for users who reached Step 3+)
Annotations:
- Flag the source with highest end-to-end conversion AND volume above the 33rd percentile.
- Flag any source where Step 1 to 2 conversion is below 50% of the average across sources (lead-quality issue).
- Flag any source where Step 3 to 4 conversion is below average (conversion fine but customers don't retain).
- Highlight the largest gap between sources at any single step.
Surface the actual revenue-weighted ROI per source.
Taxonomy notes:
- All steps reference canonical events. Users.UTM source is a real first-touch attribution attribute.
- Note: this recipe does NOT compute CAC because ad-spend is not in the canonical taxonomy. Per-source revenue is the closest proxy.
