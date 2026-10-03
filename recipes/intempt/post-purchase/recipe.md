---
id: post-purchase
title: Post purchase follow up
slash_command: /post-purchase
group: Journeys
owner: intempt
summary: Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what
  goes with it.
description: >-
  Thank-you, review request, brand education, and cross-sell for first-time buyers.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - ecommerce
  complexity: advanced
  executionMode: live
  tags:
    - post-purchase
steps:
  - id: s1
    title: Split first time from repeat
    summary: >-
      People who placed an order in the last 14 days, separated into first time and repeat buyers.
    builds: segment
    description: >-
      Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer.
  - id: s2
    title: Write the five emails
    summary: >-
      A thank you, care and use information for the product, a review request, cross sell suggestions,
      and an introduction to the loyalty programme.
    builds: email_html
    description: >-
      Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell
      suggestions. Use the result of "Split first time from repeat".
    dependsOn:
      - s1
  - id: s3
    title: Send over the first month
    summary: >-
      Confirmation straight away, care information on day 3, the review request on day 7, cross sell on
      day 14, and loyalty on day 30.
    builds: journey
    description: >-
      Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day
      (cross-sell), 30day (loyalty intro). Use the result of "Split first time from repeat", "Write the
      five emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Pick what goes with it
    summary: >-
      Cross sell recommendations built from what they bought and their profile.
    builds: recommendation
    description: >-
      Generate cross-sell recommendations based on the purchased items and the customer's profile. Use
      the result of "Split first time from repeat", "Write the five emails", "Send over the first month".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Test when to ask for a review
    summary: >-
      A/B variants sending the review request at 3, 7 or 14 days.
    builds: experiment
    description: >-
      Add A/B variants on review-request timing (3day vs 7day vs 14day). Use the result of "Split first
      time from repeat", "Write the five emails", "Send over the first month", "Pick what goes with it".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Track reviews and repeat orders
    summary: >-
      How many reviews come in, how many people buy a second time, and the lift in order value from cross
      sell.
    builds: dashboard
    description: >-
      Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell.
      Use the result of "Split first time from repeat", "Write the five emails", "Send over the first
      month", "Pick what goes with it", "Test when to ask for a review".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: recommendation
    producedByStep: s4
    type: recommendation
    description: Recommendation produced by this recipe.
  - key: experiment
    producedByStep: s5
    type: experiment
    description: Experiment produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Post purchase follow up

Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what goes with it.

## Steps

1. **Split first time from repeat** (builds segment)

   People who placed an order in the last 14 days, separated into first time and repeat buyers.

2. **Write the five emails** (builds email_html)

   A thank you, care and use information for the product, a review request, cross sell suggestions, and an introduction to the loyalty programme.

3. **Send over the first month** (builds journey)

   Confirmation straight away, care information on day 3, the review request on day 7, cross sell on day 14, and loyalty on day 30.

4. **Pick what goes with it** (builds recommendation)

   Cross sell recommendations built from what they bought and their profile.

5. **Test when to ask for a review** (builds experiment)

   A/B variants sending the review request at 3, 7 or 14 days.

6. **Track reviews and repeat orders** (builds dashboard)

   How many reviews come in, how many people buy a second time, and the lift in order value from cross sell.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, journey, recommendation.
