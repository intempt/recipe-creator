---
name: search-conversion
description: |
  Use when a user mentions "search → conversion", or asks for related help. Search-to-purchase funnel using page_viewed.query patterns with no-results surfacing and search-vs-browse comparison.
arguments: []
intempt:
  id: search-conversion
  version: 1.0.0
  slashCommand: /search-conversion
  group: Reports
  shortDescription: "Builds a funnel report tracking user progression from search page views to product clicks, cart additions, and purchases."
  availability: coming-soon
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
      title: "Build Funnel Report"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Funnel report called "Search to Conversion".

        Steps:
        1. Event "page_viewed" where page_url contains /search OR query string is non-empty — "Performed Search"
        2. Event "click_on" where the user is in a search-results context (referrer or previous_page indicates the search page) — "Clicked Result"
        3. Event "cart_created" — "Added to Cart"
        4. Event "order_created" — "Purchased"

        Conversion window: 3 days
        Breakdown: By query keyword/category (parse the query string from page_viewed.query or from click_on.query) — top 10 query categories
        Compare: Previous period (prior 3 days)

        Also build a parallel "Browse to Purchase" comparison funnel (page_viewed on category/listing → cart_created → order_created) so search-conversion can be compared head-to-head with non-search browsing.

        For each step, also surface:
        - Per-query-category conversion rate at each step
        - Volume of search page views with zero subsequent click_on within 5 minutes (zero-result or zero-engagement searches)

        Annotations:
        - Flag the share of searches that resulted in zero clicks — benchmark <10%.
        - Flag any query category where search-to-purchase conversion lags browse-to-purchase by >50% (search-relevance issue).
        - Highlight the top 5 query terms with high volume but zero downstream engagement — missed-revenue opportunities.

        Surface whether searchers convert better than browsers (typical: 2-3× better).

        Taxonomy notes:
        - "search_performed" and "search_result_clicked" as standalone events do not exist. Search interactions are derived from page_viewed.page_url + query string patterns and click_on.query / click_on.previous_page.
        - click_on carries query and previous_page properties that are useful for context detection.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Search → Conversion

## Procedure

1. **Build Funnel Report** [`build_funnel_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Funnel report called "Search to Conversion".

   Steps:
   1. Event "page_viewed" where page_url contains /search OR query string is non-empty — "Performed Search"
   2. Event "click_on" where the user is in a search-results context (referrer or previous_page indicates the search page) — "Clicked Result"
   3. Event "cart_created" — "Added to Cart"
   4. Event "order_created" — "Purchased"

   Conversion window: 3 days
   Breakdown: By query keyword/category (parse the query string from page_viewed.query or from click_on.query) — top 10 query categories
   Compare: Previous period (prior 3 days)

   Also build a parallel "Browse to Purchase" comparison funnel (page_viewed on category/listing → cart_created → order_created) so search-conversion can be compared head-to-head with non-search browsing.

   For each step, also surface:
   - Per-query-category conversion rate at each step
   - Volume of search page views with zero subsequent click_on within 5 minutes (zero-result or zero-engagement searches)

   Annotations:
   - Flag the share of searches that resulted in zero clicks — benchmark <10%.
   - Flag any query category where search-to-purchase conversion lags browse-to-purchase by >50% (search-relevance issue).
   - Highlight the top 5 query terms with high volume but zero downstream engagement — missed-revenue opportunities.

   Surface whether searchers convert better than browsers (typical: 2-3× better).

   Taxonomy notes:
   - "search_performed" and "search_result_clicked" as standalone events do not exist. Search interactions are derived from page_viewed.page_url + query string patterns and click_on.query / click_on.previous_page.
   - click_on carries query and previous_page properties that are useful for context detection.
   ```
