---
name: trial-to-paid-conversion-rate
description: |
  Use when a user mentions "trial-to-paid conversion rate", or asks for related help. Weekly trial-to-paid conversion using subscription_created.trial_end semantics with 18% benchmark.
arguments: []
intempt:
  id: trial-to-paid-conversion-rate
  version: 1.0.0
  slashCommand: /trial-to-paid-conversion-rate
  group: Reports
  shortDescription: "Weekly trial-to-paid conversion using subscription_created.trial_end semantics with 18% benchmark."
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
  prerequisites:
    integrations:
      - { value: stripe, severity: blocking }
  invokesCommands:
    - build_insights_report
  procedure:
    - step: 1
      title: "Build Insights Report"
      command: build_insights_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create an Insights report called "Trial-to-Paid Conversion Rate".

        Series A: Event "subscription_created" where trial_end is not null AND trial_start is not null, aggregation: Count Unique Users
          → this is the trial-start cohort
        Series B: Event "subscription_created" filtered to users in Series A whose subsequent subscription transitioned out of trial state — operationally: count users in Series A who have a follow-on revenue_completed event or an invoice_paid event after the trial_end date
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

        Identify which signup source has the highest conversion AND volume — that's where to double down on acquisition spend.

        Taxonomy notes:
        - subscription_created carries trial_start, trial_end, plan_name, amount, status. A trial = subscription_created with both trial_start and trial_end populated.
        - "Converted to paid" is computed from a follow-on invoice_paid (Stripe-billed) or revenue_completed event after trial_end. There is no canonical "trial_started" event — the trial-start cohort is derived from subscription_created with trial fields populated.
        - Users.utm_source is real; signup_source as a property name is not.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Trial-to-Paid Conversion Rate

## Procedure

1. **Build Insights Report** [`build_insights_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create an Insights report called "Trial-to-Paid Conversion Rate".

   Series A: Event "subscription_created" where trial_end is not null AND trial_start is not null, aggregation: Count Unique Users
     → this is the trial-start cohort
   Series B: Event "subscription_created" filtered to users in Series A whose subsequent subscription transitioned out of trial state — operationally: count users in Series A who have a follow-on revenue_completed event or an invoice_paid event after the trial_end date
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

   Identify which signup source has the highest conversion AND volume — that's where to double down on acquisition spend.

   Taxonomy notes:
   - subscription_created carries trial_start, trial_end, plan_name, amount, status. A trial = subscription_created with both trial_start and trial_end populated.
   - "Converted to paid" is computed from a follow-on invoice_paid (Stripe-billed) or revenue_completed event after trial_end. There is no canonical "trial_started" event — the trial-start cohort is derived from subscription_created with trial fields populated.
   - Users.utm_source is real; signup_source as a property name is not.
   ```
