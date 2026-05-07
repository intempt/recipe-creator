# CLAUDE.md

## Overview

Public recipes repository for the Intempt GrowthOS platform. Contains 307 recipe `.md` files with YAML frontmatter, organized by product category.

## Structure

```
recipes/
  analytics/       # 6 recipes — health scores, engagement analysis
  dashboards/      # 18 recipes — executive, funnel, retention dashboards
  experiences/     # 34 recipes — personalization, A/B tests
  marketing/       # 73 recipes — journeys, campaigns, cart recovery
  reports/         # 69 recipes — cohort, funnel, revenue reports
  sales/           # 60 recipes — deals, accounts, outreach
  segments/        # 47 recipes — customer segmentation rules
scripts/
  convert_ts_to_md.py  # Conversion from consolev2-loveable TS format
```

## Recipe .md Format

Each recipe is a markdown file with YAML frontmatter compatible with `RecipeMdParser` in single-metadata:

```yaml
---
name: Recipe Name
description: Short description
intempt:
  id: recipe-slug                    # kebab-case, unique
  version: 1.0.0                     # semver
  slashCommand: /recipe-slug
  shortDescription: ...
  author:
    type: intempt
    name: Intempt
  classification:
    product: [segments]              # product categories
    agent: segment-architect         # AI agent type
    mode: [b2b, saas]               # business modes
    complexity: standard             # quick | standard | advanced
    executionMode: live              # oneshot | live | scheduled
    tags: [tag1, tag2]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  outputs:
    - name: segment
      type: segment
      description: What this output creates
  steps:
    - id: step-id
      describe: What this step does
      produces: output-name
  prerequisites:                     # optional
    integrations:
      - value: shopify
        severity: blocking
---
# Markdown body with human-readable description
```

## Ingestion

Recipes are ingested into single-metadata via:
- `POST /v1/{org}/projects/{project}/recipes/bundles` — ZIP of .md files
- `POST /v1/{org}/projects/{project}/recipes/ingest-md` — single .md file

## Output Types

16 output types across recipes: segment, journey, workflow, content, dashboard, report, experiment, experience, attribute, event-mapping, task, deal, account, meeting, agent-config, snippet.
