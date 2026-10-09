---
description: Weekly scheduled AI agent scrapes competitor websites, review sites, social, and news, then posts a summarized competitive intel briefing to Slack.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - social
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
