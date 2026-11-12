---
frontmatter_id: active-vs-passive-users
slash_command: /active-vs-passive-users
description: Classifies each user with custom multi-threshold rules on their event activity, and outputs a report for segmenting active and passive users.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Classifies each user as Producer, Consumer, Lurker or Inactive from 30-day event activity and builds a weekly report
    showing how active users split across these groups, with revenue concentration.
  parameters:
  - name: producer_click_min
    type: number
    label: Minimum Click on events for Producer
    default: 10
    required: false
  - name: producer_submit_min
    type: number
    label: Minimum Submit on events for Producer
    default: 1
    required: false
  - name: consumer_session_min
    type: number
    label: Minimum Session start events for Consumer
    default: 3
    required: false
  - name: consumer_view_min
    type: number
    label: Minimum View page events for Consumer
    default: 10
    required: false
  - name: consumer_click_max
    type: number
    label: Click on events must be below this for Consumer
    default: 5
    required: false
  - name: lurker_session_min
    type: number
    label: Minimum Session start events for Lurker
    default: 1
    required: false
  - name: classification_window
    type: duration
    label: Trailing window for classification
    default: 30 d
    required: false
  - name: report_time_range
    type: duration
    label: Report time range
    default: 12 w
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (prior)
    default: 12 w
    required: false
  - name: producer_share_low
    type: number
    label: Producer share below which the product leans consumer (%)
    default: 15
    required: false
  - name: revenue_concentration_threshold
    type: number
    label: Producer revenue share above which power-user risk is flagged (%)
    default: 70
    required: false
  requirements:
  - slot: click_event
    kind: event
    meaning: A customer clicked on something in the product or site
  - slot: submit_event
    kind: event
    meaning: A customer submitted an action such as a form submission
  - slot: view_page_event
    kind: event
    meaning: A customer viewed a page
  - slot: session_start_event
    kind: event
    meaning: A customer started a session
  - slot: subscription_started_event
    kind: event
    meaning: A customer started a subscription
    properties:
    - name: amount
      type: number
      meaning: Subscription amount charged
      optional: false
    - name: plan
      type: string
      meaning: Plan the subscription belongs to
      optional: true
    optional: true
  - slot: revenue_completed_event
    kind: event
    meaning: A customer completed a revenue-generating purchase
    properties:
    - name: amount
      type: number
      meaning: Revenue amount of the completed purchase
      optional: false
    optional: true
  - slot: user_plan_attribute
    kind: attribute
    meaning: The subscription plan tier a user is on, taken from their most recent active subscription
  steps:
  - id: s1
    builds: report
    uses:
    - click_event
    - submit_event
    - view_page_event
    - session_start_event
    - subscription_started_event
    - revenue_completed_event
    - user_plan_attribute
    - producer_click_min
    - producer_submit_min
    - consumer_session_min
    - consumer_view_min
    - consumer_click_max
    - lurker_session_min
    - classification_window
    - report_time_range
    - comparison_period
    - producer_share_low
    - revenue_concentration_threshold
    instruction: 'Create an Insights report titled "Active vs. Passive Users". Classify each user using activity over the
      trailing {classification_window}: Producer if the user has at least {producer_click_min} {click_event} events and at
      least {producer_submit_min} {submit_event} events; Consumer if the user has at least {consumer_session_min} {session_start_event}
      events and at least {consumer_view_min} {view_page_event} events but fewer than {consumer_click_max} {click_event} events;
      Lurker if the user has at least {lurker_session_min} {session_start_event} event in the window but meets neither the
      Producer nor Consumer rule; Inactive if the user has zero {session_start_event} events in the window. Series A: count
      unique users per bucket, weekly granularity. Series B: share of total active users (excluding Inactive) per bucket,
      as a percentage. Series C: sum of {subscription_started_event.amount} or {revenue_completed_event.amount} per bucket
      to show revenue concentration. Use a weekly snapshot over the last {report_time_range}, broken down by {user_plan_attribute}
      (the plan from each user''s most recent active subscription), and compare against the prior {comparison_period}. Show
      a stacked area chart for the weekly distribution plus a secondary view of revenue concentration per bucket. Annotations:
      flag if Producer share is below {producer_share_low}% (product leans consumer, engagement risk); flag if Producer share
      declines week over week (engagement erosion, leading indicator of churn); highlight the Consumer-to-Producer migration
      rate, meaning the percentage of users classified Consumer last week who are Producers this week; flag if Producers are
      under 20% of users but above {revenue_concentration_threshold}% of revenue (power-user risk); flag any plan tier where
      Producer share is materially lower than other tiers (acquiring lurkers, pricing or positioning issue). For reference,
      healthy distributions are roughly Producers 20-40%, Consumers 40-60%, Lurkers 10-20% of active users.'
---

# Active versus passive users

Slash command: /active-vs-passive-users

## Step 1: Split users by what they do

Create an Insights report called "Active vs. Passive Users".
Per-user classification computed from the trailing 30-day window:
 - Producer: emitted ≥10 Click on events AND ≥1 Submit on (taking actions, creating, configuring)
 - Consumer: emitted ≥3 Session start AND ≥10 View page BUT <5 Click on (browsing, reading, but not creating)
 - Lurker: emitted ≥1 Session start in the last 30 days BUT below both thresholds above (logging in but barely engaging)
 - Inactive: zero Session start in the last 30 days
Series A: Count Unique Users per classification bucket, time granularity: Weekly
Series B: Computed: share of total active users (excluding Inactive) per bucket, unit: %
Series C: Sum of Subscription started.amount or Revenue completed.amount per bucket: surfaces revenue concentration
Time granularity: Weekly snapshot
Time range: Last 12 weeks
Breakdown: By Plan (resolved from each user's most-recent active Subscription started)
Compare: Previous period (prior 12 weeks)
Chart type: Stacked area chart for the weekly distribution, with a secondary view showing revenue concentration per bucket
Annotations:
- Add the classic distribution: in healthy products, Producers should be 20-40% of active users, Consumers 40-60%, Lurkers 10-20%. If Producers are <15%, the product is "leaning consumer": engagement risk.
- Flag if the Producer share is shrinking week-over-week (engagement erosion: leading indicator of churn before retention metrics catch it).
- Highlight Consumer-to-Producer migration rate: of users classified as Consumer last week, what % became Producers this week? This is the latent activation rate.
- Surface revenue concentration: in many SaaS products, Producers generate disproportionate revenue. If Producers are <20% of users but >70% of revenue, you have a "power user" risk: losing one Producer hurts more than losing 10 Lurkers.
- Flag any plan tier where Producer share is materially lower than other tiers (the plan is acquiring lurkers: pricing/positioning issue).
Use case: most engagement reports just count "active users." This recipe surfaces the hidden segment of "active but passive": users who log in regularly but never DO anything. They look retained but are pre-churn. Catching them before they go inactive is high-leverage.
Taxonomy notes:
- Click on, Submit on, View page, Session start are all canonical. Submit on is specifically the "user took an action" canonical event (form submissions, etc.).
- The classification thresholds are configurable per workspace.
