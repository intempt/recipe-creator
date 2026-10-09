---
name: browse-abandonment
description: |
  Use when a user mentions "browse abandonment", or asks for related help. Re-engage users who browsed products without adding to cart: earlier-funnel than cart abandonment.
arguments: []
intempt:
  id: browse-abandonment
  title: "Browse abandonment follow up"
  version: 1.0.0
  slashCommand: /browse-abandonment
  group: Journeys
  shortDescription: "Reminds people who looked at products but never added anything to the cart, showing the items they viewed and a few they might prefer."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [ecommerce]
    complexity: advanced
    executionMode: live
    tags: [browse-abandonment]
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
    - build_funnel_report
  procedure:
    - step: 1
      title: "Find people who only browsed"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who viewed a product in the last 7 days and never added one to their cart."
      prompt: "Identify users who viewed a product in the last 7 days but did not add one to their cart."
    - step: 2
      title: "Write the browse reminder"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [segment]
      description: "An email showing the products they looked at alongside similar items."
      prompt: "Generate browse-recovery email content highlighting the viewed products and similar items."
    - step: 3
      title: "Send at 24 and 72 hours"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn: [segment, asset]
      description: "Two emails, the first a day after the browse and the second three days after."
      prompt: "Build a 2-touch journey sending product reminder emails at 24hr and 72hr after browse."
    - step: 4
      title: "Pick items for each shopper"
      command: create_recommendation
      produces: recommendation
      bindsAs: recommendation
      dependsOn: [segment, asset, journey]
      description: "Recommendations built from what each person viewed and what they have bought before."
      prompt: "Generate product recommendations for each browser based on their viewed items and purchase history."
    - step: 5
      title: "Test picks against best sellers"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [segment, asset, journey, recommendation]
      description: "An A/B test comparing personalised recommendations with trending products."
      prompt: "Add A/B variants comparing personalized recommendations vs trending products."
    - step: 6
      title: "Follow browse through to sale"
      command: build_funnel_report
      produces: report
      bindsAs: report
      dependsOn: [segment, asset, journey, recommendation, experiment]
      description: "A funnel from browse to email open, click, add to cart and purchase."
      prompt: "Compose a funnel report tracking browse to email-open to email-click to cart-add to purchase."
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Browse abandonment follow up

Reminds people who looked at products but never added anything to the cart, showing the items they viewed and a few they might prefer.

## What it does

1. **Find people who only browsed** (`create_segment`)

   Anyone who viewed a product in the last 7 days and never added one to their cart.

2. **Write the browse reminder** (`create_email_content`)

   An email showing the products they looked at alongside similar items.

3. **Send at 24 and 72 hours** (`create_journey`)

   Two emails, the first a day after the browse and the second three days after.

4. **Pick items for each shopper** (`create_recommendation`)

   Recommendations built from what each person viewed and what they have bought before.

5. **Test picks against best sellers** (`create_experiment`)

   An A/B test comparing personalised recommendations with trending products.

6. **Follow browse through to sale** (`build_funnel_report`)

   A funnel from browse to email open, click, add to cart and purchase.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **report** (report): Report produced by this recipe.
