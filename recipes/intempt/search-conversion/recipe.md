---
id: search-conversion
title: Search to purchase
slash_command: /search-conversion
group: Reports
owner: intempt
curator: aman
summary: Shows how many on site searches lead to a click, a cart and an order, and compares that with
  shoppers who just browse.
description: >-
  Search-to-purchase funnel using page_viewed.query patterns with no-results surfacing and search-vs-browse
  comparison.
version: 2.0.0
classification:
  product:
    - analytics
  agent: data-analyst
  mode:
    - ecommerce
  industry:
    - ecommerce
  vertical: []
  complexity: quick
  executionMode: live
  tags:
    - funnel
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Follow searches through to orders"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Follow searches through to orders
    summary: >-
      A four step funnel over 3 days from a search to a result click, a cart and an order, split by the
      top 10 query categories and set against a parallel browse funnel. Flags searches that get no clicks
      and query types converting far below browsing.
    builds: report
    description: |-
      Create a Funnel report called "Search to Conversion".
      Steps:
      1. Event "page_viewed" where page_url contains /search OR query string is non-empty: "Performed Search"
      2. Event "click_on" where the user is in a search-results context (referrer or previous_page indicates the search page): "Clicked Result"
      3. Event "cart_created": "Added to Cart"
      4. Event "order_created": "Purchased"
      Conversion window: 3 days
      Breakdown: By query keyword/category (parse the query string from page_viewed.query or from click_on.query): top 10 query categories
      Compare: Previous period (prior 3 days)
      Also build a parallel "Browse to Purchase" comparison funnel (page_viewed on category/listing to cart_created to order_created) so search-conversion can be compared head-to-head with non-search browsing.
      For each step, also surface:
      - Per-query-category conversion rate at each step
      - Volume of search page views with zero subsequent click_on within 5 minutes (zero-result or zero-engagement searches)
      Annotations:
      - Flag the share of searches that resulted in zero clicks: benchmark <10%.
      - Flag any query category where search-to-purchase conversion lags browse-to-purchase by >50% (search-relevance issue).
      - Highlight the top 5 query terms with high volume but zero downstream engagement: missed-revenue opportunities.
      Surface whether searchers convert better than browsers (typical: 2-3× better).
      Taxonomy notes:
      - "search_performed" and "search_result_clicked" as standalone events do not exist. Search interactions are derived from page_viewed.page_url + query string patterns and click_on.query / click_on.previous_page.
      - click_on carries query and previous_page properties that are useful for context detection.
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Search to purchase

Shows how many on site searches lead to a click, a cart and an order, and compares that with shoppers who just browse.

## Steps

1. **Follow searches through to orders** (builds report)

   A four step funnel over 3 days from a search to a result click, a cart and an order, split by the top 10 query categories and set against a parallel browse funnel. Flags searches that get no clicks and query types converting far below browsing.

## What you end up with

- **report** (report): Report produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Follow searches through to orders"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build report.
