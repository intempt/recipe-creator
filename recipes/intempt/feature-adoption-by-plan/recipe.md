---
frontmatter_id: feature-adoption-by-plan
slash_command: /feature-adoption-by-plan
description: Emails a weekly digest of which features each plan tier adopts, the adoption rate of each feature per plan, and
  flags for upsell, deprecation and load-bearing features.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of feature adoption rates per plan tier, with the change from the period before and flags
    for upsell, low-use and load-bearing features.
  parameters:
  - name: time_window
    type: duration
    label: Window analyzed
    default: 30 d
    required: false
  - name: comparison_window
    type: duration
    label: Earlier window it is compared with
    default: 30 d
    required: false
  - name: high_adoption_threshold
    type: number
    label: Adoption rate that makes a feature load-bearing (%)
    default: 40
    required: false
  - name: upgrade_ratio_threshold
    type: number
    label: How many times higher adoption on a higher plan marks an upsell feature
    default: 2
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a page element that identifies a product feature
    properties:
    - name: target_id
      type: text
      meaning: Stable identifier of the feature surface clicked
      optional: false
    - name: target_text
      type: text
      meaning: Human-readable label of the clicked element
      optional: true
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription to a plan
    properties:
    - name: Plan
      type: text
      meaning: The plan tier the customer subscribed to
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - feature_click_event
    - subscription_started_event
    - time_window
    - comparison_window
    - high_adoption_threshold
    - upgrade_ratio_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users active in
      the last {time_window}, with each user''s plan taken from their latest {subscription_started_event.Plan}, and writes
      these figures: for each feature by {feature_click_event.target_id} (named by {feature_click_event.target_text} when
      set) and each plan, the adoption rate, the share of that plan''s active users who did {feature_click_event} on it, next
      to the {comparison_window} before; features whose adoption is at least {high_adoption_threshold}% on every plan, called
      load-bearing; features adopted at least {upgrade_ratio_threshold} times more on a higher plan than on a lower one, called
      upsell features; the 5 features with the lowest adoption on every plan, called low-use. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Feature adoption by plan

Slash command: /feature-adoption-by-plan

## Step 1: Email the weekly feature adoption digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users active in the last 30 d, with each user's plan taken from their latest Plan, and writes these figures: for each feature by target id (named by target text when set) and each plan, the adoption rate, the share of that plan's active users who did feature click event on it, next to the 30 d before; features whose adoption is at least 40% on every plan, called load-bearing; features adopted at least 2 times more on a higher plan than on a lower one, called upsell features; the 5 features with the lowest adoption on every plan, called low-use. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
