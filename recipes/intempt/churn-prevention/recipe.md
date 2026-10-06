---
id: churn-prevention
title: Churn prevention
slash_command: /churn-prevention
group: Journeys
owner: intempt
curator: somya
summary: Flags customers who are drifting away, reaches them automatically while it is still cheap to
  fix, and pulls in a CSM when it is not.
description: >-
  AI-derived risk scoring, CSM alerts, automated re-engagement, and retention measurement.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
    - media
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - churn-prevention
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new attribute, from step 1 "Score churn risk"
    - A new segment, from step 2 "Split into low, medium and high"
    - A new workflow, from step 3 "Tell the CSM about high risk"
    - A new designed email, from step 4 "Write the win back emails"
    - A new journey, from step 5 "Reach medium risk first"
    - A new report, from step 6 "Compare churn by risk tier"
    - A new dashboard, from step 7 "See if the saves are working"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Score churn risk
    summary: >-
      A churn risk score built from falling engagement, the tone of support tickets, and which features
      have gone unused.
    builds: attribute
    description: >-
      Define an AI-derived churn_risk_score attribute using engagement decline, support ticket sentiment,
      and feature-usage signals.
  - id: s2
    title: Split into low, medium and high
    summary: >-
      Three risk buckets off that score.
    builds: segment
    description: >-
      Segment users into low/medium/high churn-risk buckets. Use the result of "Score churn risk".
    dependsOn:
      - s1
  - id: s3
    title: Tell the CSM about high risk
    summary: >-
      When a user crosses the high risk threshold, their CSM gets a Slack message carrying the context
      behind the score.
    builds: workflow
    description: >-
      Create a workflow alerting CSMs when high-risk users cross the threshold, with context payload to
      Slack. Use the result of "Score churn risk", "Split into low, medium and high".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Write the win back emails
    summary: >-
      Emails that point to a feature they are missing, share a customer success story, and remind them
      what they are paying for.
    builds: email_html
    description: >-
      Generate re-engagement content: win-back-feature emails, success-story emails, value-reminder emails.
      Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high
      risk".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Reach medium risk first
    summary: >-
      Medium risk users get those emails automatically, before the account needs a CSM to step in.
    builds: journey
    description: >-
      Build a journey for medium-risk users with auto-engagement before CSM intervention is needed. Use
      the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk",
      "Write the win back emails".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: Compare churn by risk tier
    summary: >-
      Churn rate by risk tier and by which intervention the user received.
    builds: report
    description: >-
      Compose a retention report tracking churn rate by risk tier and intervention type. Use the result
      of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high risk", "Write
      the win back emails", "Reach medium risk first".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: See if the saves are working
    summary: >-
      Risk distribution, how often an intervention works, and the net effect on retention.
    builds: dashboard
    description: >-
      Compose a dashboard showing risk distribution, intervention success rate, and net retention impact.
      Use the result of "Score churn risk", "Split into low, medium and high", "Tell the CSM about high
      risk", "Write the win back emails", "Reach medium risk first", "Compare churn by risk tier".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: asset
    producedByStep: s4
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s5
    type: journey
    description: Journey produced by this recipe.
  - key: report
    producedByStep: s6
    type: report
    description: Report produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Churn prevention

Flags customers who are drifting away, reaches them automatically while it is still cheap to fix, and pulls in a CSM when it is not.

## Steps

1. **Score churn risk** (builds attribute)

   A churn risk score built from falling engagement, the tone of support tickets, and which features have gone unused.

2. **Split into low, medium and high** (builds segment)

   Three risk buckets off that score.

3. **Tell the CSM about high risk** (builds workflow)

   When a user crosses the high risk threshold, their CSM gets a Slack message carrying the context behind the score.

4. **Write the win back emails** (builds email_html)

   Emails that point to a feature they are missing, share a customer success story, and remind them what they are paying for.

5. **Reach medium risk first** (builds journey)

   Medium risk users get those emails automatically, before the account needs a CSM to step in.

6. **Compare churn by risk tier** (builds report)

   Churn rate by risk tier and by which intervention the user received.

7. **See if the saves are working** (builds dashboard)

   Risk distribution, how often an intervention works, and the net effect on retention.

## What you end up with

- **attribute** (attribute): Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **report** (report): Report produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new attribute, from step 1 "Score churn risk"
- A new segment, from step 2 "Split into low, medium and high"
- A new workflow, from step 3 "Tell the CSM about high risk"
- A new designed email, from step 4 "Write the win back emails"
- A new journey, from step 5 "Reach medium risk first"
- A new report, from step 6 "Compare churn by risk tier"
- A new dashboard, from step 7 "See if the saves are working"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, report, workflow.
