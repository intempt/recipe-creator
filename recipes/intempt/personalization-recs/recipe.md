---
id: personalization-recs
title: Product recommendations across channels
slash_command: /personalization-recs
group: Recommendations
owner: intempt
summary: Puts product recommendations on your product pages, cart, post-purchase screens and emails, tuned
  to how the shopper behaves, and measures what they earn.
description: >-
  Catalog-aware recommendations across web, email, and app surfaces.
version: 2.0.0
classification:
  product:
    - marketing
    - sales
  agent: experience-optimizer
  mode:
    - ecommerce
  complexity: advanced
  executionMode: live
  tags:
    - personalization-recs
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new product recommendation, from step 1 "Build the recommendation model"
    - A new website personalization, from step 2 "Place them on each surface"
    - A new segment, from step 3 "Split shoppers into cohorts"
    - A new A/B experiment, from step 4 "Test against the alternatives"
    - A new designed email, from step 5 "Build the email modules"
    - A new journey, from step 6 "Follow up with high-intent browsers"
    - A new dashboard, from step 7 "Track what recommendations earn"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Build the recommendation model
    summary: >-
      Recommendations drawn from your product catalog using shopper-similarity and item-similarity models.
    builds: recommendation
    description: >-
      Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity
      models.
  - id: s2
    title: Place them on each surface
    summary: >-
      Rules for what shows on product pages, in the cart, after purchase, and in email.
    builds: personalization
    description: >-
      Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces.
      Use the result of "Build the recommendation model".
    dependsOn:
      - s1
  - id: s3
    title: Split shoppers into cohorts
    summary: >-
      New visitor, browsing, returning and lapsed cohorts, each getting a differently tuned set of picks.
    builds: segment
    description: >-
      Segment users into recommendation cohorts (new visitor, browsing, returning, lapsed) for tuned strategies.
      Use the result of "Build the recommendation model", "Place them on each surface".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Test against the alternatives
    summary: >-
      A/B variants comparing personalized picks against trending products and an editor's pick.
    builds: experiment
    description: >-
      Add A/B variants comparing personalized recs vs trending products vs editor's-pick. Use the result
      of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Build the email modules
    summary: >-
      Recommendation blocks that drop into campaign and journey emails.
    builds: email_html
    description: >-
      Generate email modules that surface recommendations within campaign and journey emails. Use the
      result of "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts",
      "Test against the alternatives".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Follow up with high-intent browsers
    summary: >-
      A journey that sends personalized product picks to shoppers showing strong buying intent.
    builds: journey
    description: >-
      Build a journey delivering personalized product picks to high-intent browsers. Use the result of
      "Build the recommendation model", "Place them on each surface", "Split shoppers into cohorts", "Test
      against the alternatives", "Build the email modules".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: Track what recommendations earn
    summary: >-
      Click-through rate, revenue attributed to recommendations, and how each surface performs.
    builds: dashboard
    description: >-
      Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance.
      Use the result of "Build the recommendation model", "Place them on each surface", "Split shoppers
      into cohorts", "Test against the alternatives", "Build the email modules", "Follow up with high-intent
      browsers".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
outputs:
  - key: recommendation
    producedByStep: s1
    type: recommendation
    description: Recommendation produced by this recipe.
  - key: personalization
    producedByStep: s2
    type: personalization
    description: Personalization produced by this recipe.
  - key: segment
    producedByStep: s3
    type: segment
    description: Segment produced by this recipe.
  - key: experiment
    producedByStep: s4
    type: experiment
    description: Experiment produced by this recipe.
  - key: asset
    producedByStep: s5
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Product recommendations across channels

Puts product recommendations on your product pages, cart, post-purchase screens and emails, tuned to how the shopper behaves, and measures what they earn.

## Steps

1. **Build the recommendation model** (builds recommendation)

   Recommendations drawn from your product catalog using shopper-similarity and item-similarity models.

2. **Place them on each surface** (builds personalization)

   Rules for what shows on product pages, in the cart, after purchase, and in email.

3. **Split shoppers into cohorts** (builds segment)

   New visitor, browsing, returning and lapsed cohorts, each getting a differently tuned set of picks.

4. **Test against the alternatives** (builds experiment)

   A/B variants comparing personalized picks against trending products and an editor's pick.

5. **Build the email modules** (builds email_html)

   Recommendation blocks that drop into campaign and journey emails.

6. **Follow up with high-intent browsers** (builds journey)

   A journey that sends personalized product picks to shoppers showing strong buying intent.

7. **Track what recommendations earn** (builds dashboard)

   Click-through rate, revenue attributed to recommendations, and how each surface performs.

## What you end up with

- **recommendation** (recommendation): Recommendation produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new product recommendation, from step 1 "Build the recommendation model"
- A new website personalization, from step 2 "Place them on each surface"
- A new segment, from step 3 "Split shoppers into cohorts"
- A new A/B experiment, from step 4 "Test against the alternatives"
- A new designed email, from step 5 "Build the email modules"
- A new journey, from step 6 "Follow up with high-intent browsers"
- A new dashboard, from step 7 "Track what recommendations earn"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey, personalization, recommendation.
