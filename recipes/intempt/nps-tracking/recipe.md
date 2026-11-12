---
frontmatter_id: nps-tracking
slash_command: /nps-tracking
description: Tracks your Net Promoter Score month by month with the promoter, passive and detractor split behind it.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Tracks your Net Promoter Score month by month, showing the promoter, passive and detractor split behind the headline
    number, with benchmarks and alerts.
  parameters:
  - name: lookbackWindow
    type: duration
    label: Time range for the trend
    default: 12 m
    required: false
  - name: rollingWindow
    type: duration
    label: Rolling trend window
    default: 90 d
    required: false
  - name: dropThreshold
    type: number
    label: Alert when NPS drops by more than this many points vs. trailing 3-month average
    default: 10
    required: false
  - name: lowConfidenceSampleSize
    type: number
    label: Monthly response count below which a month is flagged low confidence
    default: 30
    required: false
  - name: underperformanceGap
    type: number
    label: Flag segments whose NPS is more than this many points below the blended average
    default: 15
    required: false
  - name: promoterMinScore
    type: number
    label: Lowest score counted as a promoter
    default: 9
    required: false
  - name: detractorMaxScore
    type: number
    label: Highest score counted as a detractor
    default: 6
    required: false
  - name: nps_survey_type_value
    type: string
    label: Value of survey_type that marks an NPS survey
    default: nps
    required: false
  requirements:
  - slot: nps_feedback_event
    kind: event
    meaning: A customer submitted feedback through a survey
    properties:
    - name: score
      type: number
      meaning: Survey score from 0 to 10
      optional: false
    - name: survey_type
      type: string
      meaning: Kind of survey that produced the feedback, e.g. nps
      optional: false
    - name: feedback_text
      type: text
      meaning: Free-text comment the customer wrote
      optional: true
    - name: sentiment
      type: string
      meaning: Sentiment label of the feedback
      optional: true
    - name: submitted_at
      type: date
      meaning: When the feedback was submitted
      optional: false
    - name: masterID
      type: string
      meaning: Customer identifier
      optional: false
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a customer is on (SaaS) or the first-purchase product category (ecommerce), used as an
      optional breakdown
    optional: true
  - slot: nps_report_destination
    kind: destination
    meaning: Where the NPS tracking report is saved and viewed
    optional: true
    channel: email
  steps:
  - id: s1
    builds: report
    uses:
    - nps_feedback_event
    - plan_attribute
    - lookbackWindow
    - rollingWindow
    - dropThreshold
    - lowConfidenceSampleSize
    - underperformanceGap
    - promoterMinScore
    - detractorMaxScore
    - nps_survey_type_value
    instruction: 'Create an Insights report called "NPS Tracking" that tracks the monthly Net Promoter Score from {nps_feedback_event}
      events where {nps_feedback_event.survey_type} equals {nps_survey_type_value}, over the last {lookbackWindow} with monthly
      granularity. Series A counts {nps_feedback_event} where {nps_feedback_event.score} is at least {promoterMinScore} and
      is labelled Promoters. Series B counts {nps_feedback_event} where {nps_feedback_event.score} is between 7 and 8 and
      is labelled Passives. Series C counts {nps_feedback_event} where {nps_feedback_event.score} is at most {detractorMaxScore}
      and is labelled Detractors. Series D is a computed NPS of (A minus C) divided by (A plus B plus C) multiplied by 100,
      unit number, labelled NPS Score. Series E is a trailing {rollingWindow} rolling NPS labelled NPS (90-day rolling). Chart
      type: stacked bar for Series A, B and C per month, with Series D as a line on a secondary axis. Colors: Promoters green,
      Passives gray, Detractors red. Compare against the same period one year earlier. Optional breakdown of the trend by
      {plan_attribute}. Annotations: show benchmarks (B2B SaaS median NPS 30, top quartile 50 or more, world-class 70 or more;
      eCommerce DTC median 30 to 40, top quartile 60 or more) and mark that a score below 0 means more detractors than promoters.
      Flag any month where Series D fell by more than {dropThreshold} points against the trailing 3-month average. Show the
      percentage of detractor responses that include {nps_feedback_event.feedback_text} as a highlighted voice-of-customer
      signal. Highlight any {plan_attribute} segment whose NPS is more than {underperformanceGap} points below the blended
      average. Show monthly response volume and add a low confidence flag for any month with fewer than {lowConfidenceSampleSize}
      responses.'
---

# NPS tracking

Slash command: /nps-tracking

## Step 1: Score NPS each month

Create an Insights report called "NPS Tracking".
Series A: Event "Feedback submitted" where survey_type = "nps", aggregation: Count where score >= 9 (promoters), label: "Promoters"
Series B: Event "Feedback submitted" where survey_type = "nps", aggregation: Count where score is between 7 and 8 (passives), label: "Passives"
Series C: Event "Feedback submitted" where survey_type = "nps", aggregation: Count where score <= 6 (detractors), label: "Detractors"
Series D: Computed NPS: (Series A − Series C) / (Series A + Series B + Series C) × 100, unit: # (NPS is reported as a score from -100 to +100), label: "NPS Score"
Series E: Trailing 90-day rolling NPS for trend smoothing, label: "NPS (90-day rolling)"
Time granularity: Monthly
Time range: Last 12 months
Breakdown for the trend chart: optional Plan (saas) or first-purchase product category (ecommerce)
Compare: Year-over-year
Chart type: Stacked bar chart for Series A/B/C distribution per month, with Series D (NPS) as a line on a secondary axis. Use color: Promoters green, Passives gray, Detractors red.
Annotations:
- Add benchmarks per industry: B2B SaaS median NPS is 30; top-quartile 50+; SaaS world-class 70+. eCommerce DTC median 30: 40; top-quartile 60+. Below 0 indicates a serious problem (more detractors than promoters).
- Flag any month where Series D dropped >10 points vs. trailing-3-month average.
- Highlight the % of detractors who left feedback_text: these are the highest-leverage voice-of-customer signals (act on the qualitative comments, not just the score).
- Highlight any plan/segment whose NPS is significantly below the blended average (>15 points lower): these are the audiences where product-market fit is weakest.
- Surface response volume per month: a falling NPS from a small sample (<30 responses/month) may not be statistically meaningful. Add a "low confidence" flag when monthly sample size <30.
Use case: every business tracks NPS but most never visualize the underlying promoter/passive/detractor distribution shifts that drive the score. A score of 30 with rising detractors is very different from a score of 30 with falling passives: same headline number, opposite direction.
Taxonomy notes:
- Feedback submitted has score, sentiment, survey_type, feedback_text, masterID, submitted_at: all canonical.
- This recipe assumes the workspace uses survey_type = "nps" to discriminate NPS surveys from other feedback. If the project uses a different value (e.g. "net_promoter"), adjust the filter.
- score is expected to be 0: 10 numeric. Workspaces emitting Feedback submitted from custom surveys may need to validate score range matches NPS convention.
- If the workspace doesn't have Feedback submitted events flowing reliably from their NPS tool (Delighted, AskNicely, Wootric, custom in-app surveys), this recipe degrades to "no data." Recommend ensuring NPS-survey integration is configured.
