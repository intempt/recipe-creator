---
frontmatter_id: trial-to-paid-conversion-rate
slash_command: /trial-to-paid-conversion-rate
description: Emails a weekly digest of the share of trial starts that become paying customers, week by week and by signup
  source, against 18% and 25% benchmarks.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Emails a weekly digest of trial-to-paid conversion by trial-start week and signup source, against 18% and 25% benchmarks,
    with a flag on sharp drops.
  parameters:
  - name: trial_window_weeks
    type: number
    label: Weeks of trial starts in the digest
    default: 12
    required: false
  - name: benchmark_median
    type: number
    label: Median conversion benchmark (%)
    default: 18
    required: false
  - name: benchmark_top_quartile
    type: number
    label: Top-quartile conversion benchmark (%)
    default: 25
    required: false
  - name: drop_alert_points
    type: number
    label: Drop against the previous period that gets flagged (percentage points)
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: trial_started_event
    kind: event
    meaning: A customer started a subscription, which may include a trial period
    properties:
    - name: trial_start
      type: date
      meaning: When the trial began
      optional: false
    - name: trial_end
      type: date
      meaning: When the trial ended
      optional: false
  - slot: revenue_completed_event
    kind: event
    meaning: A customer completed a revenue payment
  - slot: invoice_paid_event
    kind: event
    meaning: An invoice was paid through the billing system
    optional: true
  - slot: user_utm_source
    kind: attribute
    meaning: The UTM source recorded on the user at signup
  steps:
  - id: s1
    builds: automation
    uses:
    - trial_started_event
    - revenue_completed_event
    - invoice_paid_event
    - user_utm_source
    - trial_window_weeks
    - benchmark_median
    - benchmark_top_quartile
    - drop_alert_points
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {trial_started_event}
      with {trial_started_event.trial_start} and {trial_started_event.trial_end} set, grouped by trial-start week over the
      last {trial_window_weeks} weeks, counting only weeks whose trials have ended, and writes these figures: for each week,
      trial starts and the conversion rate, the share who did {revenue_completed_event} or {invoice_paid_event} after their
      trial_end; the overall rate next to the {trial_window_weeks} weeks before; the rate and trial count by {user_utm_source},
      naming the source with both high conversion and high volume as the one to spend more on; where the latest rate sits
      against {benchmark_median}% and {benchmark_top_quartile}%. When the latest week dropped by more than {drop_alert_points}
      percentage points against the period before, the email''s first line says so. Then it emails these figures as plain-text
      lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Trial to paid conversion rate

Slash command: /trial-to-paid-conversion-rate

## Step 1: Email the weekly trial conversion digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did trial started event with trial start and trial end set, grouped by trial-start week over the last 12 weeks, counting only weeks whose trials have ended, and writes these figures: for each week, trial starts and the conversion rate, the share who did revenue completed event or invoice paid event after their trial_end; the overall rate next to the 12 weeks before; the rate and trial count by user utm source, naming the source with both high conversion and high volume as the one to spend more on; where the latest rate sits against 18% and 25%. When the latest week dropped by more than 3 percentage points against the period before, the email's first line says so. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
