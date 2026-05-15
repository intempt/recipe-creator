# Intempt Recipes

Pre-built automation recipes for the Intempt platform. Each recipe is a structured `.md` file with YAML frontmatter that Blu (Intempt's AI) uses to execute multi-step workflows on behalf of users.

**256 recipes** across **10 categories**, covering segments, reports, journeys, workflows, experiments, dashboards, personalizations, meetings, agents, and recommendations.

## Categories

| Category | Count | Description |
|----------|------:|-------------|
| **reports** | 71 | Insights, funnel, retention, and path analysis |
| **segments** | 47 | Dynamic audience cohorts (accounts, users, leads) |
| **workflows** | 38 | Triggered automation, enrichment, and routing |
| **journeys** | 35 | Multi-step lifecycle playbooks |
| **experiments** | 24 | A/B and multivariate tests |
| **dashboards** | 21 | Persona-specific dashboard compositions |
| **personalizations** | 9 | Audience-targeted website experiences |
| **meetings** | 9 | Notetaker setup, taxonomy, summaries, coaching |
| **agents** | 1 | Customer-facing AI agent configuration |
| **recommendations** | 1 | Catalog-aware product/content recs |

## Business Modes

Recipes are tagged by the business model they apply to:

- **SaaS** — 68 recipes
- **B2B + SaaS** — 65 recipes
- **Ecommerce** — 60 recipes
- **B2B** — 28 recipes
- **All modes** — 14 recipes
- **Cross-mode** — 21 recipes

## AI Agents

Each recipe is assigned to an AI agent that executes it:

| Agent | Recipes | Focus |
|-------|--------:|-------|
| data-analyst | 90 | Reports, dashboards, analytics |
| segment-architect | 46 | Audience segmentation |
| experiment-strategist | 32 | A/B tests, experiments |
| journey-builder | 31 | Lifecycle journeys |
| revops-automator | 25 | Revenue operations workflows |
| workflow-builder | 12 | General automation |
| meeting-notetaker | 12 | Meeting intelligence |
| experience-optimizer | 4 | Personalizations |
| scheduling-assistant | 2 | Meeting scheduling |
| outreach-rep | 2 | Sales outreach |

## Recipe Format

Each recipe is a markdown file with YAML frontmatter:

```yaml
---
name: recipe-name
description: |
  Use when a user mentions "X", or asks for related help.
arguments: []
intempt:
  id: recipe-slug
  version: 1.0.0
  slashCommand: /recipe-slug
  group: Segments
  shortDescription: "..."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [b2b, saas]
    complexity: standard        # quick | standard | advanced
    executionMode: live         # oneshot | live | scheduled
    tags: [tag1, tag2]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:                # optional
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
      description: "What this step does."
      prompt: |
        Detailed prompt for the AI agent.
  outputs:
    - { name: segment, type: segment, cardinality: single }
---

# Human-readable description
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `classification.mode` | Business model fit (b2b, saas, ecommerce) |
| `classification.complexity` | quick (71), standard (129), advanced (56) |
| `classification.executionMode` | live (253), oneshot (2), scheduled (1) |
| `prerequisites` | Required events or integrations (blocking/recommended) |
| `procedure` | Ordered steps with commands, bindings, and prompts |
| `outputs` | What the recipe produces (segment, journey, report, etc.) |

## Ingestion

Recipes are loaded into the platform via the single-metadata service:

```
POST /v1/{org}/projects/{project}/recipes/bundles      # ZIP of .md files
POST /v1/{org}/projects/{project}/recipes/ingest-md     # Single .md file
```

## Repo Structure

```
recipes/
  agents/              — 1 recipe
  dashboards/          — 21 recipes
  experiments/         — 24 recipes
  journeys/            — 35 recipes
  meetings/            — 9 recipes
  personalizations/    — 9 recipes
  recommendations/     — 1 recipe
  reports/             — 71 recipes
  segments/            — 47 recipes
  workflows/           — 38 recipes
recipes-catalog.xlsx   — Full catalog with taxonomy and mode coverage
scripts/
  convert_ts_to_md.py  — Converts from consolev2-loveable TS format
```
