---
description: Measure the median time for new users to reach their first activation goal. Use funnel percentiles to assess how quickly users activate.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
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
