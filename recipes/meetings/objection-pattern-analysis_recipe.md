---
name: objection-pattern-analysis
description: 'Use when a user mentions "objection patterns", "objection analysis across calls", "meeting transcript search", or asks for related help. Run cross-corpus analysis on meeting transcripts: surface the most-frequent objections in the last 90 days, cluster them by theme, and produce a report ranking objections by frequency × deal value at stake. Feeds enablement and product feedback loops.'
arguments: []
intempt:
  id: objection-pattern-analysis
  version: 1.0.0
  slashCommand: /objection-pattern-analysis
  group: Meetings
  shortDescription: "'Run cross-corpus analysis on meeting transcripts: surface the most-frequent objections in the last 90 days, cluster them by theme, and produce a report ranking objections by frequency × deal value at stake. Feeds enablement and product feedback loops.'"
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
      title: Cluster Meeting Topics
      command: analyze_meeting_topics
      produces: topic_analysis
      bindsAs: topics
      description: 'Run topic clustering across all meeting transcripts in the last 90 days where meeting type is Discovery, Demo, or Proposal. Output: top 30 topic clusters by mention frequency, with cluster label, representative phrases, and meeting-count per cluster. Filter to objection-adjacent clusters (price, timing, competition, feature gaps, security, authority, trust, integration concerns).'
      prompt: 'Run topic clustering across all meeting transcripts in the last 90 days where meeting type is Discovery, Demo, or Proposal. Output: top 30 topic clusters by mention frequency, with cluster label, representative phrases, and meeting-count per cluster. Filter to objection-adjacent clusters (price, timing, competition, feature gaps, security, authority, trust, integration concerns).'
    - step: 2
      title: Surface Objection Quotes
      command: search_meeting_transcripts
      produces: transcript_search_results
      bindsAs: quotes
      dependsOn:
      - topics
      description: 'For each top objection cluster identified, search meeting transcripts for the 5 most representative verbatim quotes. Pull: quote text, meeting ID, meeting date, rep, account name, account ARR (if customer) or expected deal value (if prospect). The verbatim quotes are what makes the analysis usable — managers and enablement teams need to hear the actual language buyers use.'
      prompt: 'For each top objection cluster identified, search meeting transcripts for the 5 most representative verbatim quotes. Pull: quote text, meeting ID, meeting date, rep, account name, account ARR (if customer) or expected deal value (if prospect). The verbatim quotes are what makes the analysis usable — managers and enablement teams need to hear the actual language buyers use.'
    - step: 3
      title: Build Objection Pattern Report
      command: build_insights_report
      produces: report
      bindsAs: report
      dependsOn:
      - topics
      - quotes
      description: 'Compose an insights report ranking objections by frequency × deal value at stake (so a $500K deal mentioning ''too expensive'' weighs more than ten $5K deals). Per objection: cluster label, frequency in last 90 days, total deal value mentioned in those meetings, 3 example quotes, win-rate of deals where this objection was raised vs. comparable deals where it wasn''t. Tag each as: address-with-content (build a battlecard), address-with-product (real gap, hand to PM), or address-with-process (sales motion fix).'
      prompt: 'Compose an insights report ranking objections by frequency × deal value at stake (so a $500K deal mentioning ''too expensive'' weighs more than ten $5K deals). Per objection: cluster label, frequency in last 90 days, total deal value mentioned in those meetings, 3 example quotes, win-rate of deals where this objection was raised vs. comparable deals where it wasn''t. Tag each as: address-with-content (build a battlecard), address-with-product (real gap, hand to PM), or address-with-process (sales motion fix).'
    - step: 4
      title: Build Objection Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - topics
      - quotes
      - report
      description: 'Compose a live objection-tracking dashboard: top 10 objections this month (vs. last month — trend signal), top 5 fastest-growing objections (early warning for new competitor or market shift), objection-by-rep heatmap (which reps face which objections most — signals coaching needs), and recent verbatim quotes feed (refreshes weekly). This is the enablement team''s daily-driver view.'
      prompt: 'Compose a live objection-tracking dashboard: top 10 objections this month (vs. last month — trend signal), top 5 fastest-growing objections (early warning for new competitor or market shift), objection-by-rep heatmap (which reps face which objections most — signals coaching needs), and recent verbatim quotes feed (refreshes weekly). This is the enablement team''s daily-driver view.'
  outputs:
    - { name: topic_analysis, type: topic_analysis, cardinality: single, description: "Topic Analysis produced by this recipe." }
    - { name: transcript_search_results, type: transcript_search_results, cardinality: single, description: "Transcript Search Results produced by this recipe." }
    - { name: report, type: report, cardinality: single, description: "Insights Report produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Objection Pattern Analysis

## Procedure

1. **Cluster Meeting Topics** [`analyze_meeting_topics`] — Run topic clustering across all meeting transcripts in the last 90 days where meeting type is Discovery, Demo, or Proposal. Output: top 30 topic clusters by mention frequency, with cluster label, representative phrases, and meeting-count per cluster. Filter to objection-adjacent clusters (price, timing, competition, feature gaps, security, authority, trust, integration concerns). → produces: topic_analysis
2. **Surface Objection Quotes** [`search_meeting_transcripts`] — For each top objection cluster identified, search meeting transcripts for the 5 most representative verbatim quotes. Pull: quote text, meeting ID, meeting date, rep, account name, account ARR (if customer) or expected deal value (if prospect). The verbatim quotes are what makes the analysis usable — managers and enablement teams need to hear the actual language buyers use. → produces: transcript_search_results
3. **Build Objection Pattern Report** [`build_insights_report`] — Compose an insights report ranking objections by frequency × deal value at stake (so a $500K deal mentioning 'too expensive' weighs more than ten $5K deals). Per objection: cluster label, frequency in last 90 days, total deal value mentioned in those meetings, 3 example quotes, win-rate of deals where this objection was raised vs. comparable deals where it wasn't. Tag each as: address-with-content (build a battlecard), address-with-product (real gap, hand to PM), or address-with-process (sales motion fix). → produces: report
4. **Build Objection Dashboard** [`create_dashboard`] — Compose a live objection-tracking dashboard: top 10 objections this month (vs. last month — trend signal), top 5 fastest-growing objections (early warning for new competitor or market shift), objection-by-rep heatmap (which reps face which objections most — signals coaching needs), and recent verbatim quotes feed (refreshes weekly). This is the enablement team's daily-driver view. → produces: dashboard
