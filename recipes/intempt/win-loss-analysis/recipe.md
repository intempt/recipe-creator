---
frontmatter_id: win-loss-analysis
slash_command: /win-loss-analysis
description: Reads your closed deals every month and emails which competitors, objections and decision criteria separate the
  deals you win from the ones you lose, with a short battlecard.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a monthly digest of how won and lost deals differ by competitor, objection, decision criteria and deal size,
    with battlecard lines for the top competitors.
  parameters:
  - name: analysis_window
    type: duration
    label: Closed deals looked at
    default: 12 mo
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: closed_deal
    kind: event
    meaning: A deal was closed as won or lost
    properties:
    - name: outcome
      type: string
      meaning: won or lost
      optional: false
    - name: competitor
      type: string
      meaning: Competitor in the deal
      optional: false
    - name: objection
      type: string
      meaning: Main objection raised
      optional: false
    - name: decision_criteria
      type: string
      meaning: What the buyer decided on
      optional: false
    - name: deal_size
      type: number
      meaning: Deal amount
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - closed_deal
    - analysis_window
    - digest_recipients
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes {closed_deal}
      events in the last {analysis_window} and writes these figures: deals won and lost and the win rate, in the last {analysis_window}
      and in the last 30 days; win rate by {closed_deal.competitor} for the 5 most frequent competitors; the 5 most frequent
      {closed_deal.objection} values in lost deals and in won deals; the 5 most frequent {closed_deal.decision_criteria} values
      in won deals against lost deals; win rate and average {closed_deal.deal_size} by deal size band (under 10000, 10000
      to 50000, over 50000). Then it writes a battlecard of three lines per top-3 competitor: where we win, where we lose,
      and the counter to their most common objection, each drawn from those figures. It emails the figures as plain-text lines,
      each with its window, and the battlecard to {digest_recipients}. Nothing else is sent.'
---

# Win/loss patterns from closed deals

Slash command: /win-loss-analysis

## Step 1: Email the monthly win/loss digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes closed deal events in the last 12 mo and writes these figures: deals won and lost and the win rate, in the last 12 mo and in the last 30 days; win rate by competitor for the 5 most frequent competitors; the 5 most frequent objection values in lost deals and in won deals; the 5 most frequent decision criteria values in won deals against lost deals; win rate and average deal size by deal size band (under 10000, 10000 to 50000, over 50000). Then it writes a battlecard of three lines per top-3 competitor: where we win, where we lose, and the counter to their most common objection, each drawn from those figures. It emails the figures as plain-text lines, each with its window, and the battlecard to the email addresses that get the digest. Nothing else is sent.
