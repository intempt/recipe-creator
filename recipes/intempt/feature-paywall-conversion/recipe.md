---
frontmatter_id: feature-paywall-conversion
slash_command: /feature-paywall-conversion
description: Emails a weekly digest of which features free users try, and how often each feature leads to a pricing page view
  and a paid subscription, to guide feature gating.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly per-feature digest of free-user use, pricing page reach and paid conversion, to guide which features
    to gate.
  parameters:
  - name: lookbackWindow
    type: duration
    label: Analysis time range
    default: 90 d
    required: false
  - name: conversionWindow
    type: duration
    label: Conversion window after feature use
    default: 30 d
    required: false
  - name: featurePattern
    type: string
    label: Feature target_id pattern to match
    default: feature
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: feature_click_event
    kind: event
    meaning: A user clicked a product feature element
    properties:
    - name: target_id
      type: string
      meaning: Identifier of the clicked feature element
      optional: false
  - slot: pricing_page_view_event
    kind: event
    meaning: A user viewed a page
    properties:
    - name: page_url
      type: string
      meaning: URL of the viewed page, used to detect pricing page views
      optional: false
  - slot: subscription_started_event
    kind: event
    meaning: A user started a paid subscription
    properties:
    - name: trial_end
      type: date
      meaning: Trial end date; empty means the subscription is paid, not a trial
      optional: false
  - slot: paid_subscriber_attribute
    kind: attribute
    meaning: Whether a user has a paid subscription started (used to identify free-plan users)
  steps:
  - id: s1
    builds: automation
    uses:
    - feature_click_event
    - pricing_page_view_event
    - subscription_started_event
    - paid_subscriber_attribute
    - lookbackWindow
    - conversionWindow
    - featurePattern
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users whose {paid_subscriber_attribute}
      is not set (free users) who did {feature_click_event} with {feature_click_event.target_id} matching {featurePattern}
      in the last {lookbackWindow}, against the {lookbackWindow} before, and writes these figures per target_id: free users
      who tried the feature; of those, users who did {pricing_page_view_event} with {pricing_page_view_event.page_url} containing
      "/pricing" within {conversionWindow} after the click, and that as a % (paywall rate); users who did {subscription_started_event}
      with {subscription_started_event.trial_end} empty within {conversionWindow} (paid rate %); the top 3 features by paid
      rate; the feature with the largest gap where paywall rate is far above paid rate; features with many free users and
      no paid conversions. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Feature to paywall conversion

Slash command: /feature-paywall-conversion

## Step 1: Email the weekly feature paywall digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users whose paid subscriber attribute is not set (free users) who did feature click event with target id matching feature in the last 90 d, against the 90 d before, and writes these figures per target_id: free users who tried the feature; of those, users who did pricing page view event with page url containing "/pricing" within 30 d after the click, and that as a % (paywall rate); users who did subscription started event with trial end empty within 30 d (paid rate %); the top 3 features by paid rate; the feature with the largest gap where paywall rate is far above paid rate; features with many free users and no paid conversions. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
