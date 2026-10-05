---
id: competitive-intel-monitoring-workflow
title: Weekly competitive intel briefing
slash_command: /competitive-intel-monitoring-workflow
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Weekly scheduled AI agent scrapes competitor websites, review sites, social, and news, then posts a
  summarized competitive intel briefing to Slack.
description: >-
  A weekly scheduled AI agent gathers public information from competitor websites, review sites, social, and
  news, then summarizes it into a structured competitive intel briefing posted to Slack for product and sales
  teams.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - competitive-intelligence
    - scheduled-research
    - ai-monitoring
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new workflow, from step 1 "Replace the Monday check"
    - A new workflow, from step 2 "Run it Monday at 7am"
    - A new workflow, from step 3 "Go through each competitor"
    - A new workflow, from step 4 "Read their public pages"
    - A new workflow, from step 5 "Compare against last week"
    - A new workflow, from step 6 "Write the briefing"
    - A new workflow, from step 7 "Post it to the channel"
    - A new workflow, from step 8 "Publish and spot check it"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Replace the Monday check
    summary: >-
      Runs every Monday morning and produces a briefing product and sales can read in three minutes, instead
      of somebody manually checking what competitors did.
    builds: workflow
    description: >-
      Create a workflow 'Weekly competitive intel' scheduled to run every Monday morning. Goal: replace
      the manual 'check what competitors did this week' task with a structured AI-generated briefing the
      product and sales teams can consume in 3 minutes.
  - id: s2
    title: Run it Monday at 7am
    summary: >-
      Scheduled weekly in local time, skipped if the workspace is paused or no competitors are configured,
      and it only fetches what has appeared since the last run.
    builds: workflow
    description: >-
      Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors
      are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run.
      Use the result of "Replace the Monday check".
    dependsOn:
      - s1
  - id: s3
    title: Go through each competitor
    summary: >-
      Loops the three to seven competitor domains you configure, running the scrape and the analysis for
      each, with a pause between them to stay polite to the sources.
    builds: workflow
    description: >-
      Configure loop step that iterates over a configured list of competitor domains (configurable per
      workspace, typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze
      steps. Rate-limit between iterations to be polite to sources. Use the result of "Replace the Monday
      check", "Run it Monday at 7am".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Read their public pages
    summary: >-
      Pricing, product and feature pages, the last seven days of blog posts, the changelog, the careers
      page for hiring signals, review site summaries and recent press releases. It honours robots.txt
      and caches anything unchanged.
    builds: workflow
    description: >-
      Configure web scrape step for each competitor: pricing page, product/features pages, blog (last
      7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary,
      recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content. Use the
      result of "Replace the Monday check", "Go through each competitor".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Compare against last week
    summary: >-
      This week's content is set against last week's snapshot and only material changes are kept: price
      moves, new features, leadership changes, big customer wins, shifts in review sentiment, and hiring
      that points at a new product area. Per competitor it says what changed, what did not, and what to
      watch.
    builds: workflow
    description: >-
      Configure AI research step that compares this week's scraped content to last week's snapshot and
      flags material changes. Material = pricing changes, new features announced, leadership changes from
      careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring
      trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed,
      what didn't, what to watch. Use the result of "Replace the Monday check", "Read their public pages".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Write the briefing
    summary: >-
      One document: the three most significant moves of the week, the highlights per competitor, what
      to watch next week, and what you might do about it. Factual and scannable.
    builds: workflow
    description: >-
      Configure AI write step that consolidates per-competitor findings into a single weekly briefing.
      Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c)
      Watch-list for next week (developing stories), (d) Recommended responses (e.g. 'Competitor X just
      launched [feature]: our differentiator is still Y; product marketing may want to update positioning').
      Tone: factual, concise, scannable. Use the result of "Replace the Monday check", "Compare against
      last week".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Post it to the channel
    summary: >-
      The briefing goes to your competitive intel channel, laid out in sections with links back to the
      sources and a thread for discussion. Product and marketing leads are tagged on the big moves.
    builds: workflow
    description: >-
      Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel).
      Format: rich block layout with sections, links to source pages, and a thread for team discussion.
      Tag product + marketing leads for major moves. Use the result of "Replace the Monday check", "Write
      the briefing".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Publish and spot check it
    summary: >-
      Validated and published, with weekly delivery watched so it cannot fail silently, engagement in
      the channel, and an occasional human check that the changes it called material really were.
    builds: workflow
    description: >-
      Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement
      (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material
      changes). Use the result of "Replace the Monday check", "Post it to the channel".
    dependsOn:
      - s1
      - s7
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s7
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Weekly competitive intel briefing

Weekly scheduled AI agent scrapes competitor websites, review sites, social, and news, then posts a summarized competitive intel briefing to Slack.

## Steps

1. **Replace the Monday check** (builds workflow)

   Runs every Monday morning and produces a briefing product and sales can read in three minutes, instead of somebody manually checking what competitors did.

2. **Run it Monday at 7am** (builds workflow)

   Scheduled weekly in local time, skipped if the workspace is paused or no competitors are configured, and it only fetches what has appeared since the last run.

3. **Go through each competitor** (builds workflow)

   Loops the three to seven competitor domains you configure, running the scrape and the analysis for each, with a pause between them to stay polite to the sources.

4. **Read their public pages** (builds workflow)

   Pricing, product and feature pages, the last seven days of blog posts, the changelog, the careers page for hiring signals, review site summaries and recent press releases. It honours robots.txt and caches anything unchanged.

5. **Compare against last week** (builds workflow)

   This week's content is set against last week's snapshot and only material changes are kept: price moves, new features, leadership changes, big customer wins, shifts in review sentiment, and hiring that points at a new product area. Per competitor it says what changed, what did not, and what to watch.

6. **Write the briefing** (builds workflow)

   One document: the three most significant moves of the week, the highlights per competitor, what to watch next week, and what you might do about it. Factual and scannable.

7. **Post it to the channel** (builds workflow)

   The briefing goes to your competitive intel channel, laid out in sections with links back to the sources and a thread for discussion. Product and marketing leads are tagged on the big moves.

8. **Publish and spot check it** (builds workflow)

   Validated and published, with weekly delivery watched so it cannot fail silently, engagement in the channel, and an occasional human check that the changes it called material really were.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new workflow, from step 1 "Replace the Monday check"
- A new workflow, from step 2 "Run it Monday at 7am"
- A new workflow, from step 3 "Go through each competitor"
- A new workflow, from step 4 "Read their public pages"
- A new workflow, from step 5 "Compare against last week"
- A new workflow, from step 6 "Write the briefing"
- A new workflow, from step 7 "Post it to the channel"
- A new workflow, from step 8 "Publish and spot check it"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
