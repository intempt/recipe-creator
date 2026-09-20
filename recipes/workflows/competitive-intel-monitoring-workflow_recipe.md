---
name: competitive-intel-monitoring-workflow
description: Use when a user mentions "competitive intel monitoring workflow", "competitor monitoring", "weekly competitive intel", or asks for related help. Weekly scheduled AI agent monitors competitor websites, review sites, social, and news for material moves (pricing change, feature launch, big customer win, leadership change). Summarizes into a structured competitive intel briefing posted to Slack for product + sales teams.
arguments: []
intempt:
  id: competitive-intel-monitoring-workflow
  title: "Weekly competitive intel briefing"
  version: 1.0.0
  slashCommand: /competitive-intel-monitoring-workflow
  group: Workflows
  shortDescription: "Checks your competitors' pricing, features, blog, changelog, hiring and reviews every Monday and posts what actually changed to Slack."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [competitive-intelligence, scheduled-research, ai-monitoring]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_workflow
    - configure_workflow_wait_until_step
    - configure_loop_step
    - configure_web_scrape_step
    - configure_ai_research_step
    - configure_write_with_ai_step
    - configure_slack_step
    - publish_workflow
  procedure:
    - step: 1
      title: "Replace the Monday check"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Runs every Monday morning and produces a briefing product and sales can read in three minutes, instead of somebody manually checking what competitors did."
      prompt: 'Create a workflow ''Weekly competitive intel'' scheduled to run every Monday morning. Goal: replace the manual ''check what competitors did this week'' task with a structured AI-generated briefing the product and sales teams can consume in 3 minutes.'
    - step: 2
      title: "Run it Monday at 7am"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: "Scheduled weekly in local time, skipped if the workspace is paused or no competitors are configured, and it only fetches what has appeared since the last run."
      prompt: 'Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run.'
    - step: 3
      title: "Go through each competitor"
      command: configure_loop_step
      produces: step
      bindsAs: loop
      dependsOn:
      - workflow
      - schedule
      description: "Loops the three to seven competitor domains you configure, running the scrape and the analysis for each, with a pause between them to stay polite to the sources."
      prompt: Configure loop step that iterates over a configured list of competitor domains (configurable per workspace, typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze steps. Rate-limit between iterations to be polite to sources.
    - step: 4
      title: "Read their public pages"
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      - loop
      description: "Pricing, product and feature pages, the last seven days of blog posts, the changelog, the careers page for hiring signals, review site summaries and recent press releases. It honours robots.txt and caches anything unchanged."
      prompt: 'Configure web scrape step for each competitor: pricing page, product/features pages, blog (last 7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary, recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content.'
    - step: 5
      title: "Compare against last week"
      command: configure_ai_research_step
      produces: step
      bindsAs: analyze
      dependsOn:
      - workflow
      - scrape
      description: "This week's content is set against last week's snapshot and only material changes are kept: price moves, new features, leadership changes, big customer wins, shifts in review sentiment, and hiring that points at a new product area. Per competitor it says what changed, what did not, and what to watch."
      prompt: 'Configure AI research step that compares this week''s scraped content to last week''s snapshot and flags material changes. Material = pricing changes, new features announced, leadership changes from careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed, what didn''t, what to watch.'
    - step: 6
      title: "Write the briefing"
      command: configure_write_with_ai_step
      produces: step
      bindsAs: briefing
      dependsOn:
      - workflow
      - analyze
      description: "One document: the three most significant moves of the week, the highlights per competitor, what to watch next week, and what you might do about it. Factual and scannable."
      prompt: 'Configure AI write step that consolidates per-competitor findings into a single weekly briefing. Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c) Watch-list for next week (developing stories), (d) Recommended responses (e.g. ''Competitor X just launched [feature]: our differentiator is still Y; product marketing may want to update positioning''). Tone: factual, concise, scannable.'
    - step: 7
      title: "Post it to the channel"
      command: configure_slack_step
      produces: step
      bindsAs: post
      dependsOn:
      - workflow
      - briefing
      description: "The briefing goes to your competitive intel channel, laid out in sections with links back to the sources and a thread for discussion. Product and marketing leads are tagged on the big moves."
      prompt: 'Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel). Format: rich block layout with sections, links to source pages, and a thread for team discussion. Tag product + marketing leads for major moves.'
    - step: 8
      title: "Publish and spot check it"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - post
      description: "Validated and published, with weekly delivery watched so it cannot fail silently, engagement in the channel, and an occasional human check that the changes it called material really were."
      prompt: 'Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material changes).'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Weekly competitive intel briefing

Checks your competitors' pricing, features, blog, changelog, hiring and reviews every Monday and posts what actually changed to Slack.

## Before you run it

- Connect slack

## What it does

1. **Replace the Monday check** (`create_workflow`)

   Runs every Monday morning and produces a briefing product and sales can read in three minutes, instead of somebody manually checking what competitors did.

2. **Run it Monday at 7am** (`configure_workflow_wait_until_step`)

   Scheduled weekly in local time, skipped if the workspace is paused or no competitors are configured, and it only fetches what has appeared since the last run.

3. **Go through each competitor** (`configure_loop_step`)

   Loops the three to seven competitor domains you configure, running the scrape and the analysis for each, with a pause between them to stay polite to the sources.

4. **Read their public pages** (`configure_web_scrape_step`)

   Pricing, product and feature pages, the last seven days of blog posts, the changelog, the careers page for hiring signals, review site summaries and recent press releases. It honours robots.txt and caches anything unchanged.

5. **Compare against last week** (`configure_ai_research_step`)

   This week's content is set against last week's snapshot and only material changes are kept: price moves, new features, leadership changes, big customer wins, shifts in review sentiment, and hiring that points at a new product area. Per competitor it says what changed, what did not, and what to watch.

6. **Write the briefing** (`configure_write_with_ai_step`)

   One document: the three most significant moves of the week, the highlights per competitor, what to watch next week, and what you might do about it. Factual and scannable.

7. **Post it to the channel** (`configure_slack_step`)

   The briefing goes to your competitive intel channel, laid out in sections with links back to the sources and a thread for discussion. Product and marketing leads are tagged on the big moves.

8. **Publish and spot check it** (`publish_workflow`)

   Validated and published, with weekly delivery watched so it cannot fail silently, engagement in the channel, and an occasional human check that the changes it called material really were.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
