---
frontmatter_id: weekly-business-review-summary
slash_command: /weekly-business-review-summary
description: 'One scorecard with the six numbers to look at every Monday: new signups, new paying customers, churn, revenue, net new customers and engagement.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Gives a Monday scorecard of six weekly numbers (signups, new paying customers, churn, revenue, net new customers,
    engagement) with trends, comparisons and attention flags.
  parameters:
  - name: window_weeks
    type: number
    label: Lookback window (weeks)
    default: 12
    required: false
  - name: wow_alert_threshold
    type: number
    label: Week-over-week alert threshold (%)
    default: 15
    required: false
  - name: durable_trend_weeks
    type: number
    label: Consecutive weeks for durable wrong-direction trend
    default: 4
    required: false
  - name: churn_inactive_days
    type: duration
    label: Inactivity period that counts as churn for ecommerce
    default: 90 d
    required: false
  - name: dau_window
    type: duration
    label: Engagement trailing window
    default: 7 d
    required: false
  - name: business_model
    type: enum
    label: Business model
    default: saas
    required: false
    options:
    - saas
    - ecommerce
  requirements:
  - slot: signup_event
    kind: event
    meaning: A new user account was created
  - slot: paid_subscription_event
    kind: event
    meaning: A customer started a paid subscription
    properties:
    - name: trial_end
      type: date
      meaning: When the trial ended; empty for direct paid signups
      optional: true
  - slot: first_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: total_price
      type: number
      meaning: Order total amount
      optional: false
  - slot: subscription_canceled_event
    kind: event
    meaning: A customer canceled a subscription
  - slot: revenue_event
    kind: event
    meaning: Recurring revenue was completed for a customer
    properties:
    - name: amount
      type: number
      meaning: Revenue amount
      optional: false
    - name: type
      type: string
      meaning: Revenue type, indicating whether it is recurring
      optional: false
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product
  - slot: last_seen_attribute
    kind: attribute
    meaning: The last time a user was seen active
  steps:
  - id: s1
    builds: report
    instruction: 'Create an Insights report titled "Weekly Business Review Summary" shown as a multi-card KPI scorecard over
      the last {window_weeks} weeks, weekly granularity, compared with the prior period and year-over-year. Series A: count
      unique users of {signup_event}, labeled "New Signups". Series B: count unique users of {paid_subscription_event} where
      {paid_subscription_event.trial_end} is empty, labeled "New Paying Customers". Series C: count unique users of {subscription_canceled_event},
      labeled "Churned Customers". Series D: sum of {revenue_event.amount} where {revenue_event.type} indicates recurring
      revenue, labeled "Revenue". Series E: computed as Series B minus Series C, labeled "Net New Customers". Series F: trailing
      {dau_window} daily active users counting unique users of {session_start_event}, labeled "Engagement". Each card shows
      the current week value, week-over-week % change, year-over-year % change and a 12-week sparkline. Annotate each card
      with the current week value against the trailing 4-week average and a trend label of accelerating, steady or decelerating.
      Flag any metric that moved more than {wow_alert_threshold}% week-over-week in either direction. Flag any metric moving
      the wrong direction for {durable_trend_weeks} or more consecutive weeks. Add a growth-quality indicator: if Net New
      Customers is rising while Churned Customers is also rising, label it treadmill; if Net New Customers is rising while
      Churned Customers is flat or falling, label it compounding growth.'
---

# Weekly business review

Slash command: /weekly-business-review-summary

## Step 1: Build the Monday scorecard

Create an Insights report called "Weekly Business Review Summary".
This recipe is a multi-series KPI dashboard combining the headline numbers a founder or exec wants to see every Monday morning. Render as a multi-metric scorecard.
Series A: Event "User created", aggregation: Count Unique Users, weekly, label: "New Signups"
Series B: Event "Subscription started" where trial_end is null (paid signup) OR for ecommerce mode "Placed order" where this is the user's first order, aggregation: Count Unique Users, weekly, label: "New Paying Customers"
Series C: Event "Subscription canceled" (saas) OR users whose Users.Last seen exceeds 90 days (ecommerce churn proxy), weekly, label: "Churned Customers"
Series D: Event "Revenue completed" with type indicating recurring revenue (saas) OR Sum of Placed order.total_price (ecommerce), aggregation: Sum of amount or total_price, weekly, label: "Revenue"
Series E: Computed: Net New Customers = Series B − Series C, label: "Net New Customers"
Series F: Trailing 7-day DAU (count of unique users with Session start), label: "Engagement"
Time granularity: Weekly
Time range: Last 12 weeks
Compare: Previous period (prior 12 weeks) AND year-over-year
Chart type: Multi-card scorecard layout: each metric gets a card showing: current week value, week-over-week % change, year-over-year % change, 12-week trend sparkline
Annotations on each card:
- Highlight the current-week value vs. trailing 4-week average (trend indicator: accelerating / steady / decelerating).
- Flag any metric that moved >15% week-over-week in either direction (exec-attention threshold).
- Flag any metric trending wrong-direction for 4+ consecutive weeks (durable trend, not noise).
- Add a quality-of-growth indicator: Net New Customers (E) growing while Churned Customers (C) is also growing = treadmill (high churn offset by acquisition); Net New growing while Churned is flat or shrinking = compounding growth (best-in-class).
Use case: the WBR-fill report. Founders, execs, and operators run a weekly cadence on the same 5-6 numbers. This recipe makes that cadence one-click: automatically populated, automatically annotated, ready to present. Replaces the spreadsheet most teams maintain manually for this purpose.
Taxonomy notes:
- This recipe operates as an aggregator over multiple canonical events. For mode=saas, prioritize subscription/revenue events. For mode=ecommerce, prioritize order events. For mode=all, render both side-by-side.
- The "churn" definition for ecommerce uses Users.Last seen as a proxy because there's no explicit churn event in DTC ecommerce: adjust the threshold (60/90/180 days) per business model.
