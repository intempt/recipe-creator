---
frontmatter_id: browse-to-buy-retention
slash_command: /browse-to-buy-retention
description: Measures how long first time visitors take to place an order, by acquisition source, so you can tell fast converting channels from slow ones.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
---

# Browse to buy retention

Slash command: /browse-to-buy-retention

## Step 1: Track first visit to first order

Create a Retention report called "Browse to Buy Retention".
Anchor event: Session start (each user's first Session start)
Return event: Placed order
Cohort granularity: Weekly
Time range: Last 12 weeks
Breakdown: By Users.UTM source (top 6 sources)
Compare: Previous period (prior 12 weeks of cohorts)
Chart type: Retention curve plus cohort table with W1 / W2 / W4 / W8 / W12 columns
Annotations:
- Add benchmarks: W1 first-purchase rate of 5% is typical for considered-purchase DTC, 10%+ for impulse-buy.
- Flag any source where W12 first-purchase rate is below 8% (browse-to-buy gap).
- Highlight the source with the fastest first-purchase rate (steepest W1 conversion).
- Highlight the source with the highest W12 conversion (best overall, even if slower).
Surface which sources produce "fast converters" vs "slow converters."
Taxonomy notes:
- Session start and Placed order are canonical. Users.UTM source is canonical.
- "first session" per-user is determined by the earliest Session start for that customer_id.
