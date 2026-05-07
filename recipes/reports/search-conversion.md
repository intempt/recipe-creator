---
name: Search Conversion
description: Search-to-purchase funnel using page_viewed.query patterns with no-results surfacing and search-vs-browse comparison.
intempt:
  id: search-conversion
  version: 1.0.0
  slashCommand: /search-conversion
  shortDescription: Search-to-purchase funnel using page_viewed.query patterns with no-results surfacing and search-vs-browse
    comparison.
  author:
    type: intempt
    name: Intempt
  classification:
    product:
    - analytics
    agent: data-analyst
    mode:
    - ecommerce
    complexity: quick
    executionMode: live
    tags:
    - funnel
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
  - name: report
    type: report
    description: Report produced by this recipe.
  steps:
  - id: build-funnel-report
    describe: Configure and materialize the report described below.
    produces: report
---

# Search Conversion

Search-to-purchase funnel using page_viewed.query patterns with no-results surfacing and search-vs-browse comparison.

## Outputs

- **report** (report): Report produced by this recipe.

## Steps

1. Configure and materialize the report described below.
