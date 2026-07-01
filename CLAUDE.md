# CLAUDE.md

## Overview

Public recipes repository for the Intempt platform. Contains 292 recipe `.md` files with YAML frontmatter, organized by Blu Group.

## Structure

```
recipes/
  agents/            #  1 recipe  — customer-facing AI agent setup
  content/           #  4 recipes — channel content (email, SMS, push, site)
  creative/          # 32 recipes — image + video creative ops (pack-shot, on-model, remix, ad, video reel, etc.)
  dashboards/        # 21 recipes — persona-specific dashboard composition
  experiments/       # 24 recipes — A/B / multivariate tests
  journeys/          # 35 recipes — multi-step lifecycle playbooks
  meetings/          #  9 recipes — notetaker, taxonomy, summaries, coaching
  personalizations/  #  9 recipes — audience-targeted website personalization
  recommendations/   #  1 recipe  — catalog-aware product/content recs
  reports/           # 71 recipes — insights, funnel, retention, paths
  segments/          # 47 recipes — dynamic audience cohorts
  workflows/         # 38 recipes — triggered automation, enrichment, routing
recipes-catalog.xlsx   # Full catalog with taxonomy, commands, mode coverage
scripts/
  convert_ts_to_md.py  # Conversion from consolev2-loveable TS format
```

## Recipe .md Format

Each recipe is a markdown file with YAML frontmatter compatible with `RecipeMdParser` in single-metadata:

```yaml
---
name: recipe-name
description: |
  Use when a user mentions "X", or asks for related help. Short description.
arguments: []
intempt:
  id: recipe-slug                    # kebab-case, unique
  version: 1.0.0                     # semver
  slashCommand: /recipe-slug
  group: Segments                    # Blu Group (directory name)
  shortDescription: "..."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]              # product categories
    agent: segment-architect         # AI agent type
    mode: [b2b, saas]               # business modes
    object: accounts                 # optional: target object
    complexity: standard             # quick | standard | advanced
    executionMode: live              # oneshot | live | scheduled
    tags: [tag1, tag2]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:                     # optional
    events:
      - { value: event_name, severity: blocking }
    integrations:
      - { value: shopify, severity: blocking }
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: "Step Title"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn: []                  # optional: refs to prior bindsAs values
      description: "What this step does."
      prompt: |
        Detailed prompt for the AI agent executing this step.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "What this output creates." }
---
# Markdown body with human-readable description
```

## Ingestion

Recipes are ingested into single-metadata via:
- `POST /v1/{org}/projects/{project}/recipes/bundles` — ZIP of .md files
- `POST /v1/{org}/projects/{project}/recipes/ingest-md` — single .md file

## Output Types

Output types across recipes: segment, journey, workflow, content, dashboard, report, experiment, experience, attribute, event-mapping, task, deal, account, meeting, meeting_type, meeting_summary_recipe, meeting_type_inventory, agent-config, snippet, recommendation, image, video.
