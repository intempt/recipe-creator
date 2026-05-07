---
name: B2B Event Attendee Feedback Collection
description: Post-event NPS and qualitative feedback from attendees. Drives event ROI measurement and captures testimonials
  from happy attendees.
intempt:
  id: b2b-event-attendee-feedback-collection
  version: 1.0.0
  slashCommand: /b2b-event-attendee-feedback-collection
  shortDescription: Post-event NPS and qualitative feedback from attendees. Drives event ROI measurement and captures testimonials
    from happy attendees.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - marketing
    agent: journey-builder
    mode:
    - b2b
    complexity: advanced
    executionMode: live
    tags:
    - customer-success-and-renewal
    - b2b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: content
    type: content
    description: Content produced by this recipe.
  - name: journey
    type: journey
    description: Journey produced by this recipe.
  - name: recommendation
    type: recommendation
    description: Recommendation produced by this recipe.
  - name: experiment
    type: experiment
    description: Experiment produced by this recipe.
  - name: dashboard
    type: dashboard
    description: Dashboard produced by this recipe.
  steps:
  - id: build-content
    describe: 'Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions.
      (Tailored for: B2B event attendee feedback collection.)'
    produces: content
  - id: build-journey
    describe: 'Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell),
      30day (loyalty intro). (Tailored for: B2B event attendee feedback collection.)'
    produces: journey
  - id: build-recommendations
    describe: 'Generate cross-sell recommendations based on the purchased items and the customer''s profile. (Tailored for:
      B2B event attendee feedback collection.)'
    produces: recommendation
  - id: build-experiment
    describe: 'Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: B2B event attendee feedback
      collection.)'
    produces: experiment
  - id: build-dashboard
    describe: 'Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell.
      (Tailored for: B2B event attendee feedback collection.)'
    produces: dashboard
  prerequisites:
    integrations:
    - value: hubspot
      severity: blocking
---

# B2B Event Attendee Feedback Collection

Post-event NPS and qualitative feedback from attendees. Drives event ROI measurement and captures testimonials from happy attendees.

## Outputs

- **content** (content): Content produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **recommendation** (recommendation): Recommendation produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Steps

1. Generate post-purchase content: thank-you email, product-care info, review request, and cross-sell suggestions. (Tailored for: B2B event attendee feedback collection.)
2. Build a 5-touch journey sending content at 0hr (confirmation), 3day (care), 7day (review), 14day (cross-sell), 30day (loyalty intro). (Tailored for: B2B event attendee feedback collection.)
3. Generate cross-sell recommendations based on the purchased items and the customer's profile. (Tailored for: B2B event attendee feedback collection.)
4. Add A/B variants on review-request timing (3day vs 7day vs 14day). (Tailored for: B2B event attendee feedback collection.)
5. Compose a dashboard tracking review-collection rate, second-purchase rate, and AOV uplift from cross-sell. (Tailored for: B2B event attendee feedback collection.)

## Prerequisites

- Integration: **hubspot** (blocking)
