---
frontmatter_id: personalized-cta-copy-personalization
slash_command: /personalized-cta-copy-personalization
description: Shows visitors a main button whose wording matches their account stage (first-time, returning, trial, free plan,
  paying), replacing one generic prompt, and tracks clicks per audience.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows visitors a main button whose wording matches their account stage (first-time, returning, trial, free plan,
    paying), replacing one generic prompt, and tracks clicks per audience.
  parameters:
  - name: homepage_path
    type: string
    label: Homepage path
    default: /
    required: false
  - name: trial_app_path
    type: string
    label: Where trial users are sent
    default: /app
    required: false
  - name: free_plan_upgrade_path
    type: string
    label: Where free-plan users are sent
    default: /upgrade
    required: false
  - name: paying_dashboard_path
    type: string
    label: Where paying users are sent
    default: /dashboard
    required: false
  - name: cta_target_selector
    type: string
    label: CSS selector of the main button
    default: .primary-cta-button
    required: false
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A visitor started a website session
  - slot: user_created_event
    kind: event
    meaning: A customer created a user account
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Plan name, free for the free plan
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  steps:
  - id: s1
    builds: personalization
    uses:
    - session_start_event
    - user_created_event
    - subscription_started_event
    - subscription_canceled_event
    - homepage_path
    - trial_app_path
    - free_plan_upgrade_path
    - paying_dashboard_path
    - cta_target_selector
    instruction: 'Create a client-side personalization named "Personalized CTA Copy" that changes the text and link of the
      button {cta_target_selector} on {homepage_path} and the pricing and features pages, all devices, shown always, running
      continuously; the button keeps id primary-cta. Check account states in this order. Paying: users with {subscription_started_event}
      where {subscription_started_event.plan} is not free and no later {subscription_canceled_event}: "Open your account"
      to {paying_dashboard_path}. Free plan: users whose latest {subscription_started_event.plan} is free: "Upgrade to Pro"
      to {free_plan_upgrade_path}. Trial: users who did {user_created_event} and have no {subscription_started_event}: "Continue
      your trial" to {trial_app_path}. Returning visitor: visitors who did {session_start_event} before the current session
      and no {user_created_event}: "Continue exploring". First visit: visitors with no earlier {session_start_event}: "Start
      your free trial". Control "Get started" for anyone else. Track button clicks per variant, and per variant the users
      who then did {user_created_event} or {subscription_started_event}.'
---

# CTA wording by account state

Slash command: /personalized-cta-copy-personalization

## Step 1: Set up the five CTA variants

Create a client-side personalization named "Personalized CTA Copy" that changes the text and link of the button .primary-cta-button on / and the pricing and features pages, all devices, shown always, running continuously; the button keeps id primary-cta. Check account states in this order. Paying: users with subscription started event where plan is not free and no later subscription canceled event: "Open your account" to /dashboard. Free plan: users whose latest plan is free: "Upgrade to Pro" to /upgrade. Trial: users who did user created event and have no subscription started event: "Continue your trial" to /app. Returning visitor: visitors who did session start event before the current session and no user created event: "Continue exploring". First visit: visitors with no earlier session start event: "Start your free trial". Control "Get started" for anyone else. Track button clicks per variant, and per variant the users who then did user created event or subscription started event.
