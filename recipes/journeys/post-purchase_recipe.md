---
name: post-purchase
description: |
  Use when a user mentions "post-purchase nurture", or asks for related help. Thank-you, review request, brand education, and cross-sell for first-time buyers.
arguments: []
intempt:
  id: post-purchase
  title: "Post purchase follow up"
  version: 1.0.0
  slashCommand: /post-purchase
  group: Journeys
  shortDescription: "Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what goes with it."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [post-purchase]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_recommendation
    - create_experiment
    - create_dashboard
  procedure:
    - step: 1
      title: "Split first time from repeat"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "People who placed an order in the last 14 days, separated into first time and repeat buyers."
      prompt: "Identify users with order_placed event in last 14 days, segmented by first-time vs repeat buyer."
    - step: 2
      title: "Write the five emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "A thank you, care and use information for the product, a review request, cross sell suggestions, and an introduction to the loyalty programme."
      prompt: "Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions."
    - step: 3
      title: "Send over the first month"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Confirmation straight away, care information on day 3, the review request on day 7, cross sell on day 14, and loyalty on day 30."
      prompt: "Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro)."
    - step: 4
      title: "Pick what goes with it"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Cross sell recommendations built from what they bought and their profile."
      prompt: "Generate cross-sell recommendations based on the purchased items and the customer's profile."
    - step: 5
      title: "Test when to ask for a review"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "A/B variants sending the review request at 3, 7 or 14 days."
      prompt: "Add A/B variants on review-request timing (3day vs 7day vs 14day)."
    - step: 6
      title: "Track reviews and repeat orders"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "How many reviews come in, how many people buy a second time, and the lift in order value from cross sell."
      prompt: "Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Post purchase follow up

Thanks the buyer, shows them how to use what they bought, asks for a review, and suggests what goes with it.

## What it does

1. **Split first time from repeat** (`create_segment`)

   People who placed an order in the last 14 days, separated into first time and repeat buyers.

2. **Write the five emails** (`create_email_content`)

   A thank you, care and use information for the product, a review request, cross sell suggestions, and an introduction to the loyalty programme.

3. **Send over the first month** (`create_journey`)

   Confirmation straight away, care information on day 3, the review request on day 7, cross sell on day 14, and loyalty on day 30.

4. **Pick what goes with it** (`create_recommendation`)

   Cross sell recommendations built from what they bought and their profile.

5. **Test when to ask for a review** (`create_experiment`)

   A/B variants sending the review request at 3, 7 or 14 days.

6. **Track reviews and repeat orders** (`create_dashboard`)

   How many reviews come in, how many people buy a second time, and the lift in order value from cross sell.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
