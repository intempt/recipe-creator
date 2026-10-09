---
name: search-conversion
description: |
  Use when a user mentions "search to conversion", or asks for related help. Search-to-purchase funnel built from page view and search query patterns, with no-results surfacing and search-vs-browse comparison.
arguments: []
intempt:
  id: search-conversion
  version: 1.0.0
  slashCommand: /search-conversion
  group: Reports
  title: "Search to purchase"
  shortDescription: "Shows how many on site searches lead to a click, a cart and an order, and compares that with shoppers who just browse."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [ecommerce]
    complexity: quick
    executionMode: live
    tags: [funnel]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
  procedure:
    - step: 1
      title: "Follow searches through to orders"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "A four step funnel over 3 days from a search to a result click, a cart and an order, split by the top 10 query categories and set against a parallel browse funnel. Flags searches that get no clicks and query types converting far below browsing."
      prompt: |
        Create a Funnel report called "Search to Conversion".

        Steps:
        1. Event "View page" where the page URL contains /search OR the query string is non-empty: "Performed Search"
        2. Event "Click on" where the user is in a search-results context (the referrer or previous page indicates the search page): "Clicked Result"
        3. Event "Cart created": "Added to Cart"
        4. Event "Placed order": "Purchased"

        Conversion window: 3 days
        Breakdown: By query keyword/category (parse the query string from the page view or the click): top 10 query categories
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
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Search to purchase

Shows how many on site searches lead to a click, a cart and an order, and compares that with shoppers who just browse.

## What it does

1. **Follow searches through to orders** (`build_funnel_report`)

   A four step funnel over 3 days from a search to a result click, a cart and an order, split by the top 10 query categories and set against a parallel browse funnel. Flags searches that get no clicks and query types converting far below browsing.

## What you end up with

- **report** (report): Report produced by this recipe.
