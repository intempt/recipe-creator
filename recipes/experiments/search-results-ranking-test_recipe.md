---
name: search-results-ranking-test
description: |
  Use when a user mentions "search results ranking test", or asks for related help. Optimize product search ranking: relevance vs. popularity-weighted vs. margin-weighted. Server experiment with JSON payload controlling search backend.
arguments: []
intempt:
  id: search-results-ranking-test
  version: 1.0.1
  slashCommand: /search-results-ranking-test
  group: Experiments
  title: 'Search ranking test'
  shortDescription: 'Compares ranking search results by text relevance, by sales velocity, or by profit margin, scored on revenue after a search.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [experiences]
    agent: experiment-strategist
    mode: [ecommerce]
    complexity: standard
    executionMode: live
    tags: [experiment, server]
    experimentType: a-b
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_experiment
  procedure:
    - step: 1
      title: 'Set up the ranking test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      description: 'Runs a server experiment on the search_ranking_strategy flag with three rankings: relevance only, relevance weighted by sales velocity, and relevance weighted by profit margin. Only sessions with a real search count. The winner earns the most revenue in the session of a search.'
      prompt: |
        Create a SERVER EXPERIMENT on /experiences titled "Search Ranking Optimization".

        ═══ PATH 1: Top-level configuration ═══

        Experience type: server_experiment

        Flag Key: search_ranking_strategy

        Variants:
        - Control (34%): relevance-based (text match score only)
        - Variant B (33%): popularity-weighted (relevance × sales velocity)
        - Variant C (33%): margin-weighted (relevance × profit margin)

        Targeting:
        - Pages: any page where the search backend is called: typically search results pages (page URL contains "/search") and inline search-as-you-type widgets in the header
        - Devices: any (server-side search is device-agnostic; the ranking algorithm runs in the search backend regardless of client device)
        - Audience: users performing product searches (search query string is non-empty, OR submit_on the search form)
        - Display frequency: always (every search query call invokes getFlag and applies the assigned variant's ranking)

        Primary metric: goal_completed_in_experience where experience_id = <this> AND value > 0 (revenue from order_created within session of a search)
        Secondary metrics:
        - click_on on search results (search-to-click conversion)
        - Average click position (which rank (1, 2, 3) got clicked)
        - Revenue per search (sum of order_created.total_price / count of distinct searches)
        - Zero-result rate (searches where no click_on followed within 30 seconds)

        Guardrail: search-to-purchase conversion (the existing aggregate metric) must not drop >5% in any variant. Note: variant C (margin-weighted) is a known accuracy/profit tradeoff: guardrails catch it if the accuracy drop is too steep.

        Schedule: 21 days, 5,000 searches per variant minimum

        ═══ PATH 2: Variant JSON payload ═══

        Variant: Control (relevance)
          {
            "ranking_strategy": "relevance",
            "weights": {
              "text_match_score": 1.0,
              "popularity": 0.0,
              "margin": 0.0
            },
            "max_results": 24,
            "tie_breaker": "alphabetical"
          }

        Variant: B (popularity-weighted)
          {
            "ranking_strategy": "popularity_weighted",
            "weights": {
              "text_match_score": 0.6,
              "popularity": 0.4,
              "margin": 0.0
            },
            "max_results": 24,
            "tie_breaker": "popularity"
          }

        Variant: C (margin-weighted)
          {
            "ranking_strategy": "margin_weighted",
            "weights": {
              "text_match_score": 0.7,
              "popularity": 0.0,
              "margin": 0.3
            },
            "max_results": 24,
            "tie_breaker": "margin"
          }

        SDK integration:
          const ranking = await intempt.getFlag('search_ranking_strategy', userId);
          const results = await search.query(query, { weights: ranking.weights, max: ranking.max_results });

        Each rendered search result should have target_id = "search-result-{position}" so click_on per-position metrics roll up consistently.

        Taxonomy notes:
        - The search backend (search.query) is application-side and not part of canonical taxonomy.
        - "Click position" is the rank of the clicked result: typically captured as target_id ("search-result-3" to position 3) or as a property on click_on.
        - "Margin" data is required for variant C; if your product catalog doesn't track per-product margin, variant C cannot run faithfully.
        - "Display frequency: always": every search query for a given userId returns the same variant (sticky assignment) for the experiment's duration. The variant is computed once on first search and cached.
  outputs:
    - { name: experiment, type: experiment, cardinality: single, description: "Website experiment created on /experiences." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Search ranking test

Compares ranking search results by text relevance, by sales velocity, or by profit margin, scored on revenue after a search.

## What it does

1. **Set up the ranking test** (`create_experiment`)

   Runs a server experiment on the search_ranking_strategy flag with three rankings: relevance only, relevance weighted by sales velocity, and relevance weighted by profit margin. Only sessions with a real search count. The winner earns the most revenue in the session of a search.

## What you end up with

- **experiment** (experiment): Website experiment created on /experiences.
