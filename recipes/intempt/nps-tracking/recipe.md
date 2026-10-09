---
description: Tracks your Net Promoter Score month by month with the promoter, passive and detractor split behind it.
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
  - ecommerce
  - finance
  - media
  - social
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
