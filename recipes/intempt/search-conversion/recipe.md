---
frontmatter_id: search-conversion
slash_command: /search-conversion
description: Emails a weekly digest of how many on site searches lead to a click, a cart and an order, compared with shoppers
  who just browse.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ecommerce-retail
portable:
  summary: Emails a weekly digest of site searches leading to a click, cart and order, compared with browse conversion, with
    zero-click and missed-term flags.
  parameters:
  - name: comparison_period
    type: duration
    label: Period compared with the one before
    default: 7 d
    required: false
  - name: conversion_window
    type: duration
    label: Conversion window
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
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
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
    builds: automation
    uses:
    - search_page_view
    - search_result_click
    - browse_page_view
    - cart_created
    - order_placed
    - comparison_period
    - conversion_window
    - top_query_categories
    - zero_click_window
    - zero_click_benchmark
    - search_lag_threshold
    - top_missed_terms
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last {comparison_period}
      against the {comparison_period} before. Searchers did {search_page_view} with {search_page_view.page_url} containing
      "/search" or {search_page_view.query} not empty; browsers did {browse_page_view} and no search. It writes: searchers
      who then did {search_result_click} with {search_result_click.query} not empty or {search_result_click.previous_page}
      a search page, {cart_created}, and {order_placed}, each within {conversion_window}, with the step conversion %, split
      by the top {top_query_categories} query categories; browse-to-order conversion %; the % of searches with no {search_result_click}
      within {zero_click_window}; the top {top_missed_terms} queries by volume with no click. Then it emails these figures
      as plain-text lines, each with its window, to {digest_recipients}. The email flags a zero-click share above {zero_click_benchmark}%
      and query categories whose search-to-order conversion is more than {search_lag_threshold}% below browse-to-order. Nothing
      else is sent.'
---

# Search to purchase

Slash command: /search-conversion

## Step 1: Email the weekly search conversion digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes the last 7 d against the 7 d before. Searchers did search page view with page url containing "/search" or query not empty; browsers did browse page view and no search. It writes: searchers who then did search result click with query not empty or previous page a search page, cart created, and order placed, each within 3 d, with the step conversion %, split by the top 10 query categories; browse-to-order conversion %; the % of searches with no search result click within 5 min; the top 5 queries by volume with no click. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email flags a zero-click share above 10% and query categories whose search-to-order conversion is more than 50% below browse-to-order. Nothing else is sent.
