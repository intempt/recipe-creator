---
name: Personalization Recs
description: Catalog-aware recommendations across web, email, and app surfaces.
intempt:
  id: personalization-recs
  version: 1.0.0
  slashCommand: /personalization-recs
  shortDescription: Catalog-aware recommendations across web, email, and app surfaces.
  author:
    type: intempt
    name: Intempt
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
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: recommendation
    type: recommendation
    description: Recommendation produced by this recipe.
  - name: personalization
    type: personalization
    description: Personalization produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-recs-engine
    describe: Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity
      models.
    produces: recommendation
  - id: build-personalization
    describe: Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces.
    produces: personalization
  - id: build-experiment
    describe: Add A/B variants comparing personalized recs vs trending products vs editor's-pick.
    produces: experiment
  - id: build-content
    describe: Generate email modules that surface recommendations within campaign and journey emails.
    produces: content
  - id: build-recs-journey
    describe: Build a journey delivering personalized product picks to high-intent browsers.
    produces: journey
  - id: build-dashboard
    describe: Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance.
    produces: dashboard
---

# Personalization Recs

Catalog-aware recommendations across web, email, and app surfaces.

## Outputs

- **recommendation** (recommendation): Recommendation produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Configure recommendation engine sourcing from product catalog with collaborative-filtering and item-similarity models.
2. Configure personalization rules serving recommendations on PDP, cart, post-purchase, and email surfaces.
3. Add A/B variants comparing personalized recs vs trending products vs editor's-pick.
4. Generate email modules that surface recommendations within campaign and journey emails.
5. Build a journey delivering personalized product picks to high-intent browsers.
6. Compose a dashboard tracking recommendation CTR, attributed revenue, and per-surface performance.
