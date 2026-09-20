---
name: objection-pattern-analysis
description: 'Use when a user mentions "objection patterns", "objection analysis across calls", "meeting transcript search", or asks for related help. Run cross-corpus analysis on meeting transcripts: surface the most-frequent objections in the last 90 days, cluster them by theme, and produce a report ranking objections by frequency × deal value at stake. Feeds enablement and product feedback loops.'
arguments: []
intempt:
  id: objection-pattern-analysis
  version: 1.0.0
  slashCommand: /objection-pattern-analysis
  group: Meetings
  title: "What buyers push back on"
  shortDescription: "Reads 90 days of call transcripts to rank the objections you hear most, weighted by the deal value behind them, with the buyer's own words attached."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [transcript-analysis, objection-handling, enablement]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - analyze_meeting_topics
    - search_meeting_transcripts
    - build_insights_report
    - create_dashboard
  procedure:
    - step: 1
      title: "Cluster what gets discussed"
      command: analyze_meeting_topics
      produces: topic_analysis
      bindsAs: topics
      description: "Topic clusters across 90 days of discovery, demo and proposal transcripts, narrowed to price, timing, competition, feature gaps, security, authority, trust and integrations."
      prompt: 'Run topic clustering across all meeting transcripts in the last 90 days where meeting type is Discovery, Demo, or Proposal. Output: top 30 topic clusters by mention frequency, with cluster label, representative phrases, and meeting-count per cluster. Filter to objection-adjacent clusters (price, timing, competition, feature gaps, security, authority, trust, integration concerns).'
    - step: 2
      title: "Pull the buyer's own words"
      command: search_meeting_transcripts
      produces: transcript_search_results
      bindsAs: quotes
      dependsOn:
      - topics
      description: "Five representative verbatim quotes per objection, each with the meeting, the rep, the account and the revenue at stake."
      prompt: 'For each top objection cluster identified, search meeting transcripts for the 5 most representative verbatim quotes. Pull: quote text, meeting ID, meeting date, rep, account name, account ARR (if customer) or expected deal value (if prospect). The verbatim quotes are what makes the analysis usable: managers and enablement teams need to hear the actual language buyers use.'
    - step: 3
      title: "Rank objections by money at stake"
      command: build_insights_report
      produces: report
      bindsAs: report
      dependsOn:
      - topics
      - quotes
      description: "Objections ranked by how often they come up multiplied by the deal value behind them, with the win rate when each is raised versus when it is not, and each tagged as a content, product or qualification fix."
      prompt: 'Compose an insights report ranking objections by frequency × deal value at stake (so a $500K deal mentioning ''too expensive'' weighs more than ten $5K deals). Per objection: cluster label, frequency in last 90 days, total deal value mentioned in those meetings, 3 example quotes, win-rate of deals where this objection was raised vs. comparable deals where it wasn''t. Tag each as: address-with-content (build a battlecard), address-with-product (real gap, hand to PM), or address-with-process (sales motion fix).'
    - step: 4
      title: "Watch objections month to month"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - topics
      - quotes
      - report
      description: "Top objections this month against last month, the fastest-growing ones, and which reps hear which objections most."
      prompt: 'Compose a live objection-tracking dashboard: top 10 objections this month (vs. last month: trend signal), top 5 fastest-growing objections (early warning for new competitor or market shift), objection-by-rep heatmap (which reps face which objections most: signals coaching needs), and recent verbatim quotes feed (refreshes weekly). This is the enablement team''s daily-driver view.'
  outputs:
    - { name: topic_analysis, type: topic_analysis, cardinality: single, description: "Topic Analysis produced by this recipe." }
    - { name: transcript_search_results, type: transcript_search_results, cardinality: single, description: "Transcript Search Results produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# What buyers push back on

Reads 90 days of call transcripts to rank the objections you hear most, weighted by the deal value behind them, with the buyer's own words attached.

## What it does

1. **Cluster what gets discussed** (`analyze_meeting_topics`)

   Topic clusters across 90 days of discovery, demo and proposal transcripts, narrowed to price, timing, competition, feature gaps, security, authority, trust and integrations.

2. **Pull the buyer's own words** (`search_meeting_transcripts`)

   Five representative verbatim quotes per objection, each with the meeting, the rep, the account and the revenue at stake.

3. **Rank objections by money at stake** (`build_insights_report`)

   Objections ranked by how often they come up multiplied by the deal value behind them, with the win rate when each is raised versus when it is not, and each tagged as a content, product or qualification fix.

4. **Watch objections month to month** (`create_dashboard`)

   Top objections this month against last month, the fastest-growing ones, and which reps hear which objections most.

## What you end up with

- **topic_analysis** (topic_analysis): Topic Analysis produced by this recipe.
- **transcript_search_results** (transcript_search_results): Transcript Search Results produced by this recipe.
- **report** (report): Insights Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
