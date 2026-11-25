---
frontmatter_id: business-review
slash_command: /business-review
description: Analyzes your headline KPIs on the cadence you pick and emails the scorecard, the changes against the period
  before, the wins, the concerns and a short narrative on what moved and why.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: 'Emails a scheduled business review: headline KPIs with period-over-period changes, top wins and concerns, and
    a short narrative on what moved and why.'
  parameters:
  - name: cadence
    type: enum
    label: Delivery cadence
    default: weekly
    required: false
    options:
    - daily
    - weekly
    - monthly
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: business_kpis
    kind: event
    meaning: A headline business metric value recorded for a period
    properties:
    - name: metric_name
      type: string
      meaning: Name of the metric
      optional: false
    - name: metric_value
      type: number
      meaning: Value of the metric for the period
      optional: false
    - name: period_date
      type: date
      meaning: Date of the period the value belongs to
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - business_kpis
    - cadence
    - digest_recipients
    instruction: 'Build an automation that runs at 08:00 on a schedule, every day when {cadence} is daily, every Monday when
      weekly, on the 1st of the month when monthly. Each run it analyzes {business_kpis} and writes these figures: for each
      {business_kpis.metric_name}, the latest {business_kpis.metric_value} for the last full period by {business_kpis.period_date},
      the value for the period before and the change in percent; the three metrics with the largest improvement as wins; the
      three with the largest decline as concerns; and a narrative of up to five sentences on what moved and the likely reason,
      with one recommended action. Then it emails these figures as plain-text lines, each with its period, to {digest_recipients}.
      Nothing else is sent.'
---

# Weekly business review pack

Slash command: /business-review

## Step 1: Email the business review

Build an automation that runs at 08:00 on a schedule, every day when weekly is daily, every Monday when weekly, on the 1st of the month when monthly. Each run it analyzes business kpis and writes these figures: for each metric name, the latest metric value for the last full period by period date, the value for the period before and the change in percent; the three metrics with the largest improvement as wins; the three with the largest decline as concerns; and a narrative of up to five sentences on what moved and the likely reason, with one recommended action. Then it emails these figures as plain-text lines, each with its period, to the email addresses that get the digest. Nothing else is sent.
