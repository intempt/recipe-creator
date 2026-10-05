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
  shortDescription: "Generates a CRO funnel drop-off report, experiment plan, personalization rule, email variants, and results dashboard."
  availability: coming-soon
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
      title: "Find Dropoff"
      command: build_funnel_report
      produces: report
      bindsAs: report
      description: "Build funnel report identifying highest-impact drop-off step in conversion path."
      prompt: "Build funnel report identifying highest-impact drop-off step in conversion path."
    - step: 2
      title: "Design Experiment"
      command: create_experiment
      produces: experiment
      bindsAs: experiment
      dependsOn: [report]
      description: "Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions."
      prompt: "Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions."
    - step: 3
      title: "Build Personalization"
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn: [report, experiment]
      description: "Configure personalization rule that serves variant content to assigned cohort."
      prompt: "Configure personalization rule that serves variant content to assigned cohort."
    - step: 4
      title: "Build Variants Content"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn: [report, experiment, personalization]
      description: "Generate variant content (copy, layout, CTA changes) per the experiment design."
      prompt: "Generate variant content (copy, layout, CTA changes) per the experiment design."
    - step: 5
      title: "Build Results Dashboard"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn: [report, experiment, personalization, asset]
      description: "Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance."
      prompt: "Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance."
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
    - { name: experiment, type: experiment, cardinality: single, description: "Experiment produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# CRO Program

## Procedure

1. **Find Dropoff** [`build_funnel_report`] — Build funnel report identifying highest-impact drop-off step in conversion path. → produces: report
2. **Design Experiment** [`create_experiment`] — Define experiment hypothesis, variants, primary metric, sample-size target, and stop conditions. → produces: experiment
3. **Build Personalization** [`create_personalization`] — Configure personalization rule that serves variant content to assigned cohort. → produces: personalization
4. **Build Variants Content** [`create_email_content`] — Generate variant content (copy, layout, CTA changes) per the experiment design. → produces: asset
5. **Build Results Dashboard** [`create_dashboard`] — Compose a dashboard tracking experiment lift, statistical significance, and segment-level performance. → produces: dashboard
