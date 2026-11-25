---
frontmatter_id: nps-tracking
slash_command: /nps-tracking
description: Emails a monthly digest of your Net Promoter Score with the promoter, passive and detractor split behind it,
  and an alert when the score drops.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a monthly digest of your Net Promoter Score with the promoter, passive and detractor split, a rolling trend
    and drop alerts.
  parameters:
  - name: lookbackWindow
    type: duration
    label: Time range for the trend
    default: 12 mo
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a customer is on (SaaS) or the first-purchase product category (ecommerce), used as an
      optional breakdown
    optional: true
  steps:
  - id: s1
    builds: automation
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
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes {nps_feedback_event}
      with {nps_feedback_event.survey_type} equal to {nps_survey_type_value} and writes these figures for the last 30 days
      and for each 30 days over the last {lookbackWindow}: promoters ({nps_feedback_event.score} of {promoterMinScore} or
      more), passives (7 to 8), detractors ({detractorMaxScore} or less), response count, and NPS = (promoters - detractors)
      / responses x 100; the NPS over the last {rollingWindow}; the NPS a year ago; the % of detractor answers with {nps_feedback_event.feedback_text};
      NPS by {plan_attribute} when it is set. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      When NPS fell more than {dropThreshold} points against the average of the 90 days before, the email''s first line says
      so. The email marks months with fewer than {lowConfidenceSampleSize} responses as low confidence and names plans more
      than {underperformanceGap} points below the overall NPS. Nothing else is sent.'
---

# NPS tracking

Slash command: /nps-tracking

## Step 1: Email the monthly NPS tracking digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes nps feedback event with survey type equal to nps and writes these figures for the last 30 days and for each 30 days over the last 12 mo: promoters (score of 9 or more), passives (7 to 8), detractors (6 or less), response count, and NPS = (promoters - detractors) / responses x 100; the NPS over the last 90 d; the NPS a year ago; the % of detractor answers with feedback text; NPS by plan attribute when it is set. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. When NPS fell more than 10 points against the average of the 90 days before, the email's first line says so. The email marks months with fewer than 30 responses as low confidence and names plans more than 15 points below the overall NPS. Nothing else is sent.
