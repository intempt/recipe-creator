---
frontmatter_id: post-purchase-second-order-velocity
slash_command: /post-purchase-second-order-velocity
description: Measure the time from a customer's first order to their second order. Use the median and conversion percentages to guide when to send replenishment reminders.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how long customers take from their first order to their second, by product category, so replenishment reminders
    can be timed to the typical gap and compared across periods.
  parameters:
  - name: first_order_min_age
    type: duration
    label: Minimum age of first order (cohort must have full follow-up window)
    default: 6 mo
    required: false
  - name: comparison_window_start
    type: duration
    label: Comparison cohort first order age, start (months ago)
    default: 18 mo
    required: false
  - name: comparison_window_end
    type: duration
    label: Comparison cohort first order age, end (months ago)
    default: 12 mo
    required: false
  - name: top_categories
    type: number
    label: Number of top first-order categories to break down by
    default: 6
    required: false
  - name: early_loyalty_window
    type: duration
    label: Early loyalty window (days from first to second order)
    default: 30 d
    required: false
  - name: high_velocity_threshold
    type: duration
    label: High-velocity median threshold (flag categories below this)
    default: 14 d
    required: false
  - name: long_cycle_threshold
    type: duration
    label: Long-cycle median threshold (flag categories above this)
    default: 180 d
    required: false
  requirements:
  - slot: placed_order_event
    kind: event
    meaning: A customer placed an order
    properties:
    - name: items
      type: text
      meaning: Products included in the order; each product_id resolves to a category
      optional: false
  - slot: product_category_catalog
    kind: product_feed
    meaning: Product catalog that maps each product to its category
  - slot: time_to_second_purchase_report
    kind: segment
    meaning: Report showing the distribution of days between a customer's first and second order
    optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - placed_order_event
    - product_category_catalog
    - first_order_min_age
    - comparison_window_start
    - comparison_window_end
    - top_categories
    - early_loyalty_window
    - high_velocity_threshold
    - long_cycle_threshold
    instruction: 'Create an Insights report named "Time from 1st to 2nd Purchase". Use {placed_order_event} events. Series
      A: histogram of days between each customer''s first and second order, counted only for customers with at least two orders,
      bucketed 0-3, 4-7, 8-14, 15-30, 31-60, 61-90, 91-180, 181-365, and 365+ days. Series B: cumulative percentage of repeat
      buyers whose second order occurs within X days. Time range: customers whose first order is at least {first_order_min_age}
      old. Breakdown: category of the first placed order''s items, resolved through {product_category_catalog}, top {top_categories}
      categories. Compare against the cohort whose first order was between {comparison_window_start} and {comparison_window_end}
      ago to see whether repeat velocity is getting faster or slower. Chart type: histogram with the cumulative percentage
      as a secondary line. Annotations: highlight the median days to second purchase per category as the suggested replenishment
      trigger delay; flag categories with median below {high_velocity_threshold} as high-velocity replenishment candidates
      for subscribe-and-save; flag categories with median above {long_cycle_threshold} as long-cycle categories where replenishment
      should fire at 6-9 months; highlight the share of repeat buyers who returned within {early_loyalty_window} and note
      whether that share is rising or falling across cohorts.'
---

# Time to second purchase

Slash command: /post-purchase-second-order-velocity

## Step 1: Measure the gap to order two

Create an Insights report called "Time from 1st to 2nd Purchase".
Series A: Distribution histogram of days between each user's 1st Placed order and 2nd Placed order (only users who have at least 2 orders)
Series B: Cumulative percentage: what % of repeat-buyers make their 2nd purchase within X days
Buckets for Series A: 0-3 days / 4-7 days / 8-14 days / 15-30 days / 31-60 days / 61-90 days / 91-180 days / 181-365 days / 365+ days
Time range: Users whose 1st order was 6+ months ago (so we have a full follow-up window for measuring 2nd-purchase timing)
Breakdown: By first-order product category (derived from first Placed order.items to Products.category): top 6 categories
Compare: Previous period (cohorts whose 1st order was 12-18 months ago: answers: is repeat-velocity getting faster or slower?)
Chart type: Histogram chart with the cumulative % overlay as a secondary line
Annotations:
- Highlight the median time-to-second-purchase per category: this is the right delay to set on replenishment journey triggers.
- Flag any category where median time-to-second-purchase is <14 days (high-velocity replenishment: candidate for subscribe-and-save offering).
- Flag any category where median time-to-second-purchase is >180 days (long-cycle category: replenishment journeys should fire at 6-9 months, not 30 days).
- Highlight the share of repeat-buyers who returned within 30 days (the "early loyalty" group). This share growing over time = improving retention; shrinking = deteriorating.
Use case: distinct from the existing purchase-retention recipe (which is cohort %). This is the histogram that tells you the actual time distribution: critical for journey-trigger timing. Most brands use a generic 30-day or 60-day replenishment delay; this recipe surfaces the right delay per category.
Taxonomy notes:
- "First order" and "second order" per user are derived from the temporal order of Placed order events for the same customer_id.
- Placed order.items contains product_id which resolves to category via the Products record-object.
