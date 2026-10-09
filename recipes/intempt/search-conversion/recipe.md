---
description: Shows how many on site searches lead to a click, a cart and an order, and compares that with shoppers who just browse.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ecommerce
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
