---
frontmatter_id: feature-paywall-conversion
slash_command: /feature-paywall-conversion
description: Reports per-feature engagement among free users and their pricing page views, to inform feature-gating strategy. It does not sequence feature use to payment or show quadrants.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows which product features free users try most, and how often each feature leads to a pricing page view and a
    paid subscription, to guide which features to gate.
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
  - slot: feature_usage_report_destination
    kind: destination
    meaning: A destination where the feature-to-paywall report can be created
    optional: true
    channel: email
  steps:
  - id: s1
    builds: report
    uses:
    - feature_click_event
    - pricing_page_view_event
    - subscription_started_event
    - paid_subscriber_attribute
    - lookbackWindow
    - conversionWindow
    - featurePattern
    instruction: 'Create an insights report named "Feature to Paywall Conversion". Series A: count unique users of {feature_click_event}
      where {feature_click_event.target_id} matches {featurePattern}, limited to users without a started paid subscription
      ({paid_subscriber_attribute} not set), broken down by {feature_click_event.target_id}, labeled "Free Users Who Tried
      Feature". Series B: of the users in Series A, those who later triggered {pricing_page_view_event} with {pricing_page_view_event.page_url}
      containing "/pricing" within {conversionWindow} of the feature click, labeled "Reached Paywall". Series C: of the users
      in Series A, those who later triggered {subscription_started_event} with {subscription_started_event.trial_end} empty
      (paid, non-trial) within {conversionWindow}, labeled "Converted to Paid". Series D: computed as Series B divided by
      Series A times 100, unit %, labeled "Feature to Paywall Rate". Series E: computed as Series C divided by Series A times
      100, unit %, labeled "Feature to Paid Rate". Time range: {lookbackWindow}. Compare against the previous period of the
      same length. Chart as a scatter plot with X = Series D, Y = Series E, bubble size = Series A, one bubble per feature.
      Add quadrant labels: high paywall and high paid means monetizing features to gate or promote in upgrade prompts; high
      paywall and low paid means features that intrigue but do not close, a pricing or positioning issue; low paywall and
      high paid means stealth-monetization features that need no gate; low paywall and low paid means low-monetization features
      to keep free without over-investing. Flag any feature with high free-tier usage and zero conversion lift as pure cost
      to consider deprecating or gating. Highlight the top 3 features by Series E as the paywall-optimal features. Surface
      the feature with the largest gap where Series D is much higher than Series E as a pricing-perception issue.'
---

# Feature to paywall conversion

Slash command: /feature-paywall-conversion

## Step 1: Rank features by paid conversion

Create an Insights report called "Feature to Paywall Conversion".
Series A: Event "Click on" filtered by target_id matching a feature pattern, scoped to free-plan users (users without a paid Subscription started), aggregation: Count Unique Users per target_id, label: "Free Users Who Tried Feature"
Series B: Of the users in Series A, those who subsequently emitted a View page where Page URL contains "/pricing" within 30 days of the feature click, label: "Reached Paywall"
Series C: Of the users in Series A, those who subsequently emitted Subscription started (with trial_end null: paid, non-trial) within 30 days, label: "Converted to Paid"
Series D: Computed: Series B / Series A × 100, unit: %, label: "Feature to Paywall Rate"
Series E: Computed: Series C / Series A × 100, unit: %, label: "Feature to Paid Rate"
Breakdown: By target_id (the specific feature)
Time range: Last 90 days
Compare: Previous period (prior 90 days)
Chart type: Scatter plot: X axis = Feature to Paywall Rate (Series D), Y axis = Feature to Paid Rate (Series E), bubble size = Series A volume (free users who tried). Each bubble is a feature.
Annotations:
- Quadrant labeling on the scatter:
 - High Paywall + High Paid: features that drive monetization (gate them, or use them as the upgrade pitch). Promote in upgrade prompts.
 - High Paywall + Low Paid: features that intrigue but don't close (paywall view is happening but pricing isn't compelling: pricing/positioning issue).
 - Low Paywall + High Paid: stealth-monetization features (users convert without going through pricing: already sold; no need to gate).
 - Low Paywall + Low Paid: low-monetization features (giveaways: keep in free tier, don't gate, but also don't over-invest).
- Flag any feature with high free-tier usage AND zero conversion lift: these features are pure cost; consider deprecating or gating.
- Highlight the top 3 features by Feature to Paid Rate (Series E): these are the paywall-optimal features.
- Surface the feature with the largest Free to Paywall conversion gap (Series D much higher than Series E): pricing-perception issue specific to that feature.
Use case: Kyle Poyar's (OpenView) most-shared Amplitude template. Tells the product team which features to gate behind the paywall vs. which to give away vs. which to deprecate. The single most-actionable monetization analysis a SaaS product can run.
Taxonomy notes:
- Click on.target_id is the canonical feature handle.
- View page.Page URL filtered to /pricing identifies paywall views.
- Subscription started.trial_end null distinguishes paid from trial.
