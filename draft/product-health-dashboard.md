---
description: Answers whether the product is getting more or less engaging, which features users return to, and how users say they feel. The cohort heatmap output is in Retention, not Insights.
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
  - media
  - social
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
