---
frontmatter_id: time-to-aha-moment
slash_command: /time-to-aha-moment
description: Measure the median time for new users to reach their first activation goal. Use funnel percentiles to assess how quickly users activate.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how long new users take to reach their first activation goal, as a time distribution with cumulative percentages,
    split by signup source and compared to the prior period.
  parameters:
  - name: activation_journey_id
    type: string
    label: Activation journey ID
    default: <UNKNOWN>
    required: true
  - name: cohort_window
    type: duration
    label: Signup cohort window
    default: 90 d
  - name: activation_window
    type: duration
    label: Activation window
    default: 14 d
  - name: top_sources
    type: number
    label: Number of top signup sources to break down
    default: 6
  - name: never_alert_threshold
    type: number
    label: Alert threshold for share of users who never activate (%)
    default: 50
  requirements:
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
    properties:
    - name: utm_source
      type: text
      meaning: Signup source channel of the user
      optional: true
  - slot: journey_goal_completed_event
    kind: event
    meaning: A user completed a journey goal in the activation journey
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey the goal belongs to
      optional: false
  - slot: user_utm_source_attribute
    kind: attribute
    meaning: The user's first-touch signup source (UTM source)
  steps:
  - id: s1
    builds: report
    uses:
    - user_created_event
    - journey_goal_completed_event
    - user_utm_source_attribute
    - activation_journey_id
    - cohort_window
    - activation_window
    - top_sources
    - never_alert_threshold
    instruction: 'Create an Insights report titled "Time to Aha Moment". Series A: a distribution histogram of the time elapsed
      between each user''s {user_created_event} and their first {journey_goal_completed_event} where journey_id equals {activation_journey_id}.
      Use these buckets: 0-5 min, 5-30 min, 30 min-2 hr, 2-6 hr, 6-24 hr, 1-3 days, 3-7 days, 7-14 days, and never (no goal
      within {activation_window}). Series B: cumulative percentage of new users who reached the aha moment within each time
      X. Time range: users created in the last {cohort_window}, so every user has had at least {activation_window} to activate.
      Break down by {user_utm_source_attribute}, showing the top {top_sources} signup sources. Compare against the previous
      period of the same length. Display as a histogram with the cumulative percentage as a secondary line. Add these annotations:
      (1) benchmarks: top-quartile product-led products see 30%+ of new users reach the aha moment within 24 hours, the median
      is closer to 10% within 24 hours, and a good time-to-value is under 48 hours. (2) Highlight the 50th-percentile bucket
      as the median time-to-aha. (3) Highlight the median time-to-aha for each signup source. (4) Flag if the never bucket
      exceeds {never_alert_threshold}% of signups, meaning half of signups never reach value. (5) Flag the signup source with
      the slowest median time-to-aha as either an audience mismatch or an onboarding sequence problem for that channel.'
---

# Time to first value

Slash command: /time-to-aha-moment

## Step 1: Chart time from signup to first goal

Create an Insights report called "Time to Aha Moment".
Series A: Distribution histogram of time elapsed between each user's User created and their first Completed a journey goal for the activation journey
Series B: Cumulative percentage: what % of new users hit the aha moment within X time
Buckets for Series A: 0-5 min / 5-30 min / 30 min-2 hr / 2-6 hr / 6-24 hr / 1-3 days / 3-7 days / 7-14 days / never (haven't hit aha within 14 days)
Time range: Users created in the last 90 days (those who have had 14+ days to activate)
Breakdown: By Users.UTM source (signup source: top 6 channels)
Compare: Previous period (prior 90 days of cohort)
Chart type: Histogram with the cumulative % overlay as a secondary line
Annotations:
- Add benchmarks: top-quartile PLG products see 30%+ of new users hit aha within 24 hours; median is closer to 10% within 24 hours. Industry "good" time-to-value is <48 hours.
- Highlight the median time-to-aha (the 50th percentile bucket).
- Highlight the median per signup source: different sources often have wildly different aha-times (organic users often faster than paid; partner referrals often fastest of all).
- Flag if the "never" bucket (didn't activate within 14 days) is >50%: half your signups never experience value; severe activation problem.
- Flag the source with the worst aha-time: this is either an ICP mismatch or an onboarding sequence issue specific to that channel's audience.
Use case: distinct from the activation funnel (which is conversion %). This is the time-distribution view: answers "WHEN do users get value?" not just "DO they?" Time-to-value is the leading indicator of retention; users who hit aha fast retain at materially higher rates.
Taxonomy notes:
- User created and Completed a journey goal are canonical. The activation journey is project-specific (configurable journey_id).
- Users.UTM source is the canonical first-touch source.
