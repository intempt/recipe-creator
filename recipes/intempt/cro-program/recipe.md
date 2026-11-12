---
frontmatter_id: cro-program
slash_command: /cro-program
description: Find the worst drop-off, run an A/B experiment with random variant assignment, and review lift and significance on the Result tab. Use Personalization separately for per-variant targeting.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Finds the worst funnel drop-off, designs and runs an A/B test with random variant assignment, writes variant content,
    and tracks lift and significance on a dashboard.
  parameters:
  - name: primary_metric
    type: string
    label: Primary metric
    default: conversion rate
    required: false
  - name: sample_size
    type: number
    label: Sample-size target
    required: true
  - name: tone
    type: string
    label: Copy tone for variant content
    default: not specified
    required: false
  requirements:
  - slot: conversion_path_events
    kind: event
    meaning: A customer moved through a step of the conversion path
    properties:
    - name: step_name
      type: text
      meaning: Name of the funnel step reached
      optional: false
  - slot: experiment_audience
    kind: segment
    meaning: The visitor group that the experiment is run on
  steps:
  - id: s1
    builds: report
    instruction: Build a funnel report over {conversion_path_events.step_name} that identifies the step with the highest-impact
      drop-off in the conversion path.
  - id: s2
    builds: experiment
    uses:
    - s1
    - primary_metric
    - sample_size
    instruction: Define the experiment hypothesis, two variants, the primary metric {primary_metric}, a sample-size target
      of {sample_size}, and stop conditions, targeting the drop-off step identified in "Find the worst drop-off".
  - id: s3
    builds: personalization
    uses:
    - s1
    - s2
    - experiment_audience
    instruction: Configure a personalization rule on {experiment_audience} that serves variant content to the assigned cohort
      per the design in "Design the test".
  - id: s4
    builds: email
    uses:
    - s1
    - s2
    - s3
    instruction: Generate variant content (copy, layout, CTA changes) per the experiment design in "Design the test", using
      a {tone} tone, aimed at the drop-off step from "Find the worst drop-off" and served to the cohort from "Target the right
      visitors".
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - experiment_audience
    instruction: Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance for
      {experiment_audience}, covering the variants from "Write the variant content" and the test from "Design the test".
---

# Conversion optimization program

Slash command: /cro-program

## Step 1: Find the worst drop-off

Build funnel report identifying highest-impact drop-off step in conversion path.

## Step 2: Design the test

Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions. Use the result of "Find the worst drop-off".

## Step 3: Target the right visitors

Configure personalization rule that serves variant content to assigned cohort. Use the result of "Find the worst drop-off", "Design the test".

## Step 4: Write the variant content

This step builds a designed marketing email (HTML).
Generate variant content (copy, layout, CTA changes) per the experiment design. Use the result of "Find the worst drop-off", "Design the test", "Target the right visitors".

## Step 5: Build the results dashboard

Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance. Use the result of "Find the worst drop-off", "Design the test", "Target the right visitors", "Write the variant content".
