---
id: browse-abandonment
title: Browse abandonment follow up
slash_command: /browse-abandonment
group: Journeys
owner: intempt
summary: Reminds people who looked at products but never added anything to the cart, showing the items
  they viewed and a few they might prefer.
description: >-
  Re-engage users who browsed products without adding to cart: earlier-funnel than cart abandonment.
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
    - browse-abandonment
steps:
  - id: s1
    title: Find people who only browsed
    summary: >-
      Anyone who viewed a product in the last 7 days and never added one to their cart.
    builds: segment
    description: >-
      Identify users with product_viewed events in last 7 days who did NOT trigger cart_added.
  - id: s2
    title: Write the browse reminder
    summary: >-
      An email showing the products they looked at alongside similar items.
    builds: email_html
    description: >-
      Generate browse-recovery email content highlighting the viewed products and similar items. Use the
      result of "Find people who only browsed".
    dependsOn:
      - s1
  - id: s3
    title: Send at 24 and 72 hours
    summary: >-
      Two emails, the first a day after the browse and the second three days after.
    builds: journey
    description: >-
      Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse. Use the result
      of "Find people who only browsed", "Write the browse reminder".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Pick items for each shopper
    summary: >-
      Recommendations built from what each person viewed and what they have bought before.
    builds: recommendation
    description: >-
      Generate product recommendations for each browser based on their viewed items and purchase history.
      Use the result of "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72
      hours".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Test picks against best sellers
    summary: >-
      An A/B test comparing personalised recommendations with trending products.
    builds: experiment
    description: >-
      Add A/B variants comparing personalized recommendations vs trending products. Use the result of
      "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72 hours", "Pick items
      for each shopper".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Follow browse through to sale
    summary: >-
      A funnel from browse to email open, click, add to cart and purchase.
    builds: report
    description: >-
      Compose a funnel report tracking browse to email-open to email-click to cart-add to purchase. Use
      the result of "Find people who only browsed", "Write the browse reminder", "Send at 24 and 72 hours",
      "Pick items for each shopper", "Test picks against best sellers".
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
  - key: report
    producedByStep: s6
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Browse abandonment follow up

Reminds people who looked at products but never added anything to the cart, showing the items they viewed and a few they might prefer.

## Steps

1. **Find people who only browsed** (builds segment)

   Anyone who viewed a product in the last 7 days and never added one to their cart.

2. **Write the browse reminder** (builds email_html)

   An email showing the products they looked at alongside similar items.

3. **Send at 24 and 72 hours** (builds journey)

   Two emails, the first a day after the browse and the second three days after.

4. **Pick items for each shopper** (builds recommendation)

   Recommendations built from what each person viewed and what they have bought before.

5. **Test picks against best sellers** (builds experiment)

   An A/B test comparing personalised recommendations with trending products.

6. **Follow browse through to sale** (builds report)

   A funnel from browse to email open, click, add to cart and purchase.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **report** (report): Report produced by this recipe.

## Availability

Coming soon: waiting on the engine to build experiment, journey, recommendation, report.
