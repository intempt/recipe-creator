---
frontmatter_id: win-loss-analysis
slash_command: /win-loss-analysis
description: Reads your closed deals to show which competitors, objections and decision criteria separate the ones you win from the ones you lose.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Reads closed deals to show which competitors, objections and decision criteria separate won deals from lost ones,
    then writes a battlecard and a tracking dashboard.
  parameters:
  - name: analysis_window
    type: duration
    label: Look-back window for closed deals
    default: 12 mo
    required: false
  requirements:
  - slot: closed_deal
    kind: event
    meaning: A deal was closed as won or lost
    properties:
    - name: outcome
      type: string
      meaning: Whether the deal was won or lost
      optional: false
    - name: competitor
      type: string
      meaning: Competitor named in the deal
      optional: true
    - name: objection
      type: text
      meaning: Objections raised during the deal
      optional: true
    - name: decision_criteria
      type: text
      meaning: Criteria the buyer used to decide
      optional: true
    - name: deal_size
      type: number
      meaning: Value of the deal
      optional: true
  steps:
  - id: s1
    builds: report
    instruction: 'Analyze {closed_deal} records from the last {analysis_window} that are won or lost. Extract patterns: competitive
      mentions ({closed_deal.competitor}), objection themes ({closed_deal.objection}), and decision criteria ({closed_deal.decision_criteria}).
      Compare how these differ between won and lost deals ({closed_deal.outcome}).'
  - id: s2
    builds: page
    uses:
    - s1
    instruction: Using the result of "Compare won and lost deals", generate a battlecard content asset summarizing competitive
      positioning, common objections, and counter-messaging.
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    instruction: Using the results of "Compare won and lost deals" and "Write the battlecard", compose a dashboard showing
      win/loss patterns by competitor ({closed_deal.competitor}), objection type ({closed_deal.objection}), and deal size
      ({closed_deal.deal_size}).
---

# Win/loss patterns from closed deals

Slash command: /win-loss-analysis

## Step 1: Compare won and lost deals

This step builds a report.
Analyze closed deals (won and lost) to extract patterns: competitive mentions, objection themes, decision criteria.

## Step 2: Write the battlecard

This step builds a page.
Generate a battlecard content asset summarizing competitive positioning, common objections, and counter-messaging. Use the result of "Compare won and lost deals".

## Step 3: Track the patterns over time

Compose a dashboard surfacing win/loss patterns by competitor, objection type, and deal size. Use the result of "Compare won and lost deals", "Write the battlecard".
