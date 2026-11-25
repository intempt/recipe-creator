---
frontmatter_id: cro-program
slash_command: /cro-program
description: Runs an A/B experiment with random variant assignment on the conversion path step you pick, and emails a weekly
  digest of step-by-step drop-off and the experiment's lift.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Runs an A/B test on the conversion path step you pick and emails a weekly digest of where visitors drop off and
    how each variant converts.
  parameters:
  - name: target_step
    type: string
    label: Conversion path step the test targets (its step name)
    required: true
  - name: variant_change
    type: text
    label: What variant B changes on that step (copy, layout or call to action)
    required: true
  - name: sample_size
    type: number
    label: Visitors needed per variant
    default: 2000
    required: false
  - name: test_duration
    type: duration
    label: Longest the test runs
    default: 30 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: conversion_path_events
    kind: event
    meaning: A customer moved through a step of the conversion path
    properties:
    - name: step_name
      type: string
      meaning: Name of the conversion path step reached
      optional: false
  steps:
  - id: s1
    builds: experiment
    uses:
    - conversion_path_events
    - target_step
    - variant_change
    - sample_size
    - test_duration
    instruction: 'Create an experiment for visitors who reach the conversion path step where {conversion_path_events.step_name}
      is {target_step}. Variant A keeps the step as it is. Variant B changes it this way: {variant_change}. Split visitors
      50/50 at random; devices any; display frequency always. Primary metric: share of visitors who do {conversion_path_events}
      for the next step after {target_step} within the same session. Stop when each variant has {sample_size} visitors or
      after {test_duration}, whichever comes first.'
  - id: s2
    builds: automation
    uses:
    - s1
    - conversion_path_events
    - target_step
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes {conversion_path_events}
      by {conversion_path_events.step_name} and writes these figures: visitors reaching each step in the last 7 days and in
      the 7 days before; the conversion rate from each step to the next in both windows; the step with the largest drop-off
      in the last 7 days; for the experiment from "Design the test" on {target_step}, visitors and next-step conversion rate
      per variant since it started, and the lift of variant B over variant A. Then it emails these figures as plain-text lines,
      each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Conversion optimization program

Slash command: /cro-program

## Step 1: Design the test

Create an experiment for visitors who reach the conversion path step where step name is the conversion path step the test targets (its step name). Variant A keeps the step as it is. Variant B changes it this way: the what variant B changes on that step (copy, layout or call to action). Split visitors 50/50 at random; devices any; display frequency always. Primary metric: share of visitors who do conversion path events for the next step after the conversion path step the test targets (its step name) within the same session. Stop when each variant has 2000 visitors or after 30 d, whichever comes first.

## Step 2: Email the weekly drop-off and lift digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes conversion path events by step name and writes these figures: visitors reaching each step in the last 7 days and in the 7 days before; the conversion rate from each step to the next in both windows; the step with the largest drop-off in the last 7 days; for the experiment from "Design the test" on the conversion path step the test targets (its step name), visitors and next-step conversion rate per variant since it started, and the lift of variant B over variant A. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
