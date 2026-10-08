---
description: Shows what share of each week's signups are still coming back at weeks 1, 4 and 12, and which acquisition sources hold up best.
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
  - media
---

# Weekly user retention

Slash command: /user-retention-weekly

## Step 1: Track weekly signup cohorts

Create a Retention report called "Weekly User Retention".
Anchor event: user_created
Return event: session_start
Cohort granularity: Weekly
Time range: Last 12 weeks (require cohorts to have completed full 12-week return window where possible)
Breakdown: By Users.utm_source (acquisition source)
Compare: Previous period (prior 12 weeks of cohorts)
Chart type: Retention curve (line per cohort) plus cohort table with W1 / W4 / W12 columns
Annotations:
- Add horizontal benchmarks: W1 retention 40% (B2B SaaS median), W4 25%, W12 15%.
- Flag any cohort where W1 retention dropped >5 percentage points vs. the prior cohort.
- Highlight the source with the strongest W12 retention (highest-quality acquisition channel).
- Identify whether retention curves are flattening over time (good (natural retention forming a plateau) or continuously decaying (bad) no stable user base forming).
Surface the source-by-source retention gap at W4: the moment by which most low-quality signups have churned out.
Taxonomy notes:
- user_created and session_start are canonical. Users.utm_source is the canonical first-touch attribute.
