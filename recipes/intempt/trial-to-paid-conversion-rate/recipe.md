---
description: Shows what share of trials turn into paying customers each week, by signup source, against the 18% industry median.
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
  - finance
  - media
---

# Trial to paid conversion rate

Slash command: /trial-to-paid-conversion-rate

## Step 1: Track trial conversion weekly

Create an Insights report called "Trial-to-Paid Conversion Rate".
Series A: Event "subscription_created" where trial_end is not null AND trial_start is not null, aggregation: Count Unique Users
 to this is the trial-start cohort
Series B: Event "subscription_created" filtered to users in Series A whose subsequent subscription transitioned out of trial state: operationally: count users in Series A who have a follow-on revenue_completed event or an invoice_paid event after the trial_end date
Formula: (B / A) × 100, unit: %, label: "Trial-to-Paid Conversion"
Time granularity: Weekly (cohort by trial-start week, allow the trial window to fully elapse before counting)
Time range: Last 12 weeks (where the trial window has fully elapsed)
Breakdown: By "utm_source" attribute on the Users object (signup source)
Compare: Previous period (previous 12 weeks)
Chart type: Line chart with previous-period overlay
Annotations:
- Add a horizontal benchmark line at 18% (median for B2B SaaS with self-serve trials).
- Add a horizontal benchmark line at 25% (top-quartile threshold).
- Highlight any week where the conversion rate dropped >3 percentage points vs. previous period.
Identify which signup source has the highest conversion AND volume: that's where to double down on acquisition spend.
Taxonomy notes:
- subscription_created carries trial_start, trial_end, plan_name, amount, status. A trial = subscription_created with both trial_start and trial_end populated.
- "Converted to paid" is computed from a follow-on invoice_paid (Stripe-billed) or revenue_completed event after trial_end. There is no canonical "trial_started" event: the trial-start cohort is derived from subscription_created with trial fields populated.
- Users.utm_source is real; signup_source as a property name is not.
