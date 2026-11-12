---
frontmatter_id: personalized-cta-copy-personalization
slash_command: /personalized-cta-copy-personalization
description: The main button reads differently for a first-time visitor, a returning one, someone mid-trial, a free-plan user and a paying customer, instead of one generic prompt.
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
    label: Page where the CTA appears (homepage, marketing pages, pricing, features)
    default: /
  - name: trial_app_path
    type: string
    label: Link target for trial users
    default: /app
  - name: free_plan_upgrade_path
    type: string
    label: Link target for free-plan users
    default: /upgrade
  - name: paying_dashboard_path
    type: string
    label: Link target for paying customers
    default: /dashboard
  - name: cta_target_selector
    type: string
    label: HTML selector of the primary CTA button
    default: .primary-cta-button
  requirements:
  - slot: first_seen_event
    kind: attribute
    meaning: A user's first-seen timestamp used to tell first-time visitors from returning ones
  - slot: user_created_event
    kind: event
    meaning: A customer created a user account
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: plan
      type: string
      meaning: Plan the customer subscribed to, such as free or a paid plan
      optional: false
    - name: billing_period
      type: string
      meaning: Billing period chosen for the subscription
      optional: true
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  - slot: primary_cta_element
    kind: destination
    meaning: The main call-to-action button on the website pages where the personalization runs
    channel: email
  - slot: web_personalization_tool
    kind: integration
    meaning: A web personalization tool able to swap page content per audience and track clicks
    channel: email
  steps:
  - id: s1
    builds: personalization
    uses:
    - first_seen_event
    - user_created_event
    - subscription_started_event
    - subscription_canceled_event
    - primary_cta_element
    - web_personalization_tool
    - homepage_path
    - trial_app_path
    - free_plan_upgrade_path
    - paying_dashboard_path
    - cta_target_selector
    instruction: Create a client-side personalization titled "Personalized CTA Copy" on the experiences page that replaces
      the primary CTA in {cta_target_selector} on {homepage_path} and marketing, pricing and features pages. Keep the generic
      control copy "Get started" as the fallback for all other visitors. Show "Start your free trial" to visitors whose {first_seen_event}
      is within the current session or is empty, and who have no {subscription_started_event}. Show "Continue exploring [Brand]"
      to returning visitors whose {first_seen_event} is older than the current session and who have no {user_created_event}.
      Show "Continue your trial" to users with a {user_created_event} and no {subscription_started_event} that has a {subscription_started_event.billing_period}
      value; send these users to {trial_app_path}. Show "Upgrade to Pro" to users with a {subscription_started_event} where
      {subscription_started_event.plan} is "free"; send these users to {free_plan_upgrade_path}. Show "Open dashboard" to
      users with a {subscription_started_event} where {subscription_started_event.plan} is not "free" and no {subscription_canceled_event};
      send these users to {paying_dashboard_path}. Each variant keeps the button id "primary-cta" and a shared click target
      so clicks aggregate across variants. Track clicks per CTA copy per audience and downstream signup, trial-to-paid and
      free-to-paid upgrade conversion per audience. Run continuously with targeting on every listed page and no display frequency
      cap. The copy can be refined in the visual editor, for example a first-person variant such as "Start MY free trial".
---

# CTA wording by account state

Slash command: /personalized-cta-copy-personalization

## Step 1: Set up the five CTA variants

Create a CLIENT PERSONALIZATION on /experiences titled "Personalized CTA Copy".
This personalization changes the primary CTA copy per audience segment. Each variant binds to a lifecycle audience.
═══ PATH 1: Top-level configuration ═══
Experience type: client_personalization
Variants (each binds to a lifecycle/visitor-stage audience):
- Control (audience = all (fallback): generic CTA) "Get started"
- Variant B (audience = "First-time visitors / no account"): "Start your free trial"
 - Audience: Users.First seen within current session OR Users.First seen is null
 - AND Users has no Subscription started event
- Variant C (audience = "Returning visitors / no account / no signup"): "Continue exploring [Brand]"
 - Audience: Users.First seen older than current session AND Users has no User created event
- Variant D (audience = "Free trial users currently on trial"): "Continue your trial"
 - Audience: Users has User created event AND Users has no Subscription started event with billing_period set
- Variant E (audience = "Active free plan users"): "Upgrade to Pro"
 - Audience: Users has Subscription started where Plan = "free"
- Variant F (audience = "Paying customers"): "Open dashboard"
 - Audience: Users has Subscription started where Plan != "free" AND no Subscription canceled
Targeting:
- Pages: homepage "/", marketing pages, /pricing, /features
- Devices: any
- Display frequency: always
Metrics (CRM/CDP):
- Click on per CTA copy per audience (per-segment CTR is the headline metric)
- Downstream conversion: signup, trial-to-paid, free-to-paid upgrade: measured per audience
Schedule: continuous
═══ PATH 2: Variant HTML content (Visual Editor) ═══
Variant: Control (no DOM changes: fallback "Get started" remains)
Variant: B (first-time visitors)
 HTML target selector: .primary-cta-button (the page's primary CTA)
 Replacement HTML:
 <button class="primary-cta" data-variant="b" data-audience="first-time" id="primary-cta">
 Start your free trial
 </button>
Variant: C (returning, no account)
 HTML target selector: .primary-cta-button
 Replacement HTML:
 <button class="primary-cta" data-variant="c" data-audience="returning" id="primary-cta">
 Continue exploring [Brand]
 </button>
Variant: D (trial users)
 HTML target selector: .primary-cta-button
 Replacement HTML:
 <button class="primary-cta" data-variant="d" data-audience="trial" id="primary-cta">
 Continue your trial
 </button>
Variant: E (free plan users)
 HTML target selector: .primary-cta-button
 Replacement HTML:
 <button class="primary-cta" data-variant="e" data-audience="free-plan" id="primary-cta">
 Upgrade to Pro
 </button>
Variant: F (paying customers)
 HTML target selector: .primary-cta-button
 Replacement HTML:
 <button class="primary-cta" data-variant="f" data-audience="paying" id="primary-cta">
 Open dashboard
 </button>
The Visual Editor allows the user to refine the exact copy ("Start MY free trial" first-person tested 202% lift). The CTA's link target also changes per audience: trial users go to /app, free-plan users go to /upgrade, paying customers go to /dashboard.
Taxonomy notes:
- Uses canonical events: Users.First seen, User created, Subscription started (with Plan and billing_period properties).
- The CTA target_id remains "primary-cta" across variants for consistent Click on aggregation.
- The 202% lift figure (cited multiple times in 2026 SaaS research) is for first-person CTA copy ("Start MY free trial") personalized by visitor intent. This recipe enables that pattern.
- Don't over-segment: 5-6 lifecycle audiences is the sweet spot. Beyond that, content authoring overhead exceeds the gains.
- Combine with source-based-personalization for compounding effect: a first-time visitor from LinkedIn enterprise ads sees both source-matched hero (Variant B from source-based) AND first-person CTA copy (Variant B from this recipe). Order precedence: source beats lifecycle when both apply.
