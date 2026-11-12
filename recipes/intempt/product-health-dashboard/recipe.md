---
frontmatter_id: product-health-dashboard
slash_command: /product-health-dashboard
description: Answers whether the product is getting more or less engaging, which features users return to, and how users say they feel. The cohort heatmap output is in Retention, not Insights.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives a product lead one dashboard showing whether engagement is rising or falling, which features users return
    to, and how users feel, read across four rows.
  parameters:
  - name: boardTitle
    type: string
    label: Board title
    default: Product Health
    required: false
  - name: defaultDateRange
    type: duration
    label: Default date range
    default: 30 d
    required: false
  - name: excludeIncompletePeriods
    type: boolean
    label: Exclude incomplete periods
    default: true
    required: false
  - name: boardVisibility
    type: enum
    label: Board visibility
    default: project
    required: false
    options:
    - project
    - private
  - name: breakdownProperty
    type: string
    label: Secondary breakdown (resolved from each user's most-recent active subscription)
    default: Plan
    required: false
  - name: npsSurveyType
    type: string
    label: NPS survey type value on feedback events
    default: nps
    required: false
  requirements:
  - slot: dau_wau_mau_stickiness_insight
    kind: knowledge
    meaning: An Insights metric recipe that reports DAU/MAU stickiness ratios over time (stickiness-ratios-dau-wau-mau).
  - slot: weekly_active_users_insight
    kind: knowledge
    meaning: An Insights metric recipe that reports weekly active users trend (weekly-active-users-trend).
  - slot: active_vs_passive_users_insight
    kind: knowledge
    meaning: An Insights recipe that splits users into active producers and passive consumers (active-vs-passive-users).
  - slot: nps_tracking_insight
    kind: knowledge
    meaning: An Insights recipe that tracks NPS score from feedback survey responses (nps-tracking).
  - slot: feature_adoption_by_plan_insight
    kind: knowledge
    meaning: An Insights recipe that reports feature adoption broken down by plan (feature-adoption-by-plan).
  - slot: feature_discovery_adoption_funnel
    kind: knowledge
    meaning: A Funnel recipe that shows feature discovery and adoption steps (feature-discovery-adoption).
  - slot: retention_lifted_by_feature_adoption
    kind: knowledge
    meaning: A Retention recipe comparing retention curves of users who adopted features versus those who did not (retention-lifted-by-feature-adoption).
  - slot: feature_usage_heatmap_by_cohort
    kind: knowledge
    meaning: An Insights recipe that shows a feature usage heatmap by cohort (feature-usage-heatmap-by-cohort).
  - slot: support_tickets_vs_churn_insight
    kind: knowledge
    meaning: An Insights recipe that correlates support ticket volume with churn (support-tickets-vs-churn-correlation).
  - slot: feedback_submitted_event
    kind: event
    meaning: A customer submitted feedback through a survey.
    properties:
    - name: survey_type
      type: string
      meaning: Type of survey the feedback belongs to; NPS responses use the value nps
      optional: false
  - slot: subscription_plan_attribute
    kind: attribute
    meaning: The plan on a user's most-recent active subscription.
  steps:
  - id: s1
    builds: dashboard
    uses:
    - dau_wau_mau_stickiness_insight
    - weekly_active_users_insight
    - active_vs_passive_users_insight
    - nps_tracking_insight
    - feature_adoption_by_plan_insight
    - feature_discovery_adoption_funnel
    - retention_lifted_by_feature_adoption
    - feature_usage_heatmap_by_cohort
    - support_tickets_vs_churn_insight
    - feedback_submitted_event
    - subscription_plan_attribute
    - boardTitle
    - defaultDateRange
    - excludeIncompletePeriods
    - boardVisibility
    - breakdownProperty
    - npsSurveyType
    instruction: 'Create a 12-column Dash board titled "{boardTitle}" with project visibility "{boardVisibility}", default
      date range {defaultDateRange}, exclude incomplete periods set to {excludeIncompletePeriods}, and no board filters by
      default. Push the {breakdownProperty} breakdown (resolved from each user''s most-recent active subscription) down to
      all cards as a secondary breakdown. Lay out four rows. Row 1 (height 200 px) holds four metric cards at 3 units each:
      DAU/MAU stickiness from {dau_wau_mau_stickiness_insight} titled "DAU/MAU Stickiness"; WAU from {weekly_active_users_insight}
      titled "WAU"; Producer Share % from {active_vs_passive_users_insight} titled "Producer Share %"; NPS score from {nps_tracking_insight}
      titled "NPS Score". Row 2 (height 440 px) holds two 6-unit cards: a bar chart from {feature_adoption_by_plan_insight},
      and a funnel_steps chart from {feature_discovery_adoption_funnel}. Row 3 (height 400 px) holds two 6-unit cards: the
      side-by-side retention curve comparison chart from {retention_lifted_by_feature_adoption}, and a heatmap chart from
      {feature_usage_heatmap_by_cohort}. Row 4 (height 400 px) holds two 6-unit cards: a stacked area chart from {active_vs_passive_users_insight},
      and a dual-axis line chart from {support_tickets_vs_churn_insight}. NPS survey responses depend on feedback events where
      {feedback_submitted_event.survey_type} equals {npsSurveyType}. Annotate Row 1: the four KPIs together show whether users
      are active (WAU), sticky (DAU/MAU), actively producing (Producer Share %), and how they feel (NPS); read them together.
      Annotate the board: read the four rows together, where Row 1 gives headline state, Row 2 feature engagement depth, Row
      3 retention drivers, and Row 4 segmentation and support pulse.'
---

# Product engagement and adoption

Slash command: /product-health-dashboard

## Step 1: Build the product health board

Create a Dash board (12-column composition canvas) titled "Product Health".
Persona: Product Manager / Product Lead. Question answered: "Is the product getting more or less engaging? Which features matter? How do users feel about it?"
Board-level configuration:
- defaultDateRange: last_30_days
- exclusionPeriod: incomplete_periods
- visibility: project
- boardFilters: none by default
- boardBreakdowns: Plan (resolved from each user's most-recent active subscription): pushed down to all cards as a secondary breakdown
Layout: 4 rows.
Row 1: Engagement headline (heightPx: 200, four metric cards at widthUnits: 3):
- Card 1: Insights metric to source recipe: stickiness-ratios-dau-wau-mau, vizType: metric, titleOverride: "DAU/MAU Stickiness"
- Card 2: Insights metric to source recipe: weekly-active-users-trend, vizType: metric, titleOverride: "WAU"
- Card 3: Insights metric to source recipe: active-vs-passive-users, vizType: metric, titleOverride: "Producer Share %"
- Card 4: Insights metric to source recipe: nps-tracking, vizType: metric, titleOverride: "NPS Score"
Row 2: Feature engagement depth (heightPx: 440, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: feature-adoption-by-plan, displayMode: chart, vizType: bar
- Card 2: Funnel to source recipe: feature-discovery-adoption, displayMode: chart, vizType: funnel_steps
Row 3: Retention drivers (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Retention to source recipe: retention-lifted-by-feature-adoption, displayMode: chart (the side-by-side curve comparison)
- Card 2: Insights to source recipe: feature-usage-heatmap-by-cohort, displayMode: chart, vizType: heatmap
Row 4: Engagement segmentation and support pulse (heightPx: 400, two cards at widthUnits: 6):
- Card 1: Insights to source recipe: active-vs-passive-users, displayMode: chart, vizType: stacked_area
- Card 2: Insights to source recipe: support-tickets-vs-churn-correlation, displayMode: chart, vizType: line (dual-axis)
Annotations:
- Row 1's four KPIs together answer: are users active (WAU), are they sticky (DAU/MAU), are they actively producing (Producer Share %), and how do they feel (NPS). Each is a different lens; reading them together is the key.
- The board's value comes from reading the four rows together: Row 1 reports headline state, Row 2 reports feature engagement depth, Row 3 reports retention drivers, Row 4 reports segmentation and support pulse.
Taxonomy notes:
- All 8 source recipes are taxonomy-grounded.
- nps-tracking depends on Feedback submitted events with survey_type = "nps": see that recipe's notes.
