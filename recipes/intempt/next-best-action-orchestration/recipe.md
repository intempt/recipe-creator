---
frontmatter_id: next-best-action-orchestration
slash_command: /next-best-action-orchestration
description: This recipe gives each user a daily-refreshed recommendation for what to do next, such as teach, nurture, offer, spotlight a feature or hand off to a person, and then delivers it through email, in-app messages and an adaptive journey. It is built for lifecycle and growth marketers who want to replace fixed-cadence campaigns with behavior-driven ones.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Next best action orchestration

## Step 1: Decide the next step per user

Create an AI-derived attribute "next_best_action" on the User object, refreshed daily and on every significant behavioral event. Inputs: current lifecycle stage, engagement velocity, feature usage breadth, recent intent signals such as a pricing-page visit or a first use of a feature, and prior message engagement. Output: a structured object with a recommended_action, one of educate, nurture, offer, surface-feature, surface-recommendations, handoff-to-agent or wait; a recommended_channel, one of email, SMS, in-app, push or internal Slack; a recommended_content_theme; and a confidence score from 0 to 100.

## Step 2: Only route confident calls

Build a segment of users named "NBA-orchestrated users". A user is in the segment only when both of these are true: they did the Session start event in the last 14 days; their next_best_action.confidence is 50 or more. Refresh continuously as next_best_action changes. Use the result of "Decide the next step per user".

## Step 3: Write an email per action

Generate email content variants for the users in "NBA-orchestrated users", one per recommended_action. Educate variant: a short value tip matched to the user's lifecycle stage. Nurture variant: a case study or customer story relevant to the user's segment. Offer variant: a personalized incentive, matched to the user's plan and tenure, chosen from the account's active discount, trial-extension or credit offers. Surface-feature variant: a spotlight on the recommended feature with a deep link to it in the product. Each variant pulls its content from the user's current profile and lifecycle stage, not just their first name. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 4: Write the in-app versions

This step builds a page.
Generate in-app message variants for the surface-feature and surface-recommendations branches. For surface-feature: a contextual tooltip pointing to the feature, with a one-line value statement and a try-it action, rendered at the feature's location in the product. For surface-recommendations: a recommendation card drawn from the user's product affinity. Show these only during active sessions, never outside the app. Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action".

## Step 5: Build the recommendation set

This step builds a page.
Configure an in-app sidebar card named "NBA-driven recommendations" that renders when a user's next_best_action.recommended_action is surface-recommendations. Source the recommendations from the user's prior interaction history, usage patterns of similar users, and what is currently trending in the user's segment. Refresh weekly. Use the result of "Decide the next step per user", "Only route confident calls".

## Step 6: Re-read the signal at each gate

Build an adaptive journey wired to the "NBA-orchestrated users" segment, with gates at 7, 14, 30 and 60 days after signup and then weekly. At each gate, read the user's current next_best_action and route accordingly: educate or nurture to the matching email variant from "Write an email per action"; offer to the offer-variant email; surface-feature to the in-app tooltip from "Write the in-app versions" plus the matching email; surface-recommendations to the recommendation surface from "Build the recommendation set" plus a digest email; handoff-to-agent to an agent conversation; and wait to skip the touch and re-check at the next gate. Feed each branch's outcome, meaning clicked, engaged, converted or ignored, back into the next day's next_best_action computation. Exit the journey on a conversion event appropriate to the user's lifecycle stage, on unsubscribe, or when next_best_action returns wait for 3 consecutive gates, which suppresses further touches. Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in-app versions", "Build the recommendation set".

## Step 7: Check the model against a control

Compose an orchestration dashboard showing: the distribution of recommended_action across users, as a balance check on the model; the engagement rate per branch; the correlation between confidence and conversion, as a model-quality check; the conversion-rate lift of orchestrated users against a fixed-cadence holdout group of the same size; and the orchestration quality broken down by segment, to inform where the model needs retraining. Use the result of "Decide the next step per user", "Only route confident calls", "Write an email per action", "Write the in-app versions", "Build the recommendation set", "Re-read the signal at each gate".
