---
frontmatter_id: testing-retrospective
slash_command: /testing-retrospective
description: Builds a quarterly retrospective dashboard tracking exposure events, conversion metrics, and engagement trends across your testing periods.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: placeholder
  parameters:
  - name: quarter_period
    type: duration
    label: Length of the review period
    default: 90 d
    required: false
  requirements:
  - slot: experiment_exposure
    kind: event
    meaning: A customer was exposed to an experiment variant
    properties:
    - name: experiment_id
      type: string
      meaning: Identifier of the experiment
      optional: false
    - name: variant
      type: string
      meaning: Variant the customer saw
      optional: false
    - name: traffic_source
      type: string
      meaning: Source of the traffic that reached the experiment
      optional: true
    - name: surface
      type: string
      meaning: Surface where the exposure happened
      optional: true
  - slot: conversion_event
    kind: event
    meaning: A customer completed a conversion goal after an experiment exposure
    properties:
    - name: experiment_id
      type: string
      meaning: Identifier of the experiment
      optional: false
    - name: revenue
      type: number
      meaning: Revenue value of the conversion
      optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - experiment_exposure
    - conversion_event
    - quarter_period
    instruction: Compile results for all experiments run in the last {quarter_period}, classifying each as winner, loser or
      inconclusive. Base the classification on exposure counts from {experiment_exposure} and conversions from {conversion_event},
      grouped by {experiment_exposure.experiment_id} and {experiment_exposure.variant}.
  - id: s2
    builds: report
    uses:
    - s1
    - experiment_exposure
    instruction: 'Using the results of "Compile the quarter''s results", generate an insights report on repeating patterns:
      which hypothesis families won, how winning rates differed by {experiment_exposure.traffic_source}, and which {experiment_exposure.surface}
      performed best.'
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - quarter_period
    instruction: Using the results of "Compile the quarter's results" and "Find the patterns that repeat", compose a dashboard
      over the last {quarter_period} summarizing testing cadence, win rate and revenue impact.
---

# Quarterly experiment retrospective

Slash command: /testing-retrospective

## Step 1: Compile the quarter's results

This step builds a report.
Compile results across all experiments run in the period: winners, losers, inconclusive.

## Step 2: Find the patterns that repeat

Generate insights report extracting patterns: which hypothesis families won, which traffic sources differed, best surfaces. Use the result of "Compile the quarter's results".

## Step 3: Track cadence and impact

Compose a dashboard summarizing testing cadence, win rate, and revenue impact. Use the result of "Compile the quarter's results", "Find the patterns that repeat".
