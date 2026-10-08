---
description: Generates catalog-aware product recommendations tailored to user cohorts and evaluates their performance with A/B experiments.
author:
  first_name: V
  last_name: Ranadheer
  job_title: Design Engineer
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - ecommerce
---

# Product recommendations across channels

Slash command: /personalization-recs

## Step 1: Build the recommendation model

Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models.

## Step 2: Place them on each surface

Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces. Use the result of "Build the recommendation model".

## Step 3: Split shoppers into cohorts

Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies. Use the result of "Build the recommendation model", "Place them on each surface".

## Step 4: Test against the alternatives

Add A/B variants comparing personalized recs vs trending products vs editor's-pick. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts".

## Step 5: Build the email modules

Generate email modules that surface recommendations within campaign and journey emails. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives".

## Step 6: Follow up with high-intent browsers

Build a journey delivering personalized product picks to high-intent browsers. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives", "Build the email modules".

## Step 7: Track what recommendations earn

Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance. Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test against the alternatives", "Build the email modules", "Follow up with high-intent browsers".
