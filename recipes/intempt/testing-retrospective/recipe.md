---
frontmatter_id: testing-retrospective
slash_command: /testing-retrospective
description: 'Analyzes every experiment run in the last quarter from exposure and conversion events and emails a retrospective:
  winners, losers, inconclusive tests and the patterns that repeat.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a quarterly retrospective of your experiments: each one''s result, the win rate, revenue impact and which
    traffic sources and surfaces won most often.'
  parameters:
  - name: quarter_period
    type: duration
    label: Period the retrospective covers
    default: 90 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: experiment_exposure
    kind: event
    meaning: A customer was exposed to an experiment variant
    properties:
    - name: experiment_id
      type: string
      meaning: The experiment
      optional: false
    - name: variant
      type: string
      meaning: The variant shown
      optional: false
    - name: traffic_source
      type: string
      meaning: Where the visitor came from
      optional: false
    - name: surface
      type: string
      meaning: Page or channel the experiment ran on
      optional: false
  - slot: conversion_event
    kind: event
    meaning: A customer completed a conversion goal after an experiment exposure
    properties:
    - name: experiment_id
      type: string
      meaning: The experiment credited
      optional: false
    - name: revenue
      type: number
      meaning: Revenue of the conversion
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - experiment_exposure
    - conversion_event
    - quarter_period
    - digest_recipients
    instruction: 'Build an automation that runs on the first day of each quarter at 08:00 on a schedule. Each run it analyzes
      {experiment_exposure} and {conversion_event} in the last {quarter_period}, grouped by {experiment_exposure.experiment_id}
      and {experiment_exposure.variant}, and writes these figures: for each experiment, users exposed and conversion rate
      per variant, and its result: winner when a variant beats the first variant by 95% confidence, loser when it is worse
      by 95% confidence, inconclusive otherwise; the number of experiments run and the win rate, against the {quarter_period}
      before; total {conversion_event.revenue} of winning variants; win rate by {experiment_exposure.traffic_source}; win
      rate by {experiment_exposure.surface}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Quarterly experiment retrospective

Slash command: /testing-retrospective

## Step 1: Email the quarter's experiment results

Build an automation that runs on the first day of each quarter at 08:00 on a schedule. Each run it analyzes experiment exposure and conversion event in the last 90 d, grouped by experiment id and variant, and writes these figures: for each experiment, users exposed and conversion rate per variant, and its result: winner when a variant beats the first variant by 95% confidence, loser when it is worse by 95% confidence, inconclusive otherwise; the number of experiments run and the win rate, against the 90 d before; total revenue of winning variants; win rate by traffic source; win rate by surface. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
