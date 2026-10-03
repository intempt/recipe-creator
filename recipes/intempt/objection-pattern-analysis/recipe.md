---
id: objection-pattern-analysis
title: What buyers push back on
slash_command: /objection-pattern-analysis
group: Meetings
owner: intempt
summary: Reads 90 days of call transcripts to rank the objections you hear most, weighted by the deal
  value behind them, with the buyer's own words attached.
description: >-
  Run cross-corpus analysis on meeting transcripts: surface the most-frequent objections in the last 90
  days, cluster them by theme, and produce a report ranking objections by frequency × deal value at stake.
  Feeds enablement and product feedback loops.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - transcript-analysis
    - objection-handling
    - enablement
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A meeting action, from step 1 "Cluster what gets discussed"
    - A meeting action, from step 2 "Pull the buyer's own words"
    - A new report, from step 3 "Rank objections by money at stake"
    - A new dashboard, from step 4 "Watch objections month to month"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Cluster what gets discussed
    summary: >-
      Topic clusters across 90 days of discovery, demo and proposal transcripts, narrowed to price, timing,
      competition, feature gaps, security, authority, trust and integrations.
    builds: meeting
    description: >-
      Run topic clustering across all meeting transcripts in the last 90 days where meeting type is Discovery,
      Demo, or Proposal. Output: top 30 topic clusters by mention frequency, with cluster label, representative
      phrases, and meeting-count per cluster. Filter to objection-adjacent clusters (price, timing, competition,
      feature gaps, security, authority, trust, integration concerns).
  - id: s2
    title: Pull the buyer's own words
    summary: >-
      Five representative verbatim quotes per objection, each with the meeting, the rep, the account and
      the revenue at stake.
    builds: meeting
    description: >-
      For each top objection cluster identified, search meeting transcripts for the 5 most representative
      verbatim quotes. Pull: quote text, meeting ID, meeting date, rep, account name, account ARR (if
      customer) or expected deal value (if prospect). The verbatim quotes are what makes the analysis
      usable: managers and enablement teams need to hear the actual language buyers use. Use the result
      of "Cluster what gets discussed".
    dependsOn:
      - s1
  - id: s3
    title: Rank objections by money at stake
    summary: >-
      Objections ranked by how often they come up multiplied by the deal value behind them, with the win
      rate when each is raised versus when it is not, and each tagged as a content, product or qualification
      fix.
    builds: report
    description: >-
      Compose an insights report ranking objections by frequency × deal value at stake (so a $500K deal
      mentioning 'too expensive' weighs more than ten $5K deals). Per objection: cluster label, frequency
      in last 90 days, total deal value mentioned in those meetings, 3 example quotes, win-rate of deals
      where this objection was raised vs. comparable deals where it wasn't. Tag each as: address-with-content
      (build a battlecard), address-with-product (real gap, hand to PM), or address-with-process (sales
      motion fix). Use the result of "Cluster what gets discussed", "Pull the buyer's own words".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Watch objections month to month
    summary: >-
      Top objections this month against last month, the fastest-growing ones, and which reps hear which
      objections most.
    builds: dashboard
    description: >-
      Compose a live objection-tracking dashboard: top 10 objections this month (vs. last month: trend
      signal), top 5 fastest-growing objections (early warning for new competitor or market shift), objection-by-rep
      heatmap (which reps face which objections most: signals coaching needs), and recent verbatim quotes
      feed (refreshes weekly). This is the enablement team's daily-driver view. Use the result of "Cluster
      what gets discussed", "Pull the buyer's own words", "Rank objections by money at stake".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: topic_analysis
    producedByStep: s1
    type: topic_analysis
    description: Topic Analysis produced by this recipe.
  - key: transcript_search_results
    producedByStep: s2
    type: transcript_search_results
    description: Transcript Search Results produced by this recipe.
  - key: report
    producedByStep: s3
    type: report
    description: Insights Report produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# What buyers push back on

Reads 90 days of call transcripts to rank the objections you hear most, weighted by the deal value behind them, with the buyer's own words attached.

## Steps

1. **Cluster what gets discussed** (builds meeting)

   Topic clusters across 90 days of discovery, demo and proposal transcripts, narrowed to price, timing, competition, feature gaps, security, authority, trust and integrations.

2. **Pull the buyer's own words** (builds meeting)

   Five representative verbatim quotes per objection, each with the meeting, the rep, the account and the revenue at stake.

3. **Rank objections by money at stake** (builds report)

   Objections ranked by how often they come up multiplied by the deal value behind them, with the win rate when each is raised versus when it is not, and each tagged as a content, product or qualification fix.

4. **Watch objections month to month** (builds dashboard)

   Top objections this month against last month, the fastest-growing ones, and which reps hear which objections most.

## What you end up with

- **topic_analysis** (topic_analysis): Topic Analysis produced by this recipe.
- **transcript_search_results** (transcript_search_results): Transcript Search Results produced by this recipe.
- **report** (report): Insights Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A meeting action, from step 1 "Cluster what gets discussed"
- A meeting action, from step 2 "Pull the buyer's own words"
- A new report, from step 3 "Rank objections by money at stake"
- A new dashboard, from step 4 "Watch objections month to month"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, report.
