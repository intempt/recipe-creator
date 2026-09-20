---
name: cro-program
description: |
  Use when a user mentions "cro program", or asks for related help. Find drop-off, design experiment, ship variants, analyze, kill or promote.
arguments: []
intempt:
  id: cro-program
  version: 1.0.1
  slashCommand: /cro-program
  group: Experiments
  title: 'Conversion optimization program'
  shortDescription: 'Runs a full optimization cycle: find the worst drop-off, design the test, ship the variants, then kill or promote on the results.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: experience-optimizer
    mode: [all]
    complexity: advanced
    executionMode: live
    tags: [cro-program]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_funnel_report
    - create_experiment
    - create_personalization
    - create_email_content
    - create_dashboard
  procedure:
    - step: 1
      title: 'Find the worst drop-off'
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: 'Builds a funnel report across the conversion path and identifies the step losing the most people, which is where a test is worth running.'
      prompt: "Build funnel report identifying highest-impact drop-off step in conversion path."
    - step: 2
      title: 'Design the test'
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [report]
      description: 'Sets the hypothesis, the variants, the primary metric, how many people the test needs, and the conditions under which it stops.'
      prompt: "Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions."
    - step: 3
      title: 'Target the right visitors'
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [report, experiment]
      description: 'Configures the personalization rule that decides who sees which variant, so each cohort gets the content assigned to it.'
      prompt: "Configure personalization rule that serves variant content to assigned cohort."
    - step: 4
      title: 'Write the variant content'
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [report, experiment, personalization]
      description: 'Generates the copy, layout and CTA changes for each variant, matching the design set in the previous step.'
      prompt: "Generate variant content (copy, layout, CTA changes) per the experiment design."
    - step: 5
      title: 'Build the results dashboard'
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, experiment, personalization, asset]
      description: 'Composes a dashboard tracking lift per variant, whether the result is statistically significant, and how it breaks down by segment.'
      prompt: "Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Conversion optimization program

Runs a full optimization cycle: find the worst drop-off, design the test, ship the variants, then kill or promote on the results.

## What it does

1. **Find the worst drop-off** (`build_funnel_report`)

   Builds a funnel report across the conversion path and identifies the step losing the most people, which is where a test is worth running.

2. **Design the test** (`create_experiment`)

   Sets the hypothesis, the variants, the primary metric, how many people the test needs, and the conditions under which it stops.

3. **Target the right visitors** (`create_personalization`)

   Configures the personalization rule that decides who sees which variant, so each cohort gets the content assigned to it.

4. **Write the variant content** (`create_email_content`)

   Generates the copy, layout and CTA changes for each variant, matching the design set in the previous step.

5. **Build the results dashboard** (`create_dashboard`)

   Composes a dashboard tracking lift per variant, whether the result is statistically significant, and how it breaks down by segment.

## What you end up with

- **report** (report): Report produced by this recipe.
- **experiment** (experiment): Experiment produced by this recipe.
- **personalization** (personalization): Personalization produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
