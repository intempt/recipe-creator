---
frontmatter_id: search-conversion
slash_command: /search-conversion
description: Shows how many on site searches lead to a click, a cart and an order, and compares that with shoppers who just browse.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Shows how many site searches lead to a click, cart and order, and compares that conversion with shoppers who only
    browse.
  parameters:
  - name: conversion_window
    type: duration
    label: Conversion window
    default: 3 d
    required: false
  - name: comparison_period
    type: duration
    label: Comparison period (prior period)
    default: 3 d
    required: false
  - name: top_query_categories
    type: number
    label: Number of top query categories to break down by
    default: 10
    required: false
  - name: zero_click_window
    type: duration
    label: Window to check for a click after a search
    default: 5 min
    required: false
  - name: zero_click_benchmark
    type: number
    label: Zero-click share benchmark (%)
    default: 10
    required: false
  - name: search_lag_threshold
    type: number
    label: Search lag threshold vs browse (%)
    default: 50
    required: false
  - name: top_missed_terms
    type: number
    label: Number of top zero-engagement query terms to highlight
    default: 5
    required: false
  requirements:
  - slot: search_page_view
    kind: event
    meaning: A customer viewed a page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page viewed
      optional: false
    - name: query
      type: string
      meaning: Search query string on the page URL
      optional: true
  - slot: search_result_click
    kind: event
    meaning: A customer clicked an element on the site
    properties:
    - name: query
      type: string
      meaning: Search query associated with the click
      optional: true
    - name: previous_page
      type: string
      meaning: Page the customer came from before clicking
      optional: true
  - slot: browse_page_view
    kind: event
    meaning: A customer viewed a category or listing page
    properties:
    - name: page_url
      type: string
      meaning: URL of the category or listing page viewed
      optional: false
  - slot: cart_created
    kind: event
    meaning: A customer created a shopping cart
  - slot: order_placed
    kind: event
    meaning: A customer placed an order
  steps:
  - id: s1
    builds: report
    uses:
    - search_page_view
    - search_result_click
    - browse_page_view
    - cart_created
    - order_placed
    - conversion_window
    - comparison_period
    - top_query_categories
    - zero_click_window
    - zero_click_benchmark
    - search_lag_threshold
    - top_missed_terms
    instruction: 'Create a funnel report named "Search to Conversion" with these steps in order: (1) {search_page_view} where
      {search_page_view.page_url} contains "/search" or {search_page_view.query} is not empty, labeled "Performed Search";
      (2) {search_result_click} where {search_result_click.previous_page} indicates the search results page or {search_result_click.query}
      is not empty, labeled "Clicked Result"; (3) {cart_created}, labeled "Added to Cart"; (4) {order_placed}, labeled "Purchased".
      Set the conversion window to {conversion_window}. Break down by query category parsed from {search_page_view.query}
      or {search_result_click.query}, showing the top {top_query_categories} categories. Compare against the previous period
      of {comparison_period}. Show the conversion rate at each step for each query category. Count search page views with
      no {search_result_click} within {zero_click_window}, as zero-engagement searches. Annotate: flag when the share of searches
      with zero clicks exceeds {zero_click_benchmark}%. Flag any query category where search-to-purchase conversion is more
      than {search_lag_threshold}% below browse-to-purchase conversion as a search-relevance issue. Highlight the top {top_missed_terms}
      query terms with high search volume and zero downstream engagement as missed-revenue opportunities. State whether searchers
      convert better than browsers.'
---

# Search to purchase

Slash command: /search-conversion

## Step 1: Follow searches through to orders

Create a Funnel report called "Search to Conversion".
Steps:
1. Event "View page" where Page URL contains /search OR query string is non-empty: "Performed Search"
2. Event "Click on" where the user is in a search-results context (referrer or previous_page indicates the search page): "Clicked Result"
3. Event "Cart created": "Added to Cart"
4. Event "Placed order": "Purchased"
Conversion window: 3 days
Breakdown: By query keyword/category (parse the query string from View page.query or from Click on.query): top 10 query categories
Compare: Previous period (prior 3 days)
Also build a parallel "Browse to Purchase" comparison funnel (View page on category/listing to Cart created to Placed order) so search-conversion can be compared head-to-head with non-search browsing.
For each step, also surface:
- Per-query-category conversion rate at each step
- Volume of search page views with zero subsequent Click on within 5 minutes (zero-result or zero-engagement searches)
Annotations:
- Flag the share of searches that resulted in zero clicks: benchmark <10%.
- Flag any query category where search-to-purchase conversion lags browse-to-purchase by >50% (search-relevance issue).
- Highlight the top 5 query terms with high volume but zero downstream engagement: missed-revenue opportunities.
Surface whether searchers convert better than browsers (typical: 2-3× better).
Taxonomy notes:
- "search_performed" and "search_result_clicked" as standalone events do not exist. Search interactions are derived from View page.Page URL + query string patterns and Click on.query / Click on.previous_page.
- Click on carries query and previous_page properties that are useful for context detection.
