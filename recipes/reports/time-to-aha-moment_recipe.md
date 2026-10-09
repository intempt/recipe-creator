---
name: time-to-aha-moment
description: |
  Use when a user mentions "time to aha moment", or asks for related help. Histogram of time from user signup to first activation goal: surfaces whether users hit aha in 5 min, 5 hours, or 5 days.
arguments: []
intempt:
  id: time-to-aha-moment
  version: 1.0.0
  slashCommand: /time-to-aha-moment
  group: Reports
  title: "Time to first value"
  shortDescription: "Shows how long new users take to reach their first activation goal, so you can tell whether onboarding works in minutes or in days."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
    complexity: quick
    executionMode: live
    tags: [insights]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Chart time from signup to first goal"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "A distribution of the gap between signup and the first activation goal, bucketed from under 5 minutes out to 14 days plus a never bucket, for users created in the last 90 days and split by signup source. Flags a never bucket above 50%."
      prompt: |
        Create an Insights report called "Time to Aha Moment".

        Series A: Distribution histogram of time elapsed between each user's signup and their first completed activation goal
        Series B: Cumulative percentage: what % of new users hit the aha moment within X time

        Buckets for Series A: 0-5 min / 5-30 min / 30 min-2 hr / 2-6 hr / 6-24 hr / 1-3 days / 3-7 days / 7-14 days / never (haven't hit aha within 14 days)

        Time range: Users created in the last 90 days (those who have had 14+ days to activate)
        Breakdown: By signup source (first-touch UTM source): top 6 channels
        Compare: Previous period (prior 90 days of cohort)
        Chart type: Histogram with the cumulative % overlay as a secondary line

        Annotations:
        - Add benchmarks: top-quartile PLG products see 30%+ of new users hit aha within 24 hours; median is closer to 10% within 24 hours. Industry "good" time-to-value is <48 hours.
        - Highlight the median time-to-aha (the 50th percentile bucket).
        - Highlight the median per signup source: different sources often have wildly different aha-times (organic users often faster than paid; partner referrals often fastest of all).
        - Flag if the "never" bucket (didn't activate within 14 days) is >50%: half your signups never experience value; severe activation problem.
        - Flag the source with the worst aha-time: this is either an ICP mismatch or an onboarding sequence issue specific to that channel's audience.

        Use case: distinct from the activation funnel (which is conversion %). This is the time-distribution view: answers "WHEN do users get value?" not just "DO they?" Time-to-value is the leading indicator of retention; users who hit aha fast retain at materially higher rates.

        The activation journey is specific to each project.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Time to first value

Shows how long new users take to reach their first activation goal, so you can tell whether onboarding works in minutes or in days.

## What it does

1. **Chart time from signup to first goal** (`build_insights_report`)

   A distribution of the gap between signup and the first activation goal, bucketed from under 5 minutes out to 14 days plus a never bucket, for users created in the last 90 days and split by signup source. Flags a never bucket above 50%.

## What you end up with

- **report** (report): Report produced by this recipe.
