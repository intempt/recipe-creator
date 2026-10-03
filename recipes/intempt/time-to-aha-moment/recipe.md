---
id: time-to-aha-moment
title: Time to first value
slash_command: /time-to-aha-moment
group: Reports
owner: intempt
summary: Shows how long new users take to reach their first activation goal, so you can tell whether onboarding
  works in minutes or in days.
description: >-
  Histogram of time from user_created to first activation goal: surfaces whether users hit aha in 5 min,
  5 hours, or 5 days.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - saas
  complexity: quick
  executionMode: live
  tags:
    - insights
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Chart time from signup to first goal"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Chart time from signup to first goal
    summary: >-
      A distribution of the gap between signup and the first activation goal, bucketed from under 5 minutes
      out to 14 days plus a never bucket, for users created in the last 90 days and split by signup source.
      Flags a never bucket above 50%.
    builds: report
    description: |-
      Create an Insights report called "Time to Aha Moment".
      Series A: Distribution histogram of time elapsed between each user's user_created and their first goal_completed_in_journey for the activation journey
      Series B: Cumulative percentage: what % of new users hit the aha moment within X time
      Buckets for Series A: 0-5 min / 5-30 min / 30 min-2 hr / 2-6 hr / 6-24 hr / 1-3 days / 3-7 days / 7-14 days / never (haven't hit aha within 14 days)
      Time range: Users created in the last 90 days (those who have had 14+ days to activate)
      Breakdown: By Users.utm_source (signup source: top 6 channels)
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
      - user_created and goal_completed_in_journey are canonical. The activation journey is project-specific (configurable journey_id).
      - Users.utm_source is the canonical first-touch source.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Time to first value

Shows how long new users take to reach their first activation goal, so you can tell whether onboarding works in minutes or in days.

## Steps

1. **Chart time from signup to first goal** (builds report)

   A distribution of the gap between signup and the first activation goal, bucketed from under 5 minutes out to 14 days plus a never bucket, for users created in the last 90 days and split by signup source. Flags a never bucket above 50%.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Chart time from signup to first goal"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
