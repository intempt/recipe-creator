---
id: cro-program
title: Conversion optimization program
slash_command: /cro-program
group: Experiments
owner: intempt
curator: rana
summary: >-
  Find the worst drop-off, run an A/B experiment with random variant assignment, and review lift and
  significance on the Result tab. Use Personalization separately for per-variant targeting.
description: >-
  Find drop-off, design the test, ship variants, analyze lift and significance on the Result tab. A/B
  assignment is random; per-variant targeting is handled by Personalization, not the experiment.
version: 2.0.0
classification:
  product:
    - marketing
  agent: experience-optimizer
  mode:
    - all
  industry:
    - ai
    - b2b-saas
    - ecommerce
    - media
    - social
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - cro-program
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new report, from step 1 "Find the worst drop-off"
    - A new A/B experiment, from step 2 "Design the test"
    - A new website personalization, from step 3 "Target the right visitors"
    - A new designed email, from step 4 "Write the variant content"
    - A new dashboard, from step 5 "Build the results dashboard"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find the worst drop-off
    summary: >-
      Builds a funnel report across the conversion path and identifies the step losing the most people,
      which is where a test is worth running.
    builds: report
    description: >-
      Build funnel report identifying highest-impact drop-off step in conversion path.
  - id: s2
    title: Design the test
    summary: >-
      Sets the hypothesis, the variants, the primary metric, how many people the test needs, and the conditions
      under which it stops.
    builds: experiment
    description: >-
      Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions.
      Use the result of "Find the worst drop-off".
    dependsOn:
      - s1
  - id: s3
    title: Target the right visitors
    summary: >-
      Configures the personalization rule that decides who sees which variant, so each cohort gets the
      content assigned to it.
    builds: personalization
    description: >-
      Configure personalization rule that serves variant content to assigned cohort. Use the result of
      "Find the worst drop-off", "Design the test".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Write the variant content
    summary: >-
      Generates the copy, layout and CTA changes for each variant, matching the design set in the previous
      step.
    builds: email_html
    description: >-
      Generate variant content (copy, layout, CTA changes) per the experiment design. Use the result of
      "Find the worst drop-off", "Design the test", "Target the right visitors".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Build the results dashboard
    summary: >-
      Composes a dashboard tracking lift per variant, whether the result is statistically significant,
      and how it breaks down by segment.
    builds: dashboard
    description: >-
      Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance.
      Use the result of "Find the worst drop-off", "Design the test", "Target the right visitors", "Write
      the variant content".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: report
    producedByStep: s1
    type: report
    description: Report produced by this recipe.
  - key: experiment
    producedByStep: s2
    type: experiment
    description: Experiment produced by this recipe.
  - key: personalization
    producedByStep: s3
    type: personalization
    description: Personalization produced by this recipe.
  - key: asset
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Conversion optimization program

Find the worst drop-off, run an A/B experiment with random variant assignment, and review lift and significance on the Result tab. Use Personalization separately for per-variant targeting.

## Steps

1. **Find the worst drop-off** (builds report)

   Builds a funnel report across the conversion path and identifies the step losing the most people, which is where a test is worth running.

2. **Design the test** (builds experiment)

   Sets the hypothesis, the variants, the primary metric, how many people the test needs, and the conditions under which it stops.

3. **Target the right visitors** (builds personalization)

   Configures the personalization rule that decides who sees which variant, so each cohort gets the content assigned to it.

4. **Write the variant content** (builds email_html)

   Generates the copy, layout and CTA changes for each variant, matching the design set in the previous step.

5. **Build the results dashboard** (builds dashboard)

   Composes a dashboard tracking lift per variant, whether the result is statistically significant, and how it breaks down by segment.

## What you end up with

- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new report, from step 1 "Find the worst drop-off"
- A new A/B experiment, from step 2 "Design the test"
- A new website personalization, from step 3 "Target the right visitors"
- A new designed email, from step 4 "Write the variant content"
- A new dashboard, from step 5 "Build the results dashboard"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, experiment, personalization, report.
