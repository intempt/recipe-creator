---
frontmatter_id: competitive-intel-monitoring-workflow
slash_command: /competitive-intel-monitoring-workflow
description: Weekly scheduled AI agent scrapes competitor websites, review sites, social, and news, then posts a summarized competitive intel briefing to Slack.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Every Monday morning an AI agent scrapes competitor sites, reviews, social and news, then posts a structured competitive
    intel briefing to Slack.
  parameters:
  - name: run_time
    type: string
    label: Weekly run time (local)
    default: 07:00
    required: false
  - name: run_day
    type: enum
    label: Weekly run day
    default: monday
    required: false
    options:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday
  - name: rate_limit_delay
    type: duration
    label: Delay between competitor iterations
    default: 10 s
    required: false
  - name: scrape_window
    type: duration
    label: Blog and news lookback window
    default: 7 d
    required: false
  - name: tag_leads_for_major_moves
    type: boolean
    label: Tag product and marketing leads for major moves
    default: true
    required: false
  - name: workflow_name
    type: string
    label: Workflow name
    default: Weekly competitive intel
    required: false
  requirements:
  - slot: competitor_list
    kind: knowledge
    meaning: A configured list of competitor domains (typically 3-7) for this workspace
  - slot: competitor_intel_channel
    kind: integration
    meaning: A Slack channel for competitive intel briefings, such as a competitive-intel channel
    channel: slack
  - slot: product_and_marketing_leads
    kind: segment
    meaning: The product and marketing leads who should be tagged for major competitive moves
    optional: true
  - slot: competitor_snapshot_history
    kind: knowledge
    meaning: Stored weekly snapshots of competitor public pages from prior runs, used for week-over-week comparison
  steps:
  - id: s1
    builds: automation
    uses:
    - workflow_name
    - run_day
    - run_time
    instruction: Create a workflow named "{workflow_name}" scheduled to run every {run_day} at {run_time} local time. Its
      goal is to replace the manual weekly check of competitor activity with a structured AI-generated briefing that product
      and sales teams can read in about 3 minutes.
  - id: s2
    builds: automation
    uses:
    - s1
    - competitor_list
    - run_day
    - run_time
    instruction: Configure the scheduled trigger to run every {run_day} at {run_time} local time. Skip the run if the workspace
      is paused or if no competitors are configured in {competitor_list}. Store a last-run timestamp so each weekly scrape
      fetches only content published since the prior run.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - competitor_list
    - rate_limit_delay
    instruction: Configure a loop that iterates over each competitor domain in {competitor_list}. For each competitor, run
      the scrape and analysis steps that follow. Wait {rate_limit_delay} between iterations to be polite to sources.
  - id: s4
    builds: automation
    uses:
    - s1
    - s3
    - scrape_window
    instruction: 'For each competitor, scrape these public sources: pricing page, product and features pages, blog posts from
      the last {scrape_window}, changelog or release notes page, careers page (hiring signals), review-site summary from G2
      and Capterra, and recent press releases. Respect robots.txt. Cache content and skip re-fetching pages that have not
      changed since the last run.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    - competitor_snapshot_history
    instruction: 'Use an AI research step to compare this week''s scraped content for each competitor against the last stored
      snapshot in {competitor_snapshot_history} and flag material changes. Material changes are: pricing changes, newly announced
      features, leadership changes found on careers or about pages, large customer wins from press releases, sentiment shifts
      on review sites, and hiring trends suggesting expansion in a product area. For each competitor, output a structured
      briefing with three parts: what changed, what did not change, and what to watch.'
  - id: s6
    builds: automation
    uses:
    - s1
    - s5
    instruction: 'Use an AI writing step to consolidate the per-competitor findings from "Compare against last week" into
      one weekly briefing with these sections: (a) top 3 most material competitive moves this week, (b) per-competitor highlights,
      (c) watch-list for next week covering developing stories, and (d) recommended responses, for example: a competitor launched
      a feature, our differentiator is still X, and product marketing may want to update positioning. Use a factual, concise,
      scannable tone.'
  - id: s7
    builds: automation
    uses:
    - s1
    - s6
    - competitor_intel_channel
    - product_and_marketing_leads
    - tag_leads_for_major_moves
    instruction: Post the briefing from "Write the briefing" to {competitor_intel_channel} using a rich block layout with
      sections and links to each source page. Open a thread under the post for team discussion. If {tag_leads_for_major_moves}
      is true, tag {product_and_marketing_leads} on any major move.
  - id: s8
    builds: automation
    uses:
    - s1
    - s7
    instruction: 'Validate the workflow and publish it. Monitor three things: weekly briefing delivery, which must not fail
      silently; team engagement, measured by reactions and thread replies; and accuracy, through an occasional human spot-check
      that the AI correctly identified material changes.'
---

# Weekly competitive intel briefing

Slash command: /competitive-intel-monitoring-workflow

## Step 1: Replace the Monday check

Create a workflow 'Weekly competitive intel' scheduled to run every Monday morning. Goal: replace the manual 'check what competitors did this week' task with a structured AI-generated briefing the product and sales teams can consume in 3 minutes.

## Step 2: Run it Monday at 7am

This step builds a workflow.
Configure scheduled trigger: Every Monday at 7am local time. Skip if workspace is paused or no competitors are configured. Track last-run timestamp so weekly scrapes only fetch new content since prior run. Use the result of "Replace the Monday check".

## Step 3: Go through each competitor

This step builds a workflow.
Configure loop step that iterates over a configured list of competitor domains (configurable per workspace, typically 3-7 named competitors). For each competitor, run the subsequent scrape + analyze steps. Rate-limit between iterations to be polite to sources. Use the result of "Replace the Monday check", "Run it Monday at 7am".

## Step 4: Read their public pages

This step builds a workflow.
Configure web scrape step for each competitor: pricing page, product/features pages, blog (last 7 days), changelog/release-notes page, careers page (hiring signals), G2/Capterra review summary, recent press releases. Respect robots.txt; cache to avoid re-fetching unchanged content. Use the result of "Replace the Monday check", "Go through each competitor".

## Step 5: Compare against last week

This step builds a workflow.
Configure AI research step that compares this week's scraped content to last week's snapshot and flags material changes. Material = pricing changes, new features announced, leadership changes from careers/about pages, big customer wins from press releases, sentiment shifts on review sites, hiring trends suggesting product-area expansion. Outputs structured per-competitor briefing: what changed, what didn't, what to watch. Use the result of "Replace the Monday check", "Read their public pages".

## Step 6: Write the briefing

This step builds a workflow.
Configure AI write step that consolidates per-competitor findings into a single weekly briefing. Structure: (a) Top 3 most material competitive moves this week, (b) Per-competitor highlights, (c) Watch-list for next week (developing stories), (d) Recommended responses (e.g. 'Competitor X just launched [feature]: our differentiator is still Y; product marketing may want to update positioning'). Tone: factual, concise, scannable. Use the result of "Replace the Monday check", "Compare against last week".

## Step 7: Post it to the channel

This step builds a workflow.
Configure Slack step that posts the briefing to the configured competitive-intel channel (e.g. #competitive-intel). Format: rich block layout with sections, links to source pages, and a thread for team discussion. Tag product + marketing leads for major moves. Use the result of "Replace the Monday check", "Write the briefing".

## Step 8: Publish and spot check it

This step builds a workflow.
Validate and publish. Monitor: weekly briefing delivery (must not fail silently), team engagement (reactions, threads), and accuracy (occasional human spot-check that AI correctly identified material changes). Use the result of "Replace the Monday check", "Post it to the channel".
