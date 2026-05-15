---
name: competitive-intel-monitoring-workflow
description: Use when a user mentions "competitive intel monitoring workflow", "competitor monitoring", "weekly competitive intel", or asks for related help. Weekly scheduled AI agent monitors competitor websites, review sites, social, and news for material moves (pricing change, feature launch, big customer win, leadership change). Summarizes into a structured competitive intel briefing posted to Slack for product + sales teams.
arguments: []
intempt:
  id: competitive-intel-monitoring-workflow
  version: 1.0.0
  slashCommand: /competitive-intel-monitoring-workflow
  group: Workflows
  shortDescription: "Weekly scheduled AI agent monitors competitor websites, review sites, social, and news for material moves (pricing change, feature launch, big customer win, leadership change). Summarizes into a structured competitive intel briefing posted to Slack for product + sales teams."
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
      title: Build the Competitive Monitoring Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Weekly competitive intel'' scheduled to run every Monday morning. Goal: replace the manual ''check what competitors did this week'' task with a structured AI-generated briefing the product and sales teams can consume in 3 minutes.'
      prompt: 'Create a workflow ''Weekly competitive intel'' scheduled to run every Monday morning. Goal: replace the manual ''check what competitors did this week'' task with a structured AI-generated briefing the product and sales teams can consume in 3 minutes.'
    - step: 2
      title: Scheduled Trigger
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: 'Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run.'
      prompt: 'Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run.'
    - step: 3
      title: Loop Through Tracked Competitors
      command: configure_loop_step
      produces: step
      bindsAs: loop
      dependsOn:
      - workflow
      - schedule
      description: Configure loop step that iterates over a configured list of competitor domains (configurable per workspace — typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze steps. Rate-limit between iterations to be polite to sources.
      prompt: Configure loop step that iterates over a configured list of competitor domains (configurable per workspace — typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze steps. Rate-limit between iterations to be polite to sources.
    - step: 4
      title: Scrape Competitor Surfaces
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      - loop
      description: 'Configure web scrape step for each competitor: pricing page, product/features pages, blog (last 7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary, recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content.'
      prompt: 'Configure web scrape step for each competitor: pricing page, product/features pages, blog (last 7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary, recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content.'
    - step: 5
      title: AI Analyze for Material Changes
      command: configure_ai_research_step
      produces: step
      bindsAs: analyze
      dependsOn:
      - workflow
      - scrape
      description: 'Configure AI research step that compares this week''s scraped content to last week''s snapshot and flags material changes. Material = pricing changes, new features announced, leadership changes from careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed, what didn''t, what to watch.'
      prompt: 'Configure AI research step that compares this week''s scraped content to last week''s snapshot and flags material changes. Material = pricing changes, new features announced, leadership changes from careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed, what didn''t, what to watch.'
    - step: 6
      title: AI-Draft Briefing Summary
      command: configure_write_with_ai_step
      produces: step
      bindsAs: briefing
      dependsOn:
      - workflow
      - analyze
      description: 'Configure AI write step that consolidates per-competitor findings into a single weekly briefing. Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c) Watch-list for next week (developing stories), (d) Recommended responses (e.g. ''Competitor X just launched [feature] — our differentiator is still Y; product marketing may want to update positioning''). Tone: factual, concise, scannable.'
      prompt: 'Configure AI write step that consolidates per-competitor findings into a single weekly briefing. Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c) Watch-list for next week (developing stories), (d) Recommended responses (e.g. ''Competitor X just launched [feature] — our differentiator is still Y; product marketing may want to update positioning''). Tone: factual, concise, scannable.'
    - step: 7
      title: 'Post to Slack #competitive-intel'
      command: configure_slack_step
      produces: step
      bindsAs: post
      dependsOn:
      - workflow
      - briefing
      description: 'Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel). Format: rich block layout with sections, links to source pages, and a thread for team discussion. Tag product + marketing leads for major moves.'
      prompt: 'Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel). Format: rich block layout with sections, links to source pages, and a thread for team discussion. Tag product + marketing leads for major moves.'
    - step: 8
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - post
      description: 'Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material changes).'
      prompt: 'Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material changes).'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Competitive Intel Monitoring Workflow

## Procedure

1. **Build the Competitive Monitoring Workflow** [`create_workflow`] — Create a workflow 'Weekly competitive intel' scheduled to run every Monday morning. Goal: replace the manual 'check what competitors did this week' task with a structured AI-generated briefing the product and sales teams can consume in 3 minutes. → produces: workflow
2. **Scheduled Trigger** [`configure_workflow_wait_until_step`] — Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run. → produces: step
3. **Loop Through Tracked Competitors** [`configure_loop_step`] — Configure loop step that iterates over a configured list of competitor domains (configurable per workspace — typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze steps. Rate-limit between iterations to be polite to sources. → produces: step
4. **Scrape Competitor Surfaces** [`configure_web_scrape_step`] — Configure web scrape step for each competitor: pricing page, product/features pages, blog (last 7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary, recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content. → produces: step
5. **AI Analyze for Material Changes** [`configure_ai_research_step`] — Configure AI research step that compares this week's scraped content to last week's snapshot and flags material changes. Material = pricing changes, new features announced, leadership changes from careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed, what didn't, what to watch. → produces: step
6. **AI-Draft Briefing Summary** [`configure_write_with_ai_step`] — Configure AI write step that consolidates per-competitor findings into a single weekly briefing. Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c) Watch-list for next week (developing stories), (d) Recommended responses (e.g. 'Competitor X just launched [feature] — our differentiator is still Y; product marketing may want to update positioning'). Tone: factual, concise, scannable. → produces: step
7. **Post to Slack #competitive-intel** [`configure_slack_step`] — Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel). Format: rich block layout with sections, links to source pages, and a thread for team discussion. Tag product + marketing leads for major moves. → produces: step
8. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material changes). → produces: workflow
