---
frontmatter_id: product-health-dashboard
slash_command: /product-health-dashboard
description: Emails a product lead a weekly digest of whether the product is getting more or less engaging, which features
  users return to, and how users say they feel.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a weekly product health digest: weekly actives, stickiness, feature adoption by plan, retention of feature
    adopters, NPS and support tickets.'
  parameters:
  - name: npsSurveyType
    type: string
    label: Survey type value of NPS answers
    default: nps
    required: false
  - name: topFeatureCount
    type: number
    label: Features listed by adoption
    default: 10
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: feature_used_event
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature
      type: string
      meaning: Name of the feature used
      optional: false
  - slot: feedback_submitted_event
    kind: event
    meaning: A user answered a feedback survey
    properties:
    - name: survey_type
      type: string
      meaning: Kind of survey, such as nps
      optional: false
    - name: score
      type: number
      meaning: The 0-10 rating given
      optional: false
  - slot: ticket_created_event
    kind: event
    meaning: A user created a support ticket
    optional: true
  - slot: subscription_plan_attribute
    kind: attribute
    meaning: The plan on the user's most recent active subscription
  steps:
  - id: s1
    builds: automation
    uses:
    - session_start_event
    - feature_used_event
    - feedback_submitted_event
    - ticket_created_event
    - subscription_plan_attribute
    - npsSurveyType
    - topFeatureCount
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes
      these figures: weekly active users (did {session_start_event} in the last 7 days) against the 7 days before; stickiness,
      the average daily active users over the last 30 days divided by the users active in those 30 days, against the 30 days
      before; the {topFeatureCount} {feature_used_event.feature} values used by the largest share of weekly active users,
      per {subscription_plan_attribute}; the share of users who signed up 4 to 8 weeks ago and are active this week, split
      by whether they did {feature_used_event} in their first 7 days; NPS over the last 30 days from {feedback_submitted_event}
      where {feedback_submitted_event.survey_type} is {npsSurveyType}, as % of scores 9-10 minus % of scores 0-6; the count
      of {ticket_created_event} in the last 7 days against the 7 days before, when that event exists. Then it emails these
      figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Product engagement and adoption

Slash command: /product-health-dashboard

## Step 1: Email the weekly product health digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users and writes these figures: weekly active users (did session start event in the last 7 days) against the 7 days before; stickiness, the average daily active users over the last 30 days divided by the users active in those 30 days, against the 30 days before; the 10 feature values used by the largest share of weekly active users, per subscription plan attribute; the share of users who signed up 4 to 8 weeks ago and are active this week, split by whether they did feature used event in their first 7 days; NPS over the last 30 days from feedback submitted event where survey type is nps, as % of scores 9-10 minus % of scores 0-6; the count of ticket created event in the last 7 days against the 7 days before, when that event exists. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
